# -*- coding: utf-8 -*-
"""API specification using Open API"""

import flask
from apispec import APISpec

from .plugin import CONVERTER_MAPPING
from apispec.ext.marshmallow.swagger import FIELD_MAPPING


def make_apispec():
    return APISpec(
        title='OpenAPI spec',
        version='v1.0.0',
        plugins=[
            'flask_rest_api.spec.plugin',
            # XXX: Ideally, we shouldn't register schema_path_helper but it's
            # hard to extract only what we want from apispec.ext.marshmallow
            'apispec.ext.marshmallow',
        ]
    )


class ApiSpec(object):

    def __init__(self, app=None):

        self.spec = make_apispec()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        # TODO: set API info from app (title, description, version, etc...)

        # Add route to json spec file
        json_url = app.config.get('OPENAPI_URL', None)
        if json_url:
            app.add_url_rule(json_url, view_func=self.openapi_json)

    def openapi_json(self):
        """Serve json spec file"""
        return flask.jsonify(self.spec.to_dict())

    def register_converter(self, converter, conv_type, conv_format):
        CONVERTER_MAPPING[converter] = (conv_type, conv_format)

    def register_field(self, field, field_type, field_format):
        FIELD_MAPPING[field] = (field_type, field_format)
