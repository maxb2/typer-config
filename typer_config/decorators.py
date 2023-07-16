"""Typer Config decorators."""

from functools import partial, wraps
from inspect import Parameter, signature

from typer import Option

from . import (
    dotenv_conf_callback,
    json_conf_callback,
    toml_conf_callback,
    yaml_conf_callback,
)
from .__typing import ConfigParameterCallback, TyperCommand, TyperCommandDecorator


def use_config(
    callback: ConfigParameterCallback,
    param_name: str = "config",
    param_help: str = "Configuration file.",
) -> TyperCommandDecorator:
    """Decorator for using configuration on a typer command.

    Usage:
        ```py
        import typer
        from typer_config.decorators import use_config
        from typer_config import yaml_conf_callback # whichever callback to use

        app = typer.Typer()

        @app.command()
        @use_config(yaml_conf_callback)
        def main(...):
            ...
        ```

    Args:
        callback (ConfigParameterCallback): config parameter callback to load
        param_name (str, optional): name of config parameter. Defaults to "config".
        param_help (str, optional): config parameter help string.
            Defaults to "Configuration file.".

    Returns:
        TyperCommandDecorator: decorator to apply to command
    """

    def decorator(cmd: TyperCommand) -> TyperCommand:
        # NOTE: modifying a function's __signature__ is dangerous
        # in the sense that it only affects inspect.signature().
        # It does not affect the actual function implementation.
        # So, a caller can be confused how to pass parameters to
        # the function with modified signature.
        sig = signature(cmd)

        config_param = Parameter(
            param_name,
            kind=Parameter.KEYWORD_ONLY,
            annotation=str,  # NOTE: should this be configurable?
            default=Option("", callback=callback, is_eager=True, help=param_help),
        )

        new_sig = sig.replace(parameters=[*sig.parameters.values(), config_param])

        @wraps(cmd)
        def wrapped(*args, **kwargs):
            # NOTE: need to delete the config parameter
            # to match the wrapped command's signature.
            if param_name in kwargs:
                del kwargs[param_name]

            return cmd(*args, **kwargs)

        wrapped.__signature__ = new_sig  # type: ignore

        return wrapped

    return decorator


# default decorators
json_config = partial(use_config, callback=json_conf_callback)
"""Decorator for using JSON configuration on a typer command.

Usage:
    ```py
    import typer
    from typer_config.decorators import json_config

    app = typer.Typer()

    @app.command()
    @json_config()
    def main(...):
        ...
    ```

Args:
    param_name (str, optional): name of config parameter. Defaults to "config".
    param_help (str, optional): config parameter help string.
        Defaults to "Configuration file.".

Returns:
    TyperCommandDecorator: decorator to apply to command
"""

yaml_config = partial(use_config, callback=yaml_conf_callback)
"""Decorator for using YAML configuration on a typer command.

Usage:
    ```py
    import typer
    from typer_config.decorators import yaml_config

    app = typer.Typer()

    @app.command()
    @yaml_config()
    def main(...):
        ...
    ```

Args:
    param_name (str, optional): name of config parameter. Defaults to "config".
    param_help (str, optional): config parameter help string.
        Defaults to "Configuration file.".

Returns:
    TyperCommandDecorator: decorator to apply to command
"""

toml_config = partial(use_config, callback=toml_conf_callback)
"""Decorator for using TOML configuration on a typer command.

Usage:
    ```py
    import typer
    from typer_config.decorators import toml_config

    app = typer.Typer()

    @app.command()
    @toml_config()
    def main(...):
        ...
    ```

Args:
    param_name (str, optional): name of config parameter. Defaults to "config".
    param_help (str, optional): config parameter help string.
        Defaults to "Configuration file.".

Returns:
    TyperCommandDecorator: decorator to apply to command
"""

dotenv_config = partial(use_config, callback=dotenv_conf_callback)
"""Decorator for using dotenv configuration on a typer command.

Usage:
    ```py
    import typer
    from typer_config.decorators import dotenv_config

    app = typer.Typer()

    @app.command()
    @dotenv_config()
    def main(...):
        ...
    ```

Args:
    param_name (str, optional): name of config parameter. Defaults to "config".
    param_help (str, optional): config parameter help string.
        Defaults to "Configuration file.".

Returns:
    TyperCommandDecorator: decorator to apply to command
"""
