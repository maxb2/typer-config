"""
Data and Function types.
"""

import sys
from typing import Any, Callable, Dict, Iterable

from typer import CallbackParam
from typer import Context

# Handle some imports based on python version
if sys.version_info < (3, 10):  # pragma: no cover
    from typing_extensions import TypeAlias, ParamSpec
else:  # pragma: no cover
    from typing import TypeAlias, ParamSpec

# Data types
ConfDict: TypeAlias = Dict[str, Any]
"""Configuration dictionary."""
ParameterValue: TypeAlias = Any
"""Typer parameter value."""
ConfDictPath: TypeAlias = Iterable[str]
"""Accessor path for a configuration dictionary."""

# Function(al) types
Loader: TypeAlias = Callable[[Any], ConfDict]
"""Configuration loader function."""
ConfigParameterCallback: TypeAlias = Callable[
    [Context, CallbackParam, ParameterValue], ParameterValue
]
"""Typer config parameter callback function."""
ValueGetter: TypeAlias = Callable[[], Any]
"""Value getter function."""
LoaderCombinator: TypeAlias = Callable[[Loader, ParamSpec], Loader]
"""Loader function combinator."""
