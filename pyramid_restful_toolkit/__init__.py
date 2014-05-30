__author__ = 'tarzan'


class ErrorResponse(Exception):
    def __init__(self, code, errors=None, data=None):
        self.code = code
        self.errors = errors or {}
        self.data = data or {}

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


def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    config.add_view(on_error_response_exception, context=ErrorResponse, renderer='json')