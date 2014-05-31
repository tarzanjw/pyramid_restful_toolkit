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


from .tweens import jsonize_uncaught_exception_tween_factory
from .renderer import default_renderer


def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    config.add_renderer(None, default_renderer)
    config.add_renderer('json', default_renderer)
    config.include(__name__ + '.error_handlers')