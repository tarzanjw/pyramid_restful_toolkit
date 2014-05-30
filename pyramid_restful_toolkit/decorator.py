__author__ = 'tarzan'

import inspect
from collections import namedtuple
from . import ErrorResponse

_ErrorAdapter = namedtuple('_ErrorAdapter', ['error_cls', 'adapter'])


def rest_action(view_func):
    def view_wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except ErrorResponse, e:
            raise
        except Exception, e:
            for error_cls, adapter in rest_action.__registered_error_adapters__:
                if isinstance(e, error_cls):
                    return adapter(e)
            raise e

    view_wrapper.__doc__ = view_func.__doc__
    view_wrapper.__name__ = view_func.__name__
    return view_wrapper


rest_action.__registered_error_adapters__ = []
""":type : list[_ErrorAdapter]"""


def register_error_adapter(error_cls, adapter):
    assert inspect.isclass(error_cls)

    adapters = rest_action.__registered_error_adapters__
    ea = _ErrorAdapter(error_cls, adapter)

    ii = 0
    for i in reversed(range(0, len(adapters) - 1)):
        u = adapters[i]
        if u.error_cls is ea.error_cls:
            raise ValueError(
                "RestErrorAdapter conflicting: 2 adapters %s and %s for error class %s" \
                % (u.adapter, ea.adapter, u.error_cls)
            )
        if issubclass(u.error_cls, ea.error_cls):
            ii = i
            break
    adapters.insert(ii, ea)


def rest_error_adapter(error_cls):
    assert inspect.isclass(error_cls)

    def decorator(adapter):
        register_error_adapter(error_cls, adapter)
        return adapter

    return decorator


try:
    from formencode import Invalid as _FormEncodeInvalid
except ImportError:
    class _FormEncodeInvalid(BaseException):
        def unpack_errors(self):
            return []


@rest_error_adapter(_FormEncodeInvalid)
def _formencode_invalid_adapter(e):
    raise ErrorResponse(400, e.unpack_errors())


try:
    from schema import SchemaError as _SchemaError
except ImportError:
    class _SchemaError(Exception):
        autos = []


@rest_error_adapter(_SchemaError)
def _schemaerror_adapter(e):
    raise ErrorResponse(400, e.autos)


try:
    from colander import Invalid as _ColanderInvalid
except ImportError:
    class _ColanderInvalid(object):
        def asdict(self):
            return []


@rest_error_adapter(_ColanderInvalid)
def _colanderinvalid_adapter(e):
    raise ErrorResponse(400, e.asdict())
