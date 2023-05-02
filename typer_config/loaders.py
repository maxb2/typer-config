"""
Configuration File Loaders.

These loaders must implement the interface:
    typer_config.types.Loader = Callable[[Any], Dict[str, Any]]
"""
import json
import sys

from ._typing import ConfDict

USING_TOMLLIB = False
TOML_MISSING = True
YAML_MISSING = True


if sys.version_info >= (3, 11):
    import tomllib  # type: ignore

    TOML_MISSING = False
    USING_TOMLLIB = True
else:
    try:
        # Third-party toml parsing library
        import toml

        TOML_MISSING = False

    except ImportError:
        pass


try:
    import yaml

    YAML_MISSING = False
except ImportError:
    pass


# pylint: disable-next=unused-argument
def dummy_loader(path: str) -> ConfDict:
    """Dummy loader to show the required interface.

    Parameters
    ----------
    path : str
        path of file to load

    Returns
    -------
    ConfDict
        dictionary loaded from file
    """
    return {}


def yaml_loader(path: str) -> ConfDict:
    """YAML file loader

    Parameters
    ----------
    path : str
        path of YAML file

    Returns
    -------
    ConfDict
        dictionary loaded from file
    """

    if YAML_MISSING:
        raise ModuleNotFoundError("Please install the pyyaml library.")

    with open(path, "r", encoding="utf-8") as _file:
        conf: ConfDict = yaml.safe_load(_file)

    return conf


def json_loader(path: str) -> ConfDict:
    """JSON file loader

    Parameters
    ----------
    path : str
        path of JSON file

    Returns
    -------
    ConfDict
        dictionary loaded from file
    """

    with open(path, "r", encoding="utf-8") as _file:
        conf: ConfDict = json.load(_file)

    return conf


def toml_loader(path: str) -> ConfDict:
    """TOML file loader

    Parameters
    ----------
    path : str
        path of TOML file

    Returns
    -------
    ConfDict
        dictionary loaded from file
    """

    if TOML_MISSING:
        raise ModuleNotFoundError("Please install the toml library.")

    conf: ConfDict = {}

    if USING_TOMLLIB:
        with open(path, "rb") as _file:
            conf = tomllib.load(_file)  # type: ignore
    else:
        with open(path, "r", encoding="utf-8") as _file:
            conf = toml.load(_file)  # type: ignore

    return conf
