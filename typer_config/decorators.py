"""Typer Config decorators."""

import inspect
from functools import wraps
from inspect import Parameter
from typing import Callable

import typer

from .__typing import ConfigParameterCallback, TyperCommand


def use_config(
    callback: ConfigParameterCallback,
    param_name: str = "config",
    param_help: str = "Configuration file.",
) -> Callable[[TyperCommand], TyperCommand]:
    """TODO"""

    def decorator(cmd: TyperCommand) -> TyperCommand:
        # NOTE: modifying a functions __signature__ is dangerous
        # in the sense that it only affects inspect.signature().
        # It does not affect the actual function implementation.
        # So, a caller can be confused how to pass parameters to 
        # the function with modified signature.
        sig = inspect.signature(cmd)

        config_param = Parameter(
            param_name,
            kind=Parameter.KEYWORD_ONLY,
            annotation=str,  # NOTE: should this be configurable?
            default=typer.Option("", callback=callback, is_eager=True, help=param_help),
        )

        new_sig = sig.replace(parameters=[*sig.parameters.values(), config_param])

        @wraps(cmd)
        def inner(*args, **kwargs):
            # NOTE: need to delete the config parameter
            # to match the wrapped command's signature.
            if param_name in kwargs:
                del kwargs[param_name]

            return cmd(
                *args,
                **kwargs,
            )

        inner.__signature__ = new_sig  # type: ignore

        return inner

    return decorator
