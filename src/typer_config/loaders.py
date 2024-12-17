"""Configuration File Loaders.

These loaders must implement the `typer_config.__typing.ConfigLoader` interface.
"""

from __future__ import annotations

import json
from configparser import ConfigParser
from typing import TYPE_CHECKING, Optional

from .__optional_imports import try_import

if TYPE_CHECKING:  # pragma: no cover
    from .__typing import (
        ConfigDict,
        ConfigDictTransformer,
        ConfigLoader,
        ConfigLoaderConditional,
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


def yaml_loader(param_value: TyperParameterValue) -> ConfigDict:
    """YAML file loader.

    Args:
        param_value (TyperParameterValue): path of YAML file

    Raises:
        ModuleNotFoundError: pyyaml library is not installed

    Returns:
        ConfigDict: dictionary loaded from file
    """

    yaml = try_import("yaml")

    if yaml is None:  # pragma: no cover
        message = "Please install the pyyaml library."
        raise ModuleNotFoundError(message)

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

    # try `tomllib` first
    tomllib = try_import("tomllib")

    if tomllib is not None:
        with open(param_value, "rb") as _file:
            return tomllib.load(_file)

    # couldn't find `tommllib`, so try `toml`
    toml = try_import("toml")

    if toml is None:  # pragma: no cover
        message = "Please install the toml library."
        raise ModuleNotFoundError(message)

    with open(param_value, "r", encoding="utf-8") as _file:
        return toml.load(_file)


def dotenv_loader(param_value: TyperParameterValue) -> ConfigDict:
    """Dotenv file loader.

    Args:
        param_value (TyperParameterValue): path of Dotenv file

    Raises:
        ModuleNotFoundError: python-dotenv library is not installed

    Returns:
        ConfigDict: dictionary loaded from file
    """

    dotenv = try_import("dotenv")

    if dotenv is None:  # pragma: no cover
        message = "Please install the python-dotenv library."
        raise ModuleNotFoundError(message)

    with open(param_value, "r", encoding="utf-8") as _file:
        # NOTE: I'm using a stream here so that the loader
        # will raise an exception when the file doesn't exist.
        conf: ConfigDict = dotenv.dotenv_values(stream=_file)

    return conf


def ini_loader(param_value: TyperParameterValue) -> ConfigDict:
    """INI file loader.

    Note:
        INI files must have sections at the top level.
        You probably want to combine this with `loader_transformer`
        to extract the correct section.
        For example:
        ```py
        ini_section_loader = loader_transformer(
            ini_loader,
            config_transformer=lambda config: config["section"],
        )
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
