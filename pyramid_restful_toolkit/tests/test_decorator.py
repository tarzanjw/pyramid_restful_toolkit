__author__ = 'tarzan'

import unittest
from pyramid import testing
from pyramid.response import Response
from pyramid_restful_toolkit import ErrorResponse
from pyramid_restful_toolkit.decorator import (
    rest_action,
    rest_error_adapter,
    register_error_adapter,
)


class TestDecorator(unittest.TestCase):

    def test_rest_action_decorator(self):

        @rest_action
        def view_with_request_only(request):
            return 'view_with_request_only'


        @rest_action
        def view_with_context_and_request(context, request):
            return 'view_with_context_and_request'

        class ClassBasedView(object):

            def __init__(self, context, request):
                self.context = context
                self.request = request

            @rest_action
            def method_view(self):
                return 'ClassBasedView.method_view'

        request = testing.DummyRequest()
        context = testing.DummyResource()

        self.assertEqual(
            view_with_request_only(request),
            'view_with_request_only')
        self.assertEqual(
            view_with_context_and_request(context, request),
            'view_with_context_and_request')


        class_view = ClassBasedView(context, request)
        self.assertEqual(
            class_view.method_view(),
            'ClassBasedView.method_view',
        )

    def test_add_error_adapters(self):
        @rest_action
        def view_with_error(request):
            raise MyError('abc')

        class MyError(Exception):
            pass

        @rest_error_adapter(MyError)
        def my_error_adapter(e):
            return e.message

        def my_error_adapter2(e):
            return 'he he he'

        self.assertRaises(ValueError, register_error_adapter, MyError, my_error_adapter)

        adapters = [ea.error_cls for ea in rest_action.__registered_error_adapters__]
        print adapters
        for i in range(0, len(adapters)-2):
            for j in range(i+1, len(adapters)-1):
                u = adapters[i]
                v = adapters[j]
                print '--'
                print u
                print v
                self.assertFalse(issubclass(v, u))

        request = testing.DummyRequest()

        self.assertEqual(view_with_error(request), 'abc')
