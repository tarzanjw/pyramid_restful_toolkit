__author__ = 'tarzan'

import json
import unittest
from pyramid.config import Configurator
from webtest import TestApp
import logging
import pytest
import sys

logging.basicConfig(level=logging.INFO)

try:
    import schema
except ImportError:
    pass

try:
    import colander
    import deform
except ImportError:
    pass

try:
    import formencode
    from formencode import validators
except ImportError:
    pass


def sample_app(app_settings={}):

    def colander_view(request):
        class TestSchema(colander.MappingSchema):
            a = colander.SchemaNode(colander.Integer())
        s = TestSchema()
        return s.deserialize(request.POST)

    def schema_view(request):
        s = schema.Schema({
            'a': int,
        })
        return s.validate(request.POST.mixed())


    def deform_view(request):
        class TestSchema(colander.MappingSchema):
            a = colander.SchemaNode(colander.Integer())
        form = deform.Form(schema=TestSchema())
        return form.validate(request.POST.items())

    def formencode_view(request):
        class TestSchema(formencode.Schema):
            allow_extra_fields = True
            a = validators.Int()

        s = TestSchema()
        return s.to_python(request.POST)

    def error_response_view(request):
        from pyramid_restful_toolkit import ErrorResponse
        raise ErrorResponse(407, 'ha ha ha', 'noway')

    settings = {}
    settings.update(app_settings)
    config = Configurator(
        settings=settings,
    )
    config.include('pyramid_restful_toolkit')

    config.add_route('colander', '/colander')
    config.add_view(colander_view, route_name='colander', renderer='json')

    config.add_route('schema', '/schema')
    config.add_view(schema_view, route_name='schema', renderer='json')

    config.add_route('deform', '/deform')
    config.add_view(deform_view, route_name='deform', renderer='json')

    config.add_route('formencode', '/formencode')
    config.add_view(formencode_view, route_name='formencode', renderer='json')

    config.add_route('error_response', '/error_response')
    config.add_view(error_response_view, route_name='error_response', renderer='json')

    app = config.make_wsgi_app()
    return TestApp(app)


class ErrorHandlersTest(unittest.TestCase):
    def setUp(self):
        super(ErrorHandlersTest, self).setUp()
        self.app = sample_app({})

    def test_all_schemas(self):
        data = {'a': 'ha ha ha',
                'b': 2}
        for api_path in ['colander', 'schema', 'deform', 'formencode']:
            if api_path not in sys.modules: continue;

            rs = self.app.post('/'+api_path, params=data, expect_errors=True)
            """:type : webtest.TestResponse"""
            self.assertEqual(rs.status_int, 400)
            rdata = json.loads(rs.text)
            self.assertIn('error_code', rdata)
            self.assertEqual(rdata['error_code'], 400)
            self.assertIn('errors', rdata)
            self.assertTrue(len(rdata['errors']))

    def test_error_response(self):
        rs = self.app.get('/error_response', expect_errors=True)
        """:type : webtest.TestResponse"""
        self.assertEqual(rs.status_int, 407)
        rdata = json.loads(rs.text)

        self.assertIn('error_code', rdata)
        self.assertEqual(rdata['error_code'], 407)

        self.assertIn('errors', rdata)
        self.assertEqual(rdata['errors'], 'ha ha ha')

        self.assertIn('data', rdata)
        self.assertEqual(rdata['data'], 'noway')
