"""
Typer Configuration Utilities
"""

from typing import Any, Callable

import typer

from .loaders import json_loader, toml_loader, yaml_loader


def conf_callback_factory(
    loader: Callable[[Any], dict[str, Any]]
) -> Callable[[typer.Context, typer.CallbackParam, Any], Any]:
    """Configuration callback factory

    Parameters
    ----------
    loader : Callable[[Any], dict[str, Any]]
        Loader function that takes the value passed to the typer CLI and
        returns a dictionary that is applied to the click context's default map.

    Returns
    -------
    Callable[[typer.Context, typer.CallbackParam, Any], Any]
        Configuration callback function.
    """

    def _callback(ctx: typer.Context, param: typer.CallbackParam, value: Any) -> Any:
        try:
            conf = loader(value)  # Load config file
            ctx.default_map = ctx.default_map or {}  # Initialize the default map
            ctx.default_map.update(conf)  # Merge the config dict into default_map
        except Exception as ex:
            raise typer.BadParameter(param) from ex
        return value

    return _callback


yaml_conf_callback = conf_callback_factory(yaml_loader)
json_conf_callback = conf_callback_factory(json_loader)
toml_conf_callback = conf_callback_factory(toml_loader)
