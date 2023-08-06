# flake8: noqa
from yams.schema import Schema
from typing import Dict

APPJSTEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>CWaaS instance</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
       <div
           id="root"
           base_url="{{base_url}}"
       ></div>
       <script src="{{appjs_file}}"></script>
    </body>
</html>
"""


def generate_appjstemplate() -> str:
    return APPJSTEMPLATE
