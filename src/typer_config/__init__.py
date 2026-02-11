"""Typer Configuration Utilities."""

import importlib.metadata

from .callbacks import (
    conf_callback_factory,
    dotenv_conf_callback,
    json_conf_callback,
    toml_conf_callback,
    yaml_conf_callback,
)
from .decorators import (
    use_config,
    use_fallback_config,
    use_ini_config,
    use_json_config,
    use_multifile_config,
    use_toml_config,
    use_yaml_config,
)
from .loaders import (
    dotenv_loader,
    ini_loader,
    json_loader,
    multifile_fallback_loader,
    multifile_loader,
    toml_loader,
    yaml_loader,
)

__version__ = importlib.metadata.version("typer_config")

__all__ = [
    "conf_callback_factory",
    "dotenv_conf_callback",
    "dotenv_loader",
    "ini_loader",
    "json_conf_callback",
    "json_loader",
    "multifile_fallback_loader",
    "multifile_loader",
    "toml_conf_callback",
    "toml_loader",
    "use_config",
    "use_fallback_config",
    "use_ini_config",
    "use_json_config",
    "use_multifile_config",
    "use_toml_config",
    "use_yaml_config",
    "yaml_conf_callback",
    "yaml_loader",
]
