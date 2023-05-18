"""
Configuration File Loaders.

These loaders must implement the `typer_config.__typing.ConfigLoader` interface.
"""
import json
import sys
from configparser import ConfigParser

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

    Examples:
        The following example reads the values from the `my_app` section in
        a YAML file structured like this:
        ```yaml
        tools:
            my_app:
                ... # use these values
            others: # ignore
        stuf: # ignore
        ```

        ```py
        my_loader = subpath_loader(yaml_loader, ["tools", "my_app"])
        ```

    Args:
        loader (ConfigLoader): loader to modify
        dictpath (ConfigDictAccessorPath): path to the section of dictionary

    Returns:
        ConfigLoader: sub dictionary loader
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
    """Modify a loader to use a default value if the passed value is false-ish.

    Examples:
        The following example lets a user specify a config file, but will load
        the `pyproject.toml` if they don't.

        ```py
        pyproject_loader = default_value_loader(toml_loader, lambda: "pyproject.toml")
        ```

    Args:
        loader (ConfigLoader): loader to modify
        value_getter (NoArgCallable): function that returns default value

    Returns:
        ConfigLoader: modified loader
    """

    def _loader(param_value: str) -> ConfigDict:
        # parameter value was not specified by user
        if not param_value:
            param_value = value_getter()

        conf: ConfigDict = loader(param_value)

        return conf

    return _loader


def yaml_loader(param_value: TyperParameterValue) -> ConfigDict:
    """YAML file loader.

    Args:
        param_value (TyperParameterValue): path of YAML file

    Raises:
        ModuleNotFoundError: pyyaml library is not installed

    Returns:
        ConfigDict: dictionary loaded from file
    """

    if YAML_MISSING:  # pragma: no cover
        raise ModuleNotFoundError("Please install the pyyaml library.")

    with open(param_value, "r", encoding="utf-8") as _file:
        conf: ConfigDict = yaml.safe_load(_file)

    return conf


def json_loader(param_value: TyperParameterValue) -> ConfigDict:
    """JSON file loader.

    Args:
        param_value (TyperParameterValue): path of JSON file

    Returns:
        ConfigDict: dictionary loaded from file
    """

    with open(param_value, "r", encoding="utf-8") as _file:
        conf: ConfigDict = json.load(_file)

    return conf


def toml_loader(param_value: TyperParameterValue) -> ConfigDict:
    """TOML file loader.

    Args:
        param_value (TyperParameterValue): path of TOML file

    Raises:
        ModuleNotFoundError: toml library is not installed

    Returns:
        ConfigDict: dictionary loaded from file
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
    """Dotenv file loader.

    Args:
        param_value (TyperParameterValue): path of Dotenv file

    Raises:
        ModuleNotFoundError: python-dotenv library is not installed

    Returns:
        ConfigDict: dictionary loaded from file
    """

    if DOTENV_MISSING:  # pragma: no cover
        raise ModuleNotFoundError("Please install the python-dotenv library.")

    with open(param_value, "r", encoding="utf-8") as _file:
        # NOTE: I'm using a stream here so that the loader
        # will raise an exception when the file doesn't exist.
        conf: ConfigDict = dotenv.dotenv_values(stream=_file)

    return conf


def ini_loader(param_value: TyperParameterValue) -> ConfigDict:
    """INI file loader

    Note:
        INI files must have sections at the top level.
        You probably want to combine this with `subpath_loader`.
        For example:
        ```py
        ini_section_loader = subpath_loader(ini_loader, ["section"])
        ```

    Args:
        param_value (TyperParameterValue): path of INI file

    Returns:
        ConfigDict: dictionary loaded from file
    """

    ini_parser = ConfigParser()
    with open(param_value, "r", encoding="utf-8") as _file:
        ini_parser.read_file(_file)

    conf: ConfigDict = {
        sect: dict(ini_parser.items(sect)) for sect in ini_parser.sections()
    }

    return conf
