__author__ = 'tarzan'

from datetime import datetime
import pyramid.renderers


def create_json_renderer():
    """
    Create a JSON renderer most of common datatype
    :rtype : pyramid.renderers.JSON

    >>> from datetime import datetime
    >>> renderer = create_json_renderer()
    >>> renderer = renderer(None)
    >>> renderer('abc', {})
    '"abc"'
    >>> renderer({1, 2, 3, 4}, {})
    '[1, 2, 3, 4]'
    >>> renderer(datetime.utcfromtimestamp(0), {})
    '"1970-01-01T00:00:00"'
    """
    r = pyramid.renderers.JSON()

    r.add_adapter(set, lambda obj, request: list(obj))
    r.add_adapter(datetime, lambda obj, request: obj.isoformat())

    return r


default_renderer = create_json_renderer()