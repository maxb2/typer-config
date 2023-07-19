"""Config Dictionary Dumpers."""

import json

from .__optional_imports import try_import
from .__typing import ConfigDict, FilePath


def json_dumper(config: ConfigDict, location: FilePath) -> None:
    """Dump config to JSON file.

    Args:
        config (ConfigDict): configuration
        location (FilePath): file to write
    """
    with open(location, "w", encoding="utf-8") as _file:
        json.dump(config, _file)


def yaml_dumper(config: ConfigDict, location: FilePath) -> None:
    """Dump config to YAML file.

    Args:
        config (ConfigDict): configuration
        location (FilePath): file to write

    Raises:
        ModuleNotFoundError: pyyaml is required
    """

    yaml = try_import("yaml")

    if yaml is None:  # pragma: no cover
        message = "Please install the pyyaml library."
        raise ModuleNotFoundError(message)

    with open(location, "w", encoding="utf-8") as _file:
        # NOTE: we must convert config from OrderedDict to dict because
        # pyyaml can't load OrderedDict for python <= 3.8
        yaml.dump(dict(config), _file)


def toml_dumper(config: ConfigDict, location: FilePath) -> None:
    """Dump config to TOML file.

    Args:
        config (ConfigDict): configuration
        location (FilePath): file to write

    Raises:
        ModuleNotFoundError: toml library is required for writing files
    """

    toml = try_import("toml")

    if toml is None:  # pragma: no cover
        message = "Please install the toml library to write TOML files."
        raise ModuleNotFoundError(message)

    with open(location, "w", encoding="utf-8") as _file:
        toml.dump(config, _file)  # type: ignore
