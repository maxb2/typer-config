"""Handle optional imports."""

from functools import lru_cache
from importlib import import_module
from importlib.util import find_spec


@lru_cache()
def try_import(module_name: str):
    """Try to import a module by name.

    Note: caches the imported modules in a `functools.lru_cache`

    Args:
        pkg_name (str): name of module to import

    Returns:
        Module: imported module
    """
    if find_spec(module_name):
        return import_module(module_name)
    return None


# REMOVE THIS
# just want to check CodeCov
if try_import("sdlfjksldfkj"):
    print("doing nothing")
