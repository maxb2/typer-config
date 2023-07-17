"""
Configuration File Loaders.

These loaders must implement the `typer_config.__typing.ConfigLoader` interface.
"""
import json
from configparser import ConfigParser
from typing import Optional
from warnings import warn

from .__optional_imports import *  # pylint: disable=wildcard-import, unused-wildcard-import
from .__typing import (
    ConfigDict,
    ConfigDictAccessorPath,
    ConfigDictTransformer,
    ConfigLoader,
    ConfigLoaderConditional,
    NoArgCallable,
    TyperParameterValue,
    TyperParameterValueTransformer,
)


def loader_transformer(
    loader: ConfigLoader,
    loader_conditional: Optional[ConfigLoaderConditional] = None,
    param_transformer: Optional[TyperParameterValueTransformer] = None,
    config_transformer: Optional[ConfigDictTransformer] = None,
) -> ConfigLoader:
    """Configuration loader transformer.

    This allows to transform the input and output of a configuration loader.

    Examples:
        Set a default file to open when none is given:
        ```py
        default_file_loader = loader_transformer(
            yaml_loader,
            param_transformer=lambda param: param if param else "config.yml",
        )
        ```

        Use a subsection of a file:
        ```py
        subsection_loader = loader_transformer(
            yaml_loader,
            config_transformer = lambda config: config["subsection"],
        )
        ```

        Use both transformers to use the `[tool.my_tool]` section from `pyproject.toml`
        by default:
        ```py
        pyproject_loader = loader_transformer(
            toml_loader,
            param_transformer = lambda param: param if param else "pyproject.toml"
            config_transformer = lambda config: config["tool"]["my_tool"],
        )
        ```

    Args:
        loader (ConfigLoader): Loader to transform.
        loader_conditional (Optional[ConfigLoaderConditional], optional): Function
            to determine whether to execute loader. Defaults to None (no-op).
        param_transformer (Optional[TyperParameterValueTransformer], optional): Typer
            parameter transformer. Defaults to None (no-op).
        config_transformer (Optional[ConfigDictTransformer], optional): Config
            dictionary transformer. Defaults to None (no-op).

    Returns:
        ConfigLoader: Transformed config loader.
    """

    def _loader(param_value: TyperParameterValue) -> ConfigDict:
        # Transform input
        if param_transformer is not None:
            param_value = param_transformer(param_value)

        # Decide whether to execute loader
        # NOTE: bad things can happen when `param_value=''`
        # such as `--help` not working
        conf: ConfigDict = {}
        if loader_conditional is None or loader_conditional(param_value):
            conf = loader(param_value)

        # Transform output
        if config_transformer is not None:
            conf = config_transformer(conf)

        return conf

    return _loader


def subpath_loader(
    loader: ConfigLoader, dictpath: ConfigDictAccessorPath
) -> ConfigLoader:
    """Modify a loader to return a subpath of the dictionary from file.

    Warns:
        DeprecationWarning: This function is deprecated. Please use
            typer_config.loaders.loader_transformer instead.

    Examples:
        The following example reads the values from the `my_app` section in
        a YAML file structured like this:
        ```yaml
        tools:
            my_app:
                ... # use these values
            others: # ignore
        stuff: # ignore
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

    warn(
        "typer_config.loaders.subpath_loader is deprecated. "
        "Please use typer_config.loaders.loader_transformer instead.",
        DeprecationWarning,
    )

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

    Warns:
        DeprecationWarning: This function is deprecated. Please use
            typer_config.loaders.loader_transformer instead.

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

    warn(
        "typer_config.loaders.default_value_loader is deprecated. "
        "Please use typer_config.loaders.loader_transformer instead.",
        DeprecationWarning,
    )

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

    if USING_TOMLLIB:  # pragma: no cover
        with open(param_value, "rb") as _file:
            return tomllib.load(_file)  # type: ignore

    if TOML_MISSING:  # pragma: no cover
        raise ModuleNotFoundError("Please install the toml library.")
    with open(param_value, "r", encoding="utf-8") as _file:  # pragma: no cover
        return toml.load(_file)  # type: ignore


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
