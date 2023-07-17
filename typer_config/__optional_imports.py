# pylint: disable=unused-import

"""
Handle optional and version dependent imports.

Note: Be careful with this file because other files wildcard import from here.

"""

import sys

USING_TOMLLIB = False
TOML_MISSING = True
YAML_MISSING = True
DOTENV_MISSING = True


if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib  # type: ignore

    USING_TOMLLIB = True

try:  # pragma: no cover
    # Third-party toml parsing library
    # Note: needed for writing TOML files
    import toml

    TOML_MISSING = False

except ImportError:  # pragma: no cover
    pass


try:  # pragma: no cover
    import yaml

    YAML_MISSING = False
except ImportError:  # pragma: no cover
    pass

try:  # pragma: no cover
    import dotenv

    DOTENV_MISSING = False
except ImportError:  # pragma: no cover
    pass
