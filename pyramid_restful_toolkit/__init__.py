__author__ = 'tarzan'
from datetime import datetime


class ErrorResponse(Exception):
    def __init__(self, code, errors=None, data=None):
        self.code = code
        self.errors = errors or {}
        self.data = data or {}
        self.message = '%d: %s %s' % (code, errors, data)

    def response(self, request):
        request.response.status_code = self.code
        data = {'data': self.data} if self.data else {}
        data['error_code'] = self.code
        data['errors'] = self.errors
        return data


from decorator import rest_action


def on_error_response_exception(context, request):
    """
    :type context: ErrorResponse
    """
    return context.response(request)


def jsonize_uncaught_exception_tween_factory(handler, registry):
    """
    This tween prevent all uncaught exception and return JSON response with error code 500
    """
    def jsonize_uncaught_exception_tween(request):
        """
        :type request: pyramid.request.Request
        :rtype : pyramid.response.Response
        """
        try:
            return handler(request)
        except BaseException, e:
            import json
            from pyramid import response

            body = json.dumps({
                'error': e.__class__.__name__,
                'code': 500,
                'status': '500 Internal Server Error',
                'message': e.message,
            })
            return response.Response(
                body=body,
                status='500 Internal Server Error',
                content_type='application/json',
            )

    return jsonize_uncaught_exception_tween


def create_pyramid_json_renderer():
    """
    Create a JSON renderer most of common datatype
    :rtype : pyramid.renderers.JSON
    """
    from pyramid import renderers
    r = renderers.JSON()

    r.add_adapter(set, lambda obj, request: list(obj))
    r.add_adapter(datetime, lambda obj, request: obj.isoformat())

    return r


def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    config.add_renderer(None, create_pyramid_json_renderer())
    config.add_view(on_error_response_exception, context=ErrorResponse)
    if not config.registry.settings.get('pyramid_restful_toolkit.dev_mode', False):
        config.add_tween('pyramid_restful_toolkit.jsonize_uncaught_exception_tween_factory')
