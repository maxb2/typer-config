"""
Data and Function types.
"""

from typing import Any, Callable, Dict, TypeAlias
from typer import Context as typer_Context, CallbackParam as typer_CallbackParam

# Data types
ConfDict: TypeAlias = Dict[str, Any]
ParameterValue: TypeAlias = Any

# Function types
Loader: TypeAlias = Callable[[Any], ConfDict]
ConfigParameterCallback: TypeAlias = Callable[
    [typer_Context, typer_CallbackParam, ParameterValue], ParameterValue
]
