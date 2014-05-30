=========================
 pyramid_restful_toolkit
=========================


A toolkit for RESTful API development in Pyramid.

That includes:

1. JSON renderer
2. rest_action decorator
3. HTTP Auth Policy (Basic, Digest)

-----
 API
-----

  Under construction.

Sorry, I have no time for this.

rest_action decorator
#####################


```python

    @rest_action
    def view_function(request)
        return {}
```

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
