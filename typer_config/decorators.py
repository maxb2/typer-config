"""Typer Config decorators."""

from inspect import Parameter
from typing import Callable

import typer

from .__typing import ConfigParameterCallback, TyperCommand

try:  # pragma: no cover
    from makefun import wraps

except ImportError as exc:  # pragma: no cover
    raise ModuleNotFoundError(
        "Please install makefun to use typer-config decorators."
    ) from exc


def use_config(
    callback: ConfigParameterCallback,
) -> Callable[[TyperCommand], TyperCommand]:
    """TODO"""

    def decorator(cmd: TyperCommand) -> TyperCommand:
        config_param = Parameter(
            "config",
            kind=Parameter.KEYWORD_ONLY,
            annotation=str,
            default=typer.Option(
                "",
                callback=callback,
                is_eager=True,
            ),
        )

        @wraps(
            cmd,
            append_args=config_param,
        )
        def inner(*args, **kwargs):
            return cmd(
                *args,
                **kwargs,
            )

        return inner

    return decorator
