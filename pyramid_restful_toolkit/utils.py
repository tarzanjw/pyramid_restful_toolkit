__author__ = 'tarzan'


def is_sqlalchemy_column(col):
    try:
        from sqlalchemy.orm.attributes import InstrumentedAttribute
        from sqlalchemy.orm.properties import ColumnProperty

        return \
            isinstance(col, InstrumentedAttribute) \
            and \
            isinstance(col.property, ColumnProperty)
    except ImportError as e:
        return False


def sqlalchemy_obj_to_dict(obj):
    """
    Return a dict from a sqlalchemy object
    :param object obj: object that contains source information
    :return: data from object
    :rtype : dict
    """
    cls = obj.__class__
    data = {a: obj.__getattribute__(a) for a, c in cls.__dict__.items()
            if is_sqlalchemy_column(c)}
    return data