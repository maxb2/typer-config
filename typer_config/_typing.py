"""
Data and Function types.
"""

import sys
from typing import Any, Callable, Dict, Iterable

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

ConfDict: TypeAlias = Dict[TyperParameterName, Any]
"""Configuration dictionary to be applied to the click context default map."""

ConfDictAccessorPath: TypeAlias = Iterable[str]
"""Configuration dictionary accessor path."""

# Function types
ConfLoader: TypeAlias = Callable[[TyperParameterValue], ConfDict]
"""Configuration loader function."""

ConfigParameterCallback: TypeAlias = Callable[
    [Context, CallbackParam, TyperParameterValue], TyperParameterValue
]
"""Typer config parameter callback function."""

NoArgCallable: TypeAlias = Callable[[], Any]
"""No argument callable."""
