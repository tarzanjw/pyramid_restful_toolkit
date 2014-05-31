__author__ = 'tarzan'

from datetime import datetime
import pyramid.renderers


def create_json_renderer():
    """
    Create a JSON renderer most of common datatype
    :rtype : pyramid.renderers.JSON
    """
    r = pyramid.renderers.JSON()

    r.add_adapter(set, lambda obj, request: list(obj))
    r.add_adapter(datetime, lambda obj, request: obj.isoformat())

    return r


default_renderer = create_json_renderer()