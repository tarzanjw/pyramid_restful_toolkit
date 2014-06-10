from __future__ import absolute_import
__author__ = 'tarzan'

import importlib
from sqlalchemy import Column, types, Table, MetaData
from sqlalchemy.orm import mapper
from datetime import datetime

Base = None
DBSession = None

meta = MetaData()


def setup_database(session):
    global DBSession
    DBSession = session


_user_table = Table("rest_user", meta,
                    Column("id", types.Integer, primary_key=True,
                           autoincrement=True),
                    Column("username", types.VARCHAR(length=64),
                           unique=True, nullable=False),
                    Column("password", types.VARCHAR(length=64),
                           nullable=False),
                    Column("desc", types.TEXT),
                    Column("groups", types.TEXT),
                    Column("enabled", types.BOOLEAN,
                           default=True),
                    Column("last_modified_time", types.DateTime,
                           nullable=False,
                           default=datetime.now, onupdate=datetime.now)
)


class RESTfulUser(object):
    def __init__(self, **kwargs):
        self.id = None
        self.username = None
        self.password = None
        self.desc = None
        self.groups = None
        self.enabled = None
        self.last_modified_time = None
        self.__dict__.update(kwargs)

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.__unicode__().encode('utf-8')


mapper(RESTfulUser, _user_table)


def get_rest_user(username):
    user = DBSession.query(RESTfulUser).filter(
        RESTfulUser.username == username,
        RESTfulUser.enabled).first()
    if user is not None:
        return {
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'roles': user.groups,
        }
    return None


def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    dbsession_path = config.registry.settings["pyramid_restful_toolkit.auth.dbsession"]
    module_name, attr_name = dbsession_path.rsplit('.', 1)
    module = importlib.import_module(module_name, package=None)
    dbsession = getattr(module, attr_name)
    setup_database(dbsession)

    config.registry.settings['pyramid_restful_toolkit.auth.get_user_callback'] = \
        'pyramid_restful_toolkit.auth.models.sqlalchemy.get_rest_user'


"""Try to automatically declare backend schema
if pyramid_backend has installed"""
try:
    import pyramid_backend
    import colander
    from deform import widget

    class RESTfulUserSchema(colander.MappingSchema):
        username = colander.SchemaNode(colander.String())
        password = colander.SchemaNode(colander.String())
        enabled = colander.SchemaNode(colander.Boolean())
        groups = colander.SchemaNode(colander.String(), missing=colander.null)
        desc = colander.SchemaNode(colander.String(), missing=colander.null)

    RESTfulUser.__backend_schema_cls__ = RESTfulUserSchema

except ImportError:
        pass
