=========================
 pyramid_restful_toolkit
=========================


A toolkit for RESTful API development in Pyramid.

That includes:

1. JSON renderer
2. HTTP Auth Policy (Basic, Digest)
3. Some utilities to work with SQLAlchemy, CQLEngine

-----
 API
-----

To use it, just

.. code-block::python

    config.include('pyramid_restful_toolkit')

This will do those jobs:

    1. Add JSON as default renderer with some default adapters. You can access
       it through `pyramid_restful_toolkit.default_renderer`
    2. Add some error handlers for common validators library such as: formencode,
       colander, schema.

If you want all uncaught exception has return as JSON text. Just include tween
`pyramid_restful_toolkit.jsonize_uncaught_exception_tween_factory`. This is
normally used in production.ini.


HTTP Auth Policy
################

To use this package, in the app function, just include it.

    config.include("pyramid_restful_toolkit.auth")

In you *development.ini*

    pyramid_restful_toolkit.auth.get_user_callback = 'path to get user function'

You can use built-in model:

**For SQLAlchemy**

    config.include("pyramid_restful_toolkit.auth.models.sqlalchemy")

with *development.ini*

    pyramid_restful_toolkit.auth.dbsession = app.models.DBSession

Use *pyramid_restful_toolkit.auth.models.sqlalchemy.RESTfulUser* to manage your users. Its table
name is *rest_user*.


-----------
CHANGES LOG
-----------

1.1.1
=====

* Add default renderer for datetime.date

1.1.0
=====

* Add python 3 support
* Remove auth, move to `pyramid_httpauth (https://github.com/tarzanjw/pyramid_httpauth)`_

1.0.3
=====

* Add default JSON renderer for cqlengine.columns.ValueQuoter, cqlengine.model.Model

1.0.2
=====

* Add default error handler support for deform.ValidationFailure