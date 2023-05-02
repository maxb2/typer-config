"""
Typer Configuration Utilities
"""

import typer

from .loaders import json_loader, toml_loader, yaml_loader
from .types import ConfigParameterCallback, Loader, ParameterValue


def conf_callback_factory(loader: Loader) -> ConfigParameterCallback:
    """Configuration callback factory

    Parameters
    ----------
    loader : Loader
        Loader function that takes the value passed to the typer CLI and
        returns a dictionary that is applied to the click context's default map.

    Returns
    -------
    ConfigParameterCallback
        Configuration callback function.
    """

    def _callback(
        ctx: typer.Context, param: typer.CallbackParam, value: ParameterValue
    ) -> ParameterValue:
        try:
            conf = loader(value)  # Load config file
            ctx.default_map = ctx.default_map or {}  # Initialize the default map
            ctx.default_map.update(conf)  # Merge the config Dict into default_map
        except Exception as ex:
            raise typer.BadParameter(str(ex), ctx=ctx, param=param) from ex
        return value

    return _callback


yaml_conf_callback: ConfigParameterCallback = conf_callback_factory(yaml_loader)
json_conf_callback: ConfigParameterCallback = conf_callback_factory(json_loader)
toml_conf_callback: ConfigParameterCallback = conf_callback_factory(toml_loader)
