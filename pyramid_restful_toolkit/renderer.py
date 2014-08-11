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
    >>> try:
    ...     from cqlengine.models import Model
    ...     from cqlengine import columns
    ...     class TestModel(Model):
    ...         id = columns.Integer(primary_key=True)
    ...         set_col = columns.Set(columns.Integer)
    ...     m = TestModel(id=1234, set_col={1, 2, 3, 4})
    ... except ImportError:
    ...     class TestModel(dict):
    ...         def _as_dict(self):
    ...             return self
    ...     m = TestModel(id=1234, set_col={1, 2, 3, 4})
    >>>
    >>> renderer(m._as_dict(), {})
    '{"set_col": [1, 2, 3, 4], "id": 1234}'
    >>> renderer(m, {})
    '{"set_col": [1, 2, 3, 4], "id": 1234}'
    """
    r = pyramid.renderers.JSON()

    r.add_adapter(set, lambda obj, request: list(obj))
    r.add_adapter(datetime, lambda obj, request: obj.isoformat())

    try:
        import cqlengine.columns
        import cqlengine.models
        r.add_adapter(cqlengine.models.Model,
                      lambda obj, request: obj._as_dict())
        r.add_adapter(cqlengine.columns.ValueQuoter,
                      lambda obj, request: obj.value)
    except ImportError:
        pass

    return r


default_renderer = create_json_renderer()