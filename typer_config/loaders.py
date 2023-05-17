"""
Configuration File Loaders.

These loaders must implement the `typer_config.__typing.ConfigLoader` interface.
"""
import json
import sys

from .__typing import (
    ConfigDict,
    ConfigDictAccessorPath,
    ConfigLoader,
    NoArgCallable,
    TyperParameterValue,
)

USING_TOMLLIB = False
TOML_MISSING = True
YAML_MISSING = True
DOTENV_MISSING = True


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

try:  # pragma: no cover
    import dotenv

    DOTENV_MISSING = False
except ImportError:  # pragma: no cover
    pass


def subpath_loader(
    loader: ConfigLoader, dictpath: ConfigDictAccessorPath
) -> ConfigLoader:
    """Modify a loader to return a subpath of the dictionary from file.

    Parameters
    ----------
    loader : ConfigLoader
        loader to modify
    dictpath : ConfigDictAccessorPath
        path to the section of the dictionary to return

    Returns
    -------
    ConfigLoader
        sub dictionary loader
    """

    def _loader(param_value: str) -> ConfigDict:
        # get original ConfigDict
        conf: ConfigDict = loader(param_value)

        # get subpath of dictionary
        for path in dictpath:
            conf = conf.get(path, {})
        return conf

    return _loader


def default_value_loader(
    loader: ConfigLoader, value_getter: NoArgCallable
) -> ConfigLoader:
    """Modify a loader to use a default value if the passed value is false-ish

    Parameters
    ----------
    loader : ConfigLoader
        loader to modify
    value_getter : NoArgCallable
        function that returns default value

    Returns
    -------
    ConfigLoader
        modified loader
    """

    def _loader(param_value: str) -> ConfigDict:
        # parameter value was not specified by user
        if not param_value:
            param_value = value_getter()

        conf: ConfigDict = loader(param_value)

        return conf

    return _loader


def yaml_loader(param_value: TyperParameterValue) -> ConfigDict:
    """YAML file loader

    Parameters
    ----------
    param_value : TyperParameterValue
        path of YAML file

    Returns
    -------
    ConfigDict
        dictionary loaded from file
    """

    if YAML_MISSING:  # pragma: no cover
        raise ModuleNotFoundError("Please install the pyyaml library.")

    with open(param_value, "r", encoding="utf-8") as _file:
        conf: ConfigDict = yaml.safe_load(_file)

    return conf


def json_loader(param_value: TyperParameterValue) -> ConfigDict:
    """JSON file loader

    Parameters
    ----------
    param_value : TyperParameterValue
        path of JSON file

    Returns
    -------
    ConfigDict
        dictionary loaded from file
    """

    with open(param_value, "r", encoding="utf-8") as _file:
        conf: ConfigDict = json.load(_file)

    return conf


def toml_loader(param_value: TyperParameterValue) -> ConfigDict:
    """TOML file loader

    Parameters
    ----------
    param_value : TyperParameterValue
        path of TOML file

    Returns
    -------
    ConfigDict
        dictionary loaded from file
    """

    if TOML_MISSING:  # pragma: no cover
        raise ModuleNotFoundError("Please install the toml library.")

    conf: ConfigDict = {}

    if USING_TOMLLIB:  # pragma: no cover
        with open(param_value, "rb") as _file:
            conf = tomllib.load(_file)  # type: ignore
    else:  # pragma: no cover
        with open(param_value, "r", encoding="utf-8") as _file:
            conf = toml.load(_file)  # type: ignore

    return conf


def dotenv_loader(param_value: TyperParameterValue) -> ConfigDict:
    """Dotenv file loader

    Parameters
    ----------
    param_value : TyperParameterValue
        path of YAML file

    Returns
    -------
    ConfigDict
        dictionary loaded from file
    """

    if DOTENV_MISSING:  # pragma: no cover
        raise ModuleNotFoundError("Please install the python-dotenv library.")

    with open(param_value, "r", encoding="utf-8") as _file:
        # NOTE: I'm using a stream here so that the loader
        # will raise an exception when the file doesn't exist.
        conf: ConfigDict = dotenv.dotenv_values(stream=_file)

    return conf
