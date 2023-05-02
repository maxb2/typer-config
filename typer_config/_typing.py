"""
Data and Function types.
"""

import sys
from typing import Any, Callable, Dict, Iterable

from typer import CallbackParam
from typer import Context

# Handle some imports based on python version
if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias, ParamSpec
else:
    from typing import TypeAlias, ParamSpec

# Data types
ConfDict: TypeAlias = Dict[str, Any]
ParameterValue: TypeAlias = Any
ConfDictPath: TypeAlias = Iterable[str]

# Function(al) types
Loader: TypeAlias = Callable[[Any], ConfDict]
ConfigParameterCallback: TypeAlias = Callable[
    [Context, CallbackParam, ParameterValue], ParameterValue
]
ValueGetter: TypeAlias = Callable[[], Any]
LoaderCombinator: TypeAlias = Callable[[Loader, ParamSpec], Loader]
