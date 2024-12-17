"""Data and Function types."""

import sys
from pathlib import Path
from typing import Any, Callable, Dict, Union

from typer import CallbackParam, Context

# Handle some imports based on python version
if sys.version_info < (3, 10):  # pragma: no cover
    from typing_extensions import TypeAlias
else:  # pragma: no cover
    from typing import TypeAlias

# Data types
TyperParameterName: TypeAlias = str
"""Typer CLI parameter name."""

TyperParameterValue: TypeAlias = Any
"""Typer CLI parameter value."""

ConfigDict: TypeAlias = Dict[TyperParameterName, Any]
"""Configuration dictionary to be applied to the click context default map."""


FilePath: TypeAlias = Union[Path, str]
"""File path"""

# Function types
TyperParameterValueTransformer: TypeAlias = Callable[
    [TyperParameterValue], TyperParameterValue
]
"""Typer parameter value transforming function."""

ConfigDictTransformer: TypeAlias = Callable[[ConfigDict], ConfigDict]
"""ConfigDict transforming function."""

ConfigLoader: TypeAlias = Callable[[TyperParameterValue], ConfigDict]
"""Configuration loader function."""

ConfigLoaderConditional: TypeAlias = Callable[[TyperParameterValue], bool]
"""Configuration loader conditional function."""

ConfigParameterCallback: TypeAlias = Callable[
    [Context, CallbackParam, TyperParameterValue], TyperParameterValue
]
"""Typer config parameter callback function."""

ConfigDumper: TypeAlias = Callable[[ConfigDict, FilePath], None]
"""Configuration dumper function."""

TyperCommand: TypeAlias = Callable[..., Any]
"""A function that will be decorated with `typer.Typer().command()`."""

TyperCommandDecorator: TypeAlias = Callable[[TyperCommand], TyperCommand]
"""A decorator applied to a typer command."""
