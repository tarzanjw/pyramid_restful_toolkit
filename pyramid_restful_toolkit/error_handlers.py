__author__ = 'tarzan'

from . import ErrorResponse


def _make_error_response(status_code, errors=None, data=None):
    data = {'data': data} if data else {}
    data['error_code'] = status_code
    data['errors'] = errors or {}
    return data


def on_schema_error(context, request):
    """
    :type context: _SchemaError
    :type request: pyramid.request.Request
    """
    request.response.status_code = 400
    return _make_error_response(400, context.autos)


def on_colander_invalid(context, request):
    """
    :type context: colander.Invalid
    :type request: pyramid.request.Request
    """
    request.response.status_code = 400
    return _make_error_response(400, context.asdict())


def on_formencode_invalid(context, request):
    """
    :type context: formencode.Invalid
    :type request: pyramid.request.Request
    """
    request.response.status_code = 400
    return _make_error_response(400, context.unpack_errors())


def on_error_response(context, request):
    """
    :type context: ErrorResponse
    """
    return context.response(request)


def on_deform_validation_failure(context, request):
    """
    :type context: deform.ValidationFailure
    """
    request.response.status_code = 400
    return _make_error_response(400, context.error.asdict())


def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    try:
        import formencode
        config.add_view(on_formencode_invalid, context=formencode.Invalid)
    except ImportError:
        pass

    try:
        import colander
        config.add_view(on_colander_invalid, context=colander.Invalid)
    except ImportError:
        pass

    try:
        import schema
        config.add_view(on_schema_error, context=schema.SchemaError)
    except ImportError as e:
        pass

    try:
        import deform
        config.add_view(on_deform_validation_failure,
                        context=deform.ValidationFailure)
    except ImportError as e:
        pass

    config.add_view(on_error_response, context=ErrorResponse)