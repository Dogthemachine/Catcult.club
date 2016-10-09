def get_django_env():
    """
    Set proper environment for settings import.

    Default environments: `dev`, `prod`, `test`.
    They could be extended if needed.

    """
    from os import environ

    try:
        env = environ['TC_DJANGO_SETTINGS_MODULE']
    except KeyError:
        env = 'three_cats.settings.prod'

    return env

exec("from %s import *" % get_django_env())
