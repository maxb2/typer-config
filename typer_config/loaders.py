"""
Configuration File Loaders.

These loaders must implement the interface:
    typer_config.types.Loader = Callable[[Any], Dict[str, Any]]
"""
import json
import sys

from ._typing import ConfDict, Loader, ConfDictPath, ValueGetter

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


def subpath_loader(loader: Loader, dictpath: ConfDictPath) -> Loader:
    """Modify a loader to return a subpath of the dictionary from file.

    Parameters
    ----------
    loader : Loader
        loader to modify
    dictpath : ConfDictPath
        path to the section of the dictionary to return

    Returns
    -------
    Loader
        sub dictionary loader
    """

    def _loader(param_value: str) -> ConfDict:
        # get original ConfDict
        conf: ConfDict = loader(param_value)

        # get subpath of dictionary
        for path in dictpath:
            conf = conf.get(path, {})
        return conf

    return _loader


def default_value_loader(loader: Loader, value_getter: ValueGetter) -> Loader:
    """Modify a loader to use a default value if the passed value is false-ish

    Parameters
    ----------
    loader : Loader
        loader to modify
    value_getter : ValueGetter
        function that returns default value

    Returns
    -------
    Loader
        modified loader
    """

    def _loader(param_value: str) -> ConfDict:
        # parameter value was not specified by user
        if not param_value:
            param_value = value_getter()

        conf: ConfDict = loader(param_value)

        return conf

    return _loader


def yaml_loader(param_value: str) -> ConfDict:
    """YAML file loader

    Parameters
    ----------
    param_value : str
        path of YAML file

    Returns
    -------
    ConfDict
        dictionary loaded from file
    """

    if YAML_MISSING:
        raise ModuleNotFoundError("Please install the pyyaml library.")

    with open(param_value, "r", encoding="utf-8") as _file:
        conf: ConfDict = yaml.safe_load(_file)

    return conf


def json_loader(param_value: str) -> ConfDict:
    """JSON file loader

    Parameters
    ----------
    param_value : str
        path of JSON file

    Returns
    -------
    ConfDict
        dictionary loaded from file
    """

    with open(param_value, "r", encoding="utf-8") as _file:
        conf: ConfDict = json.load(_file)

    return conf


def toml_loader(param_value: str) -> ConfDict:
    """TOML file loader

    Parameters
    ----------
    param_value : str
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
        with open(param_value, "rb") as _file:
            conf = tomllib.load(_file)  # type: ignore
    else:
        with open(param_value, "r", encoding="utf-8") as _file:
            conf = toml.load(_file)  # type: ignore

    return conf
