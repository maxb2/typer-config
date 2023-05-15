"""
Typer Configuration Utilities
"""

from typer import Context, CallbackParam, BadParameter

from .__typing import ConfigParameterCallback, ConfigLoader, TyperParameterValue
from .loaders import json_loader, toml_loader, yaml_loader


def conf_callback_factory(loader: ConfigLoader) -> ConfigParameterCallback:
    """Typer configuration callback factory.

    Parameters
    ----------
    loader : ConfigLoader
        Config loader function that takes the value passed to the typer CLI and
        returns a dictionary that is applied to the click context's default map.

    Returns
    -------
    ConfigParameterCallback
        Configuration parameter callback function.
    """

    def _callback(
        ctx: Context, param: CallbackParam, param_value: TyperParameterValue
    ) -> TyperParameterValue:
        try:
            conf = loader(param_value)  # Load config file
            ctx.default_map = ctx.default_map or {}  # Initialize the default map
            ctx.default_map.update(conf)  # Merge the config Dict into default_map
        except Exception as ex:
            raise BadParameter(str(ex), ctx=ctx, param=param) from ex
        return param_value

    return _callback


yaml_conf_callback: ConfigParameterCallback = conf_callback_factory(yaml_loader)
"""YAML configuration callback for a typer parameter."""

json_conf_callback: ConfigParameterCallback = conf_callback_factory(json_loader)
"""JSON configuration callback for a typer parameter."""

toml_conf_callback: ConfigParameterCallback = conf_callback_factory(toml_loader)
"""TOML configuration callback for a typer parameter."""
