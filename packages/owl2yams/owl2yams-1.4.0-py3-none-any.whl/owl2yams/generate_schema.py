# flake8: noqa
from yams.schema import Schema
from typing import Dict
import jinja2

schema_template = jinja2.Template(
    """
from yams.buildobjs import *


class equivalent_uri(RelationDefinition):  # type: ignore
    subject = ("CWEType", "CWRType", {% for fragment, _ in entitytype_fragment_to_uri.items() %}"{{fragment}}", {% endfor %})
    object = "ExternalUri"
    cardinality = "*?"


class label(RelationDefinition):  # type: ignore
    subject = ({% for fragment, _ in entitytype_fragment_to_uri.items() %}"{{fragment}}", {% endfor %})
    object = "Label"
    cardinality = "*?"


class Label(EntityType):  # type: ignore
    value = String(required=True)  # type: ignore
"""
)


def generate_schema(
    schema: Schema,
    entitytype_fragment_to_uri: Dict[str, str],
    relationtype_fragment_to_uri: Dict[str, str],
) -> str:
    rendered = schema_template.render(
        entitytype_fragment_to_uri=entitytype_fragment_to_uri,
        relationtype_fragment_to_uri=relationtype_fragment_to_uri,
    )
    return rendered if rendered is not None else ""
