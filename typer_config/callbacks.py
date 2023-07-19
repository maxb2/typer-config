"""Typer Configuration Parameter Callbacks."""

from typer import BadParameter, CallbackParam, Context

from .__typing import ConfigLoader, ConfigParameterCallback, TyperParameterValue
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
        except Exception as ex:  # noqa: BLE001 (reraising to typer framework)
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
