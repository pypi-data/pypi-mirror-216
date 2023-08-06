# flake8: noqa
from yams.schema import Schema
from typing import Dict

VIEWS = """
# -*- coding: utf-8 -*-
# copyright 2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from pyramid.view import view_config


def build_jinja_dict(request, js_file="app.js"):
    cnx = request.cw_cnx
    appjs_file = cnx.vreg.config.datadir_url + js_file
    base_url = cnx.base_url()
    return {
        "base_url": base_url,
        "appjs_file": appjs_file,
    }


@view_config(
    route_name="raindex",
    renderer="appjs.jinja2",
)
def react_admin_index(request):
    return build_jinja_dict(request, js_file="appjs/main.js")


def includeme(config):
    config.include("pyramid_jinja2")

    config.add_route(
        "raindex",
        "/admin",
    )
    config.scan(__name__)
"""


def generate_views() -> str:
    return VIEWS
