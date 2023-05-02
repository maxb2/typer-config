"""
Data and Function types.
"""

import sys
from typing import Any, Callable, Dict

from typer import CallbackParam as typer_CallbackParam
from typer import Context as typer_Context

# Handle TypeAlias based on python version
if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias

# Data types
ConfDict: TypeAlias = Dict[str, Any]
ParameterValue: TypeAlias = Any

# Function types
Loader: TypeAlias = Callable[[Any], ConfDict]
ConfigParameterCallback: TypeAlias = Callable[
    [typer_Context, typer_CallbackParam, ParameterValue], ParameterValue
]
