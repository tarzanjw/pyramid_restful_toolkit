__author__ = 'tarzan'

import importlib

from pyramid_restful_toolkit.auth.auth_policy import AuthPolicy


def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    get_user_callback_path = config.registry.settings[
        "pyramid_restful_toolkit.auth.get_user_callback"]
    module_name, attr_name = get_user_callback_path.rsplit('.', 1)
    module = importlib.import_module(module_name, package=None)
    get_user_callback = getattr(module, attr_name)

    auth = AuthPolicy(get_user_callback=get_user_callback)
    config.set_authentication_policy(auth)
    config.add_forbidden_view(auth.forbidden)
