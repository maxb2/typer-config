"""Typer Configuration Parameter Callbacks."""

from __future__ import annotations

from typing import List, Optional

from typer import BadParameter, CallbackParam, Context

# NOTE: I'm not sure why, but these types must be imported at runtime
# for the tests to pass...
from .__typing import (  # noqa: TCH001
    ConfigLoader,
    ConfigParameterCallback,
    TyperParameterValue,
)
from .loaders import (
    dotenv_loader,
    json_loader,
    loader_transformer,
    toml_loader,
    yaml_loader,
)


def conf_callback_factory(loader: ConfigLoader) -> ConfigParameterCallback:
    """Typer configuration callback factory.

    Args:
        loader (ConfigLoader): Config loader function that takes the value
            passed to the typer CLI and returns a dictionary that is
            applied to the click context's default map.

    Returns:
        ConfigParameterCallback: Configuration parameter callback function.
    """

    def _callback(
        ctx: Context, param: CallbackParam, param_value: TyperParameterValue
    ) -> TyperParameterValue:
        """Generated typer config parameter callback.

        Args:
            ctx (typer.Context): typer context (automatically passed)
            param (typer.CallbackParam): typer callback parameter (automatically passed)
            param_value (TyperParameterValue): parameter value passed to typer
                (automatically passed)

        Raises:
            BadParameter: bad parameter value

        Returns:
            TyperParameterValue: must return back the given parameter
        """
        try:
            conf = loader(param_value)  # Load config file
            ctx.default_map = ctx.default_map or {}  # Initialize the default map
            ctx.default_map.update(conf)  # Merge the config Dict into default_map
        except Exception as ex:
            raise BadParameter(str(ex), ctx=ctx, param=param) from ex
        return param_value

    return _callback


yaml_conf_callback: ConfigParameterCallback = conf_callback_factory(
    loader_transformer(yaml_loader, loader_conditional=lambda param_value: param_value)
)
"""YAML typer config parameter callback.

Args:
    ctx (typer.Context): typer context (automatically passed)
    param (typer.CallbackParam): typer callback parameter (automatically passed)
    param_value (TyperParameterValue): parameter value passed to typer (automatically
        passed)

Raises:
    BadParameter: bad parameter value

Returns:
    TyperParameterValue: must return back the given parameter
"""

json_conf_callback: ConfigParameterCallback = conf_callback_factory(
    loader_transformer(json_loader, loader_conditional=lambda param_value: param_value)
)
"""JSON typer config parameter callback.

Args:
    ctx (typer.Context): typer context (automatically passed)
    param (typer.CallbackParam): typer callback parameter (automatically passed)
    param_value (TyperParameterValue): parameter value passed to typer (automatically
        passed)

Raises:
    BadParameter: bad parameter value

Returns:
    TyperParameterValue: must return back the given parameter
"""


toml_conf_callback: ConfigParameterCallback = conf_callback_factory(
    loader_transformer(toml_loader, loader_conditional=lambda param_value: param_value)
)
"""TOML typer config parameter callback.

Args:
    ctx (typer.Context): typer context (automatically passed)
    param (typer.CallbackParam): typer callback parameter (automatically passed)
    param_value (TyperParameterValue): parameter value passed to typer (automatically
        passed)

Raises:
    BadParameter: bad parameter value

Returns:
    TyperParameterValue: must return back the given parameter
"""

dotenv_conf_callback: ConfigParameterCallback = conf_callback_factory(
    loader_transformer(
        dotenv_loader, loader_conditional=lambda param_value: param_value
    )
)
"""Dotenv typer config parameter callback.

Args:
    ctx (typer.Context): typer context (automatically passed)
    param (typer.CallbackParam): typer callback parameter (automatically passed)
    param_value (TyperParameterValue): parameter value passed to typer (automatically
        passed)

Raises:
    BadParameter: bad parameter value

Returns:
    TyperParameterValue: must return back the given parameter
"""


def argument_list_callback(
    ctx: Context, param: CallbackParam, param_value: Optional[List[str]]
) -> List[str]:
    """Argument list callback.

    Note:
        This is a shim to fix list arguments in a config.
        See [maxb2/typer-config#124](https://github.com/maxb2/typer-config/issues/124).

    Args:
        ctx (typer.Context): typer context
        param (typer.CallbackParam): typer parameter
        param_value (Optional[List[str]]): typer parameter value

    Returns:
        List[str]: argument list
    """
    ctx.default_map = ctx.default_map or {}
    default = ctx.default_map.get(param.name, []) if param.name else []
    return param_value if param_value else default
