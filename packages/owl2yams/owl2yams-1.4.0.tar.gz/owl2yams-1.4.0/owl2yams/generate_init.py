# flake8: noqa
from yams.schema import Schema
from typing import Dict

INIT = '''
"""cubicweb-cwaas_instance application package

cube representing {owl_file}
"""


def includeme(config):
    config.include(".views")
'''


def generate_init() -> str:
    return INIT
