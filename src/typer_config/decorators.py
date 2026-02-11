"""Typer Config decorators."""

from __future__ import annotations

from enum import Enum
from functools import wraps
from inspect import Parameter, signature
from typing import TYPE_CHECKING, List, Optional

from typer import Option

from .callbacks import conf_callback_factory
from .dumpers import json_dumper, toml_dumper, yaml_dumper
from .loaders import (
    dotenv_loader,
    ini_loader,
    json_loader,
    loader_transformer,
    multifile_fallback_loader,
    multifile_loader,
    toml_loader,
    yaml_loader,
)
from .utils import file_exists_and_warn, get_dict_section

if TYPE_CHECKING:  # pragma: no cover
    from .__typing import (
        ConfigDumper,
        ConfigParameterCallback,
        FilePath,
        TyperCommand,
        TyperCommandDecorator,
        TyperParameterName,
        TyperParameterValue,
    )


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
        sig = signature(cmd, eval_str=True)

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
            kwargs.pop(param_name, None)

            return cmd(*args, **kwargs)

        wrapped.__signature__ = new_sig  # type: ignore

        return wrapped

    return decorator


# default decorators
def use_json_config(
    section: Optional[List[str]] = None,
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
    default_value: Optional[TyperParameterValue] = None,
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
        section (List[str], optional): List of nested sections to access in the config.
            Defaults to None.
        param_name (TyperParameterName, optional): name of config parameter.
            Defaults to "config".
        param_help (str, optional): config parameter help string.
            Defaults to "Configuration file.".
        default_value (TyperParameterValue, optional): default config parameter value.
            Defaults to None.

    Returns:
        TyperCommandDecorator: decorator to apply to command
    """

    callback = conf_callback_factory(
        loader_transformer(
            json_loader,
            loader_conditional=lambda param_value: (
                file_exists_and_warn(param_value) if param_value else param_value
            ),
            param_transformer=(
                (lambda param_value: param_value if param_value else default_value)
                if default_value is not None
                else None
            ),
            config_transformer=lambda config: get_dict_section(config, section),
        )
    )

    return use_config(callback=callback, param_name=param_name, param_help=param_help)


def use_yaml_config(
    section: Optional[List[str]] = None,
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
    default_value: Optional[TyperParameterValue] = None,
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
        section (List[str], optional): List of nested sections to access in the config.
            Defaults to None.
        param_name (str, optional): name of config parameter. Defaults to "config".
        param_help (str, optional): config parameter help string.
            Defaults to "Configuration file.".
        default_value (TyperParameterValue, optional): default config parameter value.
            Defaults to None.

    Returns:
        TyperCommandDecorator: decorator to apply to command
    """

    callback = conf_callback_factory(
        loader_transformer(
            yaml_loader,
            loader_conditional=lambda param_value: (
                file_exists_and_warn(param_value) if param_value else param_value
            ),
            param_transformer=(
                (lambda param_value: param_value if param_value else default_value)
                if default_value is not None
                else None
            ),
            config_transformer=lambda config: get_dict_section(config, section),
        )
    )

    return use_config(callback=callback, param_name=param_name, param_help=param_help)


def use_toml_config(
    section: Optional[List[str]] = None,
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
    default_value: Optional[TyperParameterValue] = None,
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
        section (List[str], optional): List of nested sections to access in the config.
            Defaults to None.
        param_name (str, optional): name of config parameter. Defaults to "config".
        param_help (str, optional): config parameter help string.
            Defaults to "Configuration file.".
        default_value (TyperParameterValue, optional): default config parameter value.
            Defaults to None.

    Returns:
        TyperCommandDecorator: decorator to apply to command
    """

    callback = conf_callback_factory(
        loader_transformer(
            toml_loader,
            loader_conditional=lambda param_value: (
                file_exists_and_warn(param_value) if param_value else param_value
            ),
            param_transformer=(
                (lambda param_value: param_value if param_value else default_value)
                if default_value is not None
                else None
            ),
            config_transformer=lambda config: get_dict_section(config, section),
        )
    )

    return use_config(callback=callback, param_name=param_name, param_help=param_help)


def use_dotenv_config(
    section: Optional[List[str]] = None,
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
    default_value: Optional[TyperParameterValue] = None,
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
        section (List[str], optional): List of nested sections to access in the config.
            Defaults to None.
        param_name (str, optional): name of config parameter. Defaults to "config".
        param_help (str, optional): config parameter help string.
            Defaults to "Configuration file.".
        default_value (TyperParameterValue, optional): default config parameter value.
            Defaults to None.

    Returns:
        TyperCommandDecorator: decorator to apply to command
    """

    callback = conf_callback_factory(
        loader_transformer(
            dotenv_loader,
            loader_conditional=lambda param_value: (
                file_exists_and_warn(param_value) if param_value else param_value
            ),
            param_transformer=(
                (lambda param_value: param_value if param_value else default_value)
                if default_value is not None
                else None
            ),
            config_transformer=lambda config: get_dict_section(config, section),
        )
    )

    return use_config(callback=callback, param_name=param_name, param_help=param_help)


def use_ini_config(
    section: List[str],
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
    default_value: Optional[TyperParameterValue] = None,
) -> TyperCommandDecorator:
    """Decorator for using INI configuration on a typer command.

    Usage:
        ```py
        import typer
        from typer_config.decorators import use_ini_config

        app = typer.Typer()

        @app.command()
        @use_ini_config(["section", "subsection"])
        def main(...):
            ...
        ```

    Args:
        section (List[str]): List of nested sections to access in the INI file.
        param_name (str, optional): name of config parameter. Defaults to "config".
        param_help (str, optional): config parameter help string.
            Defaults to "Configuration file.".
        default_value (TyperParameterValue, optional): default config parameter value.
            Defaults to None.

    Returns:
        TyperCommandDecorator: decorator to apply to command
    """

    callback = conf_callback_factory(
        loader_transformer(
            ini_loader,
            loader_conditional=lambda param_value: (
                file_exists_and_warn(param_value) if param_value else param_value
            ),
            param_transformer=(
                (lambda param_value: param_value if param_value else default_value)
                if default_value is not None
                else None
            ),
            config_transformer=lambda config: get_dict_section(config, section),
        )
    )

    return use_config(callback=callback, param_name=param_name, param_help=param_help)


def use_multifile_config(
    default_files: List[TyperParameterValue],
    section: Optional[List[str]] = None,
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
) -> TyperCommandDecorator:
    """Decorator for using multiple configuration files on a typer command.

    Multiple config files are merged together, with later files overriding
    earlier ones. Files that don't exist are skipped. Nested dictionaries
    are deep-merged.

    This is useful for configuration inheritance, e.g.:
    - Start with system defaults: `/etc/myapp.yaml`
    - Override with user config: `~/.config/myapp.yaml`
    - Override with local config: `./myapp.yaml`
    - Override with --config option if provided

    Usage:
        ```py
        import typer
        from typer_config.decorators import use_multifile_config

        app = typer.Typer()

        @app.command()
        @use_multifile_config([
            "/etc/myapp.yaml",
            "~/.config/myapp.yaml",
            "./myapp.yaml",
        ])
        def main(...):
            ...
        ```

    Args:
        default_files (List[TyperParameterValue]): List of default file paths to load.
            Files are processed in order, with later files overriding earlier ones.
            Missing files are silently skipped.
        section (List[str], optional): List of nested sections to access in the config.
            Defaults to None.
        param_name (TyperParameterName, optional): name of config parameter.
            Defaults to "config".
        param_help (str, optional): config parameter help string.
            Defaults to "Configuration file.".

    Returns:
        TyperCommandDecorator: decorator to apply to command
    """

    callback = conf_callback_factory(
        loader_transformer(
            multifile_loader,
            loader_conditional=lambda _: True,  # always load
            param_transformer=lambda param_value: (
                [*default_files, param_value] if param_value else default_files
            ),
            config_transformer=lambda config: get_dict_section(config, section),
        )
    )

    return use_config(callback=callback, param_name=param_name, param_help=param_help)


def use_fallback_config(
    fallback_files: List[TyperParameterValue],
    section: Optional[List[str]] = None,
    param_name: TyperParameterName = "config",
    param_help: str = "Configuration file.",
) -> TyperCommandDecorator:
    """Decorator for using a fallback list of configuration files.

    Only the first existing configuration file is used. Files are checked
    in order from first to last.

    This is useful for fallback configurations, e.g.:
    - Use local config if it exists: `./myapp.yaml`
    - Otherwise, use user config: `~/.config/myapp.yaml`
    - Otherwise, use system config: `/etc/myapp.yaml`

    Usage:
        ```py
        import typer
        from typer_config.decorators import use_fallback_config

        app = typer.Typer()

        @app.command()
        @use_fallback_config([
            "./myapp.yaml",           # highest priority
            "~/.config/myapp.yaml",
            "/etc/myapp.yaml",        # lowest priority
        ])
        def main(...):
            ...
        ```

    Args:
        fallback_files (List[TyperParameterValue]): List of file paths to try,
            in order of priority (first has highest priority).
            The first existing file will be used.
        section (List[str], optional): List of nested sections to access in the config.
            Defaults to None.
        param_name (TyperParameterName, optional): name of config parameter.
            Defaults to "config".
        param_help (str, optional): config parameter help string.
            Defaults to "Configuration file.".

    Returns:
        TyperCommandDecorator: decorator to apply to command
    """

    callback = conf_callback_factory(
        loader_transformer(
            multifile_fallback_loader,
            loader_conditional=lambda _: True,  # always load
            param_transformer=lambda param_value: (
                [param_value, *fallback_files] if param_value else fallback_files
            ),
            config_transformer=lambda config: get_dict_section(config, section),
        )
    )

    return use_config(callback=callback, param_name=param_name, param_help=param_help)


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
