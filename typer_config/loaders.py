"""
Configuration File Loaders.

These loaders must follow the signature: Callable[[Any], Dict[str, Any]]
"""

import json
from typing import Any, Dict

USING_TOMLLIB = False

try:
    # Only available for python>=3.11
    import tomllib as toml

    USING_TOMLLIB = True
except ImportError:
    try:
        # Third-party toml parsing library
        import toml
    except ImportError:
        toml = None

try:
    import yaml
except ImportError:
    yaml = None


# pylint: disable-next=unused-argument
def dummy_loader(path: str) -> Dict[str, Any]:
    """Dummy loader to show the required interface.

    Parameters
    ----------
    path : str
        path of file to load

    Returns
    -------
    Dict
        dictionary loaded from file
    """
    return {}


def yaml_loader(path: str) -> Dict[str, Any]:
    """YAML file loader

    Parameters
    ----------
    path : str
        path of YAML file

    Returns
    -------
    Dict
        dictionary loaded from file
    """

    with open(path, "r", encoding="utf-8") as _file:
        conf = yaml.safe_load(_file)

    return conf


def json_loader(path: str) -> Dict[str, Any]:
    """JSON file loader

    Parameters
    ----------
    path : str
        path of JSON file

    Returns
    -------
    Dict
        dictionary loaded from file
    """

    with open(path, "r", encoding="utf-8") as _file:
        conf = json.load(_file)

    return conf


def toml_loader(path: str) -> Dict[str, Any]:
    """TOML file loader

    Parameters
    ----------
    path : str
        path of TOML file

    Returns
    -------
    Dict
        dictionary loaded from file
    """

    if USING_TOMLLIB:
        with open(path, "rb") as _file:
            conf = toml.load(_file)
    else:
        with open(path, "r", encoding="utf-8") as _file:
            conf = toml.load(_file)

    return conf
