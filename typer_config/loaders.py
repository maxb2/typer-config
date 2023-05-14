"""
Configuration File Loaders.

These loaders must implement the interface:
    typer_config.types.ConfLoader = Callable[[Any], Dict[str, Any]]
"""
import json
import sys

from ._typing import (
    ConfDict,
    ConfLoader,
    ConfDictAccessorPath,
    NoArgCallable,
    TyperParameterValue,
)

USING_TOMLLIB = False
TOML_MISSING = True
YAML_MISSING = True


if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib  # type: ignore

    TOML_MISSING = False
    USING_TOMLLIB = True
else:  # pragma: no cover
    try:
        # Third-party toml parsing library
        import toml

        TOML_MISSING = False

    except ImportError:
        pass


try:  # pragma: no cover
    import yaml

    YAML_MISSING = False
except ImportError:  # pragma: no cover
    pass


def subpath_loader(loader: ConfLoader, dictpath: ConfDictAccessorPath) -> ConfLoader:
    """Modify a loader to return a subpath of the dictionary from file.

    Parameters
    ----------
    loader : ConfLoader
        loader to modify
    dictpath : ConfDictPath
        path to the section of the dictionary to return

    Returns
    -------
    ConfLoader
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


def default_value_loader(loader: ConfLoader, value_getter: NoArgCallable) -> ConfLoader:
    """Modify a loader to use a default value if the passed value is false-ish

    Parameters
    ----------
    loader : ConfLoader
        loader to modify
    value_getter : NoArgCallable
        function that returns default value

    Returns
    -------
    ConfLoader
        modified loader
    """

    def _loader(param_value: str) -> ConfDict:
        # parameter value was not specified by user
        if not param_value:
            param_value = value_getter()

        conf: ConfDict = loader(param_value)

        return conf

    return _loader


def yaml_loader(param_value: TyperParameterValue) -> ConfDict:
    """YAML file loader

    Parameters
    ----------
    param_value : TyperParameterValue
        path of YAML file

    Returns
    -------
    ConfDict
        dictionary loaded from file
    """

    if YAML_MISSING:  # pragma: no cover
        raise ModuleNotFoundError("Please install the pyyaml library.")

    with open(param_value, "r", encoding="utf-8") as _file:
        conf: ConfDict = yaml.safe_load(_file)

    return conf


def json_loader(param_value: TyperParameterValue) -> ConfDict:
    """JSON file loader

    Parameters
    ----------
    param_value : TyperParameterValue
        path of JSON file

    Returns
    -------
    ConfDict
        dictionary loaded from file
    """

    with open(param_value, "r", encoding="utf-8") as _file:
        conf: ConfDict = json.load(_file)

    return conf


def toml_loader(param_value: TyperParameterValue) -> ConfDict:
    """TOML file loader

    Parameters
    ----------
    param_value : TyperParameterValue
        path of TOML file

    Returns
    -------
    ConfDict
        dictionary loaded from file
    """

    if TOML_MISSING:  # pragma: no cover
        raise ModuleNotFoundError("Please install the toml library.")

    conf: ConfDict = {}

    if USING_TOMLLIB:  # pragma: no cover
        with open(param_value, "rb") as _file:
            conf = tomllib.load(_file)  # type: ignore
    else:  # pragma: no cover
        with open(param_value, "r", encoding="utf-8") as _file:
            conf = toml.load(_file)  # type: ignore

    return conf
