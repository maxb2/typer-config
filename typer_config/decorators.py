"""Typer Config decorators."""

from enum import Enum
from functools import wraps
from inspect import Parameter, signature

from typer import Option

from .__typing import (
    ConfigDumper,
    ConfigParameterCallback,
    FilePath,
    TyperCommand,
    TyperCommandDecorator,
    TyperParameterName,
)
from .callbacks import (
    dotenv_conf_callback,
    json_conf_callback,
    toml_conf_callback,
    yaml_conf_callback,
)
from .dumpers import json_dumper, toml_dumper, yaml_dumper


def use_config(
    callback: ConfigParameterCallback,
    param_name: TyperParameterName = "config",
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
        param_name (TyperParameterName, optional): name of config parameter.
            Defaults to "config".
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
            annotation=str,
            default=Option("", callback=callback, is_eager=True, help=param_help),
        )

        new_sig = sig.replace(parameters=[*sig.parameters.values(), config_param])

        @wraps(cmd)
        def wrapped(*args, **kwargs):  # noqa: ANN202,ANN002,ANN003
            # NOTE: need to delete the config parameter
            # to match the wrapped command's signature.
            if param_name in kwargs:
                del kwargs[param_name]

            return cmd(*args, **kwargs)

        wrapped.__signature__ = new_sig  # type: ignore

        return wrapped

    return decorator


# default decorators
def use_json_config(
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
) -> TyperCommandDecorator:
    """Decorator for using JSON configuration on a typer command.

    Usage:
        ```py
        import typer
        from typer_config.decorators import use_json_config

        app = typer.Typer()

        @app.command()
        @use_json_config()
        def main(...):
            ...
        ```

    Args:
        param_name (TyperParameterName, optional): name of config parameter.
            Defaults to "config".
        param_help (str, optional): config parameter help string.
            Defaults to "Configuration file.".

    Returns:
        TyperCommandDecorator: decorator to apply to command
    """
    return use_config(
        callback=json_conf_callback, param_name=param_name, param_help=param_help
    )


def use_yaml_config(
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
) -> TyperCommandDecorator:
    """Decorator for using YAML configuration on a typer command.

    Usage:
        ```py
        import typer
        from typer_config.decorators import use_yaml_config

        app = typer.Typer()

        @app.command()
        @use_yaml_config()
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
    return use_config(
        callback=yaml_conf_callback, param_name=param_name, param_help=param_help
    )


def use_toml_config(
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
) -> TyperCommandDecorator:
    """Decorator for using TOML configuration on a typer command.

    Usage:
        ```py
        import typer
        from typer_config.decorators import use_toml_config

        app = typer.Typer()

        @app.command()
        @use_toml_config()
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
    return use_config(
        callback=toml_conf_callback, param_name=param_name, param_help=param_help
    )


def use_dotenv_config(
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
) -> TyperCommandDecorator:
    """Decorator for using dotenv configuration on a typer command.

    Usage:
        ```py
        import typer
        from typer_config.decorators import use_dotenv_config

        app = typer.Typer()

        @app.command()
        @use_dotenv_config()
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
    return use_config(
        callback=dotenv_conf_callback, param_name=param_name, param_help=param_help
    )


def dump_config(dumper: ConfigDumper, location: FilePath) -> TyperCommandDecorator:
    """Decorator for dumping a config file with parameters
    from an invocation of a typer command.

    Usage:
        ```py
        import typer
        from typer.decorators import dump_config

        app = typer.Typer()

        @app.command()
        # NOTE: @dump_config MUST BE AFTER @app.command()
        @dump_config(yaml_dumper, "config_dump_dir/params.yaml")
        def cmd(...):
            ...
        ```

    Args:
        dumper (ConfigDumper): config file dumper
        location (FilePath): config file to write

    Returns:
        TyperCommandDecorator: command decorator
    """

    def decorator(cmd: TyperCommand) -> TyperCommand:
        @wraps(cmd)
        def inner(*args, **kwargs):  # noqa: ANN202,ANN002,ANN003
            # get a dictionary of the passed args
            bound_args = signature(cmd).bind(*args, **kwargs).arguments

            # convert enums to their values
            # NOTE: bound_args shouldn't be nested in the typer
            # framework, so top level iteration should be fine.
            for key, val in bound_args.items():
                if isinstance(val, Enum):
                    bound_args[key] = val.value

            # dump passed args
            dumper(bound_args, location)

            # run original command
            return cmd(*args, **kwargs)

        return inner

    return decorator


def dump_json_config(location: FilePath) -> TyperCommandDecorator:
    """Decorator for dumping a JSON file with parameters
    from an invocation of a typer command.

    Usage:
        ```py
        import typer
        from typer.decorators import dump_json_config

        app = typer.Typer()

        @app.command()
        # NOTE: @dump_json_config MUST BE AFTER @app.command()
        @dump_json_config("config_dump_dir/params.json")
        def cmd(...):
            ...
        ```

    Args:
        location (FilePath): config file to write

    Returns:
        TyperCommandDecorator: command decorator
    """
    return dump_config(dumper=json_dumper, location=location)


def dump_yaml_config(location: FilePath) -> TyperCommandDecorator:
    """Decorator for dumping a YAML file with parameters
    from an invocation of a typer command.

    Usage:
        ```py
        import typer
        from typer.decorators import dump_yaml_config

        app = typer.Typer()

        @app.command()
        # NOTE: @dump_yaml_config MUST BE AFTER @app.command()
        @dump_yaml_config("config_dump_dir/params.yml")
        def cmd(...):
            ...
        ```

    Args:
        location (FilePath): config file to write

    Returns:
        TyperCommandDecorator: command decorator
    """
    return dump_config(dumper=yaml_dumper, location=location)


def dump_toml_config(location: FilePath) -> TyperCommandDecorator:
    """Decorator for dumping a TOML file with parameters
    from an invocation of a typer command.

    Usage:
        ```py
        import typer
        from typer.decorators import dump_toml_config

        app = typer.Typer()

        @app.command()
        # NOTE: @dump_toml_config MUST BE AFTER @app.command()
        @dump_toml_config("config_dump_dir/params.toml")
        def cmd(...):
            ...
        ```

    Args:
        location (FilePath): config file to write

    Returns:
        TyperCommandDecorator: command decorator
    """
    return dump_config(dumper=toml_dumper, location=location)
