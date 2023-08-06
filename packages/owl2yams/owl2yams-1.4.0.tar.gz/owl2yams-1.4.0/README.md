# OWL2YAMS

A script to create a new CubicWeb instance from OWL ontology and RDF data

## Installing the project

Create and activate a virtual environment
```
python3 -m venv my-virtual-env
source my-virtual-env/bin/activate
```

Install the dependencies, in this folder, run
```
pip install -e .
```

## Bootstrap a cube from a OWL file

This command will create a cube from the OWL file

```
owl2yams -m path/to/my-ontology.owl -n my_owl2yams_instance
```
It requires the ontology file path.

optional arguments:

| Option | Description |
| -------- | -------- |
| `-h, --help`     | how this help message and exit     |
| `--owl-model OWL_MODEL, -m OWL_MODEL` | Specify the OWL file to translate |
| `--instance-name INSTANCE_NAME, -n INSTANCE_NAME` | Specify the instance name for the CW instance |
| `--parse-format {turtle,xml,n3,nquads,nt,trix}, -f {turtle,xml,n3,nquads,nt,trix}` | pecify the OWL file serialization |
| `--dry-run, -d` | Print the YAMS schema only |
| `--only-cube` | Only create the cube and exit (no instance and db-init) |


## Populate a CubicWeb instance from RDF data

Run the script to populate your CubicWeb instance with your RDF data compliant
with the OWL ontology that was used to create your cube.

```
cubicweb-ctl import-rdf my_owl2yams_instance -f /path/to/rdfdata.ttl
```

optional arguments:
  --parse-format      The RDF serialization format between {turtle,xml,n3,nquads,nt,trix}


## Launch your CubicWeb instance

This command will launch the CubicWeb instance

```
cubicweb-ctl pyramid my_owl2yams_instance
```
By default it used the `8080` port. You can change this port using the environement variable
`CW_PORT`, which you can set with the following command:

```
export CW_PORT=8081
```

You know the server is running when you see the log
```
Serving on http://0.0.0.0:8080
```

## Use your CubicWeb instance

After those two commands, you can browse, create new data and more on your
web application.

Go to `http://localhost:8080` and you can start browsing, adding data, etc.

If you want to use this instance as a data server, there is an API available
automatically since the
(`cubicweb-api`)[https://forge.extranet.logilab.fr/cubicweb/cubes/api/] cube is
installed by default when using OWL2YAMS. You can find the
[`open-api`](https://www.openapis.org) spec using the route `/api/v1/openapi`.

This cube is mandatory to use the
(`cubicweb-react-admin`)[https://forge.extranet.logilab.fr/cubicweb/react-admin-cubicweb]
tool.  This tool lets you navigate and administrate your data using a modern
and dynamic interface.
