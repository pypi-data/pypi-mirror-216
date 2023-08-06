import itertools
import json
import os
import re
import shutil
import subprocess
import unicodedata
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse

from rdflib import OWL, RDF, RDFS, XSD, Graph, URIRef  # type: ignore
from rdflib.term import BNode
from redbaron import RedBaron
from yams.buildobjs import RelationDefinition  # type: ignore
from yams.buildobjs import EntityType, RelationType, register_base_types
from yams.schema import Schema  # type: ignore
from yams.serialize import serialize_to_python  # type: ignore

from owl2yams.generate_appjstemplate import generate_appjstemplate
from owl2yams.generate_entities import generate_entities
from owl2yams.generate_init import generate_init
from owl2yams.generate_postcreate import generate_postcreate
from owl2yams.generate_schema import generate_schema
from owl2yams.generate_views import generate_views

here = os.path.dirname(__file__)

LITERAL_TYPES_TO_YAMS_TYPES = {
    RDFS.Literal: "String",
    XSD.string: "String",
    XSD.int: "Int",
    XSD.integer: "Int",
    XSD.float: "Float",
    XSD.gYear: "Int",
    XSD.dateTime: "String",
}

with open(f"{here}/prefixes.json", "r") as fobj:
    PREFIXES = json.load(fobj)


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def fragment_from_uri(uri: str, titling=False, no_prefix=False) -> Optional[str]:
    if uri == OWL.Thing or uri == RDFS.Class:
        return None
    url = urlparse(uri)
    # if url.fragment is not None, the fragment is done with `#`
    if url.fragment:
        fragment = url.fragment
    else:
        # otherwise split with `/`
        fragment = url.path.split("/")[-1]
    prefix = ""
    # try to find prefix in list of prefixes
    unfragmented_url = uri.rstrip(fragment)
    if unfragmented_url in PREFIXES:
        prefix = PREFIXES[unfragmented_url] + "_"
    elif url.hostname is not None:
        prefix = url.hostname.replace("www.", "").replace(".", "_") + "_"
    if titling:
        prefix = prefix.title().replace("_", "")
    else:
        fragment = fragment.lower()
    fragment = strip_accents(fragment.replace("_", "").replace("-", ""))
    if no_prefix:
        return fragment
    else:
        return f"{prefix}{fragment}"


def property_range_domain_uris(owl_model, property_uri, domain=True):
    domain_range_property = "rdfs:domain"
    if not domain:
        domain_range_property = "rdfs:range"

    query_domains = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?uri WHERE {{
        {{<{property_uri}> {domain_range_property} ?uri. FILTER(!isBlank(?uri))}}
        UNION
        {{<{property_uri}> {domain_range_property} ?z.
            ?z owl:unionOf ?uri.
            FILTER (isBlank(?z))
            FILTER (!isBlank(?uri))
        }}
        UNION
        {{<{property_uri}> {domain_range_property} ?z.
            ?z owl:unionOf ?list.
            ?list rdf:rest*/rdf:first ?uri.
        }}
    }}
    """

    domain_uris = []
    # first, check if the property has its own domain defined
    for domain_res in owl_model.query(query_domains):
        domain_uri = domain_res.uri
        if isinstance(domain_uri, BNode):
            continue
        domain_uris.append(domain_uri)

    # if the property has its own domain/range defined
    # it is more specific than its parents so return it
    if len(domain_uris) > 0:
        return domain_uris

    # if it has no specification, perhaps its parents do
    query_parent_domains = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?uri WHERE {{
        <{property_uri}> rdfs:subPropertyOf+ ?prop.
        {{?prop {domain_range_property} ?uri.}}
        UNION
        {{?prop {domain_range_property} ?z.
        ?z owl:unionOf ?uri.}}
    }}
    """

    for parent_domain_res in owl_model.query(query_parent_domains):
        domain_uri = parent_domain_res.uri
        if isinstance(domain_uri, BNode):
            continue
        domain_uris.append(domain_uri)

    return domain_uris


def yams_domain_from_urirefs(
    uris: Iterable[URIRef], all_entity_types: Iterable[str], no_prefix=False
) -> List[str]:
    fragments: List[str] = []
    for uri in uris:
        if isinstance(uri, BNode):
            continue
        fragment = fragment_from_uri(uri, titling=True, no_prefix=no_prefix)
        if fragment is not None:
            fragments.append(fragment)
        else:
            return list(all_entity_types)
    if not len(fragments):
        return list(all_entity_types)
    return fragments


def owl_model_to_yams(
    owl_model: Graph, instance_name: str, no_prefix=False
) -> Tuple[Schema, Dict[str, str], Dict[str, str]]:
    entitytype_fragment_to_uri: Dict[str, str] = {}
    relationtype_fragment_to_uri: Dict[str, str] = {}
    # 0. Create a new YAMS Schema
    schema = Schema(instance_name)
    register_base_types(schema)

    # p = s._entities["Person"] # normalement p = s.entity_schema_for("Person")
    # p.check({'name':1})

    class_query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?uri WHERE {
            {?uri a owl:Class}
            UNION {?rangeprop rdfs:range ?uri.}
            UNION {?domainprop rdfs:domain ?uri.}
            UNION{?uri a rdfs:Class.}
        }
    """

    # 1. fetch all classes
    for class_res in owl_model.query(class_query):
        class_uri = class_res.uri
        if isinstance(class_uri, BNode) or class_uri.startswith(XSD):
            continue
        class_fragment = fragment_from_uri(class_uri, titling=True, no_prefix=no_prefix)
        if class_fragment is None:
            print(f"Warning: class {class_uri} could not be parsed")
            continue
        if class_fragment in schema:
            raise ValueError(
                f"Error: class {class_uri} and"
                f" {entitytype_fragment_to_uri[class_fragment]} use the same fragment"
            )
        entity_schema = schema.add_entity_type(EntityType(class_fragment))
        entitytype_fragment_to_uri[class_fragment] = class_uri
        superior_classes = []
        for _, _, superior_class_uri in owl_model.triples(
            (class_uri, RDFS.subClassOf, None)
        ):
            superior_class_fragment = fragment_from_uri(
                superior_class_uri, titling=True, no_prefix=no_prefix
            )
            if superior_class_fragment is not None:
                superior_classes.append(superior_class_fragment)
        if superior_classes:
            entity_schema._specialized_type = ", ".join(superior_classes)

    # 2. fetch all datatype properties

    datatype_property_query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT DISTINCT ?uri WHERE {
            {?uri a owl:DatatypeProperty}
            UNION {?uri a owl:AnnotationProperty.}
            UNION {?uri rdfs:range ?z.
            FILTER (?z in (xsd:int, rdfs:Literal, xsd:date, xsd:float, xsd:integer))}
        }
    """
    for datatype_property_res in owl_model.query(datatype_property_query):
        datatype_property_uri = datatype_property_res.uri
        datatype_property_uri_fragment = fragment_from_uri(
            datatype_property_uri, no_prefix=no_prefix
        )
        if datatype_property_uri_fragment is None:
            print(f"Warning: data property {datatype_property_uri} could not be parsed")
            continue
        if datatype_property_uri_fragment in schema:
            datatype_property_uri_fragment = datatype_property_uri_fragment + "_bis"
        schema.add_relation_type(RelationType(datatype_property_uri_fragment))
        relationtype_fragment_to_uri[
            datatype_property_uri_fragment
        ] = datatype_property_uri
        # take first range, if no range use RDFS.Literal
        _, _, literal_type = next(
            owl_model.triples((datatype_property_uri, RDFS.range, None)),
            (None, None, RDFS.Literal),
        )
        try:
            yams_type = LITERAL_TYPES_TO_YAMS_TYPES[literal_type]
        except Exception:
            print(
                f"replace {datatype_property_uri} range with String (cause BlankNode)"
            )
            yams_type = "String"

        domain_fragments = yams_domain_from_urirefs(
            property_range_domain_uris(owl_model, datatype_property_uri, domain=True),
            entitytype_fragment_to_uri.keys(),
            no_prefix=no_prefix,
        )
        for domain_fragment in domain_fragments:
            # if the parent of the domain is already in domain_fragments
            domain_parents_str = schema[domain_fragment]._specialized_type or ""
            domain_parents = domain_parents_str.split(", ")
            if set(domain_parents).intersection(set(domain_fragments)):
                continue
            schema.add_relation_def(
                RelationDefinition(
                    domain_fragment, datatype_property_uri_fragment, yams_type
                )
            )

    # 3. fetch all object properties

    for (
        object_property_uri,
        _,
        _,
    ) in owl_model.triples((None, RDF.type, OWL.ObjectProperty)):
        object_property_uri_fragment = fragment_from_uri(
            object_property_uri, no_prefix=no_prefix
        )
        if object_property_uri_fragment is None:
            print(f"Warning: object property {object_property_uri} could not be parsed")
            continue
        if object_property_uri_fragment in schema:
            object_property_uri_fragment += "_bis"
        schema.add_relation_type(RelationType(object_property_uri_fragment))
        relationtype_fragment_to_uri[object_property_uri_fragment] = object_property_uri
        all_types = list(entitytype_fragment_to_uri.keys())

        domain_fragments = yams_domain_from_urirefs(
            property_range_domain_uris(owl_model, object_property_uri, domain=True),
            all_types,
            no_prefix=no_prefix,
        )

        range_fragments = yams_domain_from_urirefs(
            property_range_domain_uris(owl_model, object_property_uri, domain=False),
            all_types,
            no_prefix=no_prefix,
        )

        for domain_fragment, range_fragment in itertools.product(
            domain_fragments, range_fragments
        ):
            schema.add_relation_def(
                RelationDefinition(
                    domain_fragment,
                    object_property_uri_fragment,
                    range_fragment,
                )
            )

    return schema, entitytype_fragment_to_uri, relationtype_fragment_to_uri


def run_and_print_if_error(command, custom_env=None):
    res = subprocess.run(command, shell=True, capture_output=True, env=custom_env)
    if res.returncode != 0:
        print(res.stdout.decode())
        print(res.stderr.decode())
        exit(1)
    return res


def generate_cubicweb_cube(
    owl_file="owl2yams/model.owl",
    instance_name="owl_instance",
    parse_format="turtle",
    dry_run=False,
    only_cube=False,
    base_url="http://localhost:8080/",
    no_prefix=False,
):
    owl_model = Graph()
    owl_model.parse(owl_file, format=parse_format)

    (
        schema,
        entitytype_fragment_to_uri,
        relationtype_fragment_to_uri,
    ) = owl_model_to_yams(owl_model, instance_name, no_prefix=no_prefix)

    if dry_run:
        print(serialize_to_python(schema))
        return

    cube_name = instance_name.replace("_", "-")
    cube_master_folder = f"cubicweb-{cube_name}"

    print(
        f"creating the cube inside the folder {cube_master_folder}/ "
        "(the schema is there)"
    )
    create_cube = (
        f'cubicweb-ctl newcube {instance_name} -s "cube representing {{owl_file}}"'
    )
    run_and_print_if_error(create_cube)

    cube_subfolder = cube_master_folder.replace("-", "_")

    model_schema_path = Path(f"{cube_master_folder}/{cube_subfolder}/schema/schema.py")
    model_schema_path.parent.mkdir(parents=True, exist_ok=True)

    with open(model_schema_path, "a") as f:
        f.write(serialize_to_python(schema))

    ccplugin_path = Path(f"{cube_master_folder}/{cube_subfolder}/ccplugin.py")
    shutil.copy(str(f"{here}/ccplugin.py"), str(ccplugin_path))

    appjs_path = Path(f"{cube_master_folder}/{cube_subfolder}/data/appjs")
    shutil.copytree(str(f"{here}/cw_react_admin"), str(appjs_path))

    with open(
        f"{cube_master_folder}/{cube_subfolder}/migration/postcreate.py", "a"
    ) as f:
        f.write(
            generate_postcreate(
                entitytype_fragment_to_uri, relationtype_fragment_to_uri
            )
        )

    with open(f"{cube_master_folder}/{cube_subfolder}/entities.py", "a") as f:
        f.write(
            generate_entities(
                schema, entitytype_fragment_to_uri, relationtype_fragment_to_uri
            )
        )

    with open(f"{cube_master_folder}/{cube_subfolder}/schema/__init__.py", "a") as f:
        f.write(
            generate_schema(
                schema, entitytype_fragment_to_uri, relationtype_fragment_to_uri
            )
        )

    with open(f"{cube_master_folder}/{cube_subfolder}/__init__.py", "a") as f:
        f.write(generate_init())
    with open(f"{cube_master_folder}/{cube_subfolder}/views.py", "a") as f:
        f.write(generate_views())
    with open(f"{cube_master_folder}/{cube_subfolder}/appjs.jinja2", "a") as f:
        f.write(generate_appjstemplate())

    # add dependencies
    pkginfo_path = Path(
        os.path.join(cube_master_folder, cube_subfolder, "__pkginfo__.py")
    )
    red = RedBaron(pkginfo_path.read_text())
    dependencies_node = red.find("assign", target=lambda x: x.value == "__depends__")
    dependencies = dependencies_node.value.to_python()
    dependencies["cubicweb"] = "<4.0.0"
    dependencies["cubicweb-api"] = None
    dependencies["pyramid-jinja2"] = None
    dependencies_node.value = str(dependencies)
    pkginfo_path.write_text(red.dumps())

    if only_cube:
        print("Cube correctly initialized")
        return

    # should pip install the cube
    pip_install_cube = f"pip install  -e cubicweb-{cube_name}"
    run_and_print_if_error(pip_install_cube)

    print(
        f"creating the instance {instance_name}. "
        f"The parameters are in ~/etc/cubicweb.d/{instance_name}/"
    )
    os.environ.setdefault("CW_DB_DRIVER", "sqlite")
    os.environ.setdefault(
        "CW_DB_NAME",
        str(
            Path.home()
            / "etc"
            / "cubicweb.d"
            / instance_name
            / f"{instance_name}.sqlite"
        ),
    )
    os.environ.setdefault("CW_ANONYMOUS_USER", "anon")
    os.environ.setdefault("CW_ANONYMOUS_PASSWORD", "anon")
    create_instance = (
        f"cubicweb-ctl create {instance_name} {instance_name} -a --no-db-create"
    )
    run_and_print_if_error(create_instance, custom_env=os.environ)

    source_path = os.path.expanduser(f"~/etc/cubicweb.d/{instance_name}/sources")
    # The source file has to be modified to include sqlite
    driver_regexp = re.compile("db-driver.*")
    admin_pass = re.compile("password=(.*)")
    dbname_regexp = re.compile("db-name=.*")
    with open(source_path, "r") as f:
        content = f.read()
        replaced_content = driver_regexp.sub("db-driver=sqlite", content)
        replaced_content = dbname_regexp.sub(
            f"db-name={os.getenv('CW_DB_NAME')}", replaced_content
        )
        admin_pwd = next(admin_pass.finditer(content)).group(1)

    with open(source_path, "w") as f:
        f.write(replaced_content)

    if os.environ["CW_ANONYMOUS_USER"]:
        all_in_one_path = (
            Path.home() / "etc" / "cubicweb.d" / instance_name / "all-in-one.conf"
        )
        all_in_one_content = all_in_one_path.read_text()
        all_in_one_path.write_text(
            all_in_one_content.replace(
                "#anonymous-user=", f"anonymous-user={os.environ['CW_ANONYMOUS_USER']}"
            )
            .replace(
                "#anonymous-password=",
                f"anonymous-password={os.environ['CW_ANONYMOUS_PASSWORD']}",
            )
            .replace("#base-url=", f"base-url={base_url}")
        )

    create_db_instance = (
        f"cubicweb-ctl db-create {instance_name} -a --create-db=y --drop=y"
    )
    run_and_print_if_error(create_db_instance, custom_env=os.environ)

    run_and_print_if_error(f"black {cube_master_folder}")

    print(
        "Congratulation ! You can run your instance with : "
        f"`cubicweb-ctl pyramid -D -l info {instance_name}`"
    )
    print(f"(admin password: {admin_pwd} (from {source_path})")


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--owl-model",
        "-m",
        default="owl2yams/model.owl",
        help="Specify the OWL file to translate",
    )
    parser.add_argument(
        "--instance-name",
        "-n",
        default="owl_instance",
        help="Specify the instance name for the CW instance",
    )
    parser.add_argument(
        "--parse-format",
        "-f",
        choices=["turtle", "xml", "n3", "nquads", "nt", "trix"],
        default="turtle",
        help="Specify the OWL file serialization",
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Print the YAMS schema only",
    )
    parser.add_argument(
        "--only-cube",
        action="store_true",
        help="Only create the cube and exit (no instance and db-init)",
    )
    parser.add_argument(
        "--base-url",
        "-b",
        default="http://localhost:8080/",
        help="Set CW URI base-url",
    )
    parser.add_argument(
        "--no-prefix",
        action="store_true",
        help="Do not prefix YAMS object with domain name",
    )

    args = parser.parse_args()
    generate_cubicweb_cube(
        args.owl_model,
        args.instance_name,
        args.parse_format,
        args.dry_run,
        args.only_cube,
        args.base_url,
        args.no_prefix,
    )
