# typer-config

[![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/maxb2/typer-config/ci.yml?branch=main&style=flat-square)](https://github.com/maxb2/typer-config/actions/workflows/ci.yml)
[![Codecov](https://img.shields.io/codecov/c/github/maxb2/typer-config?style=flat-square)](https://app.codecov.io/gh/maxb2/typer-config)
[![PyPI](https://img.shields.io/pypi/v/typer-config?style=flat-square)](https://pypi.org/project/typer-config/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/typer-config?style=flat-square)](https://pypi.org/project/typer-config/#history)
[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/typer-config?style=flat-square)](https://libraries.io/pypi/typer-config)

This is a collection of utilities to use configuration files to set parameters for a [typer](https://github.com/tiangolo/typer) CLI.
It is useful for typer commands with many options/arguments so you don't have to constantly rewrite long commands.
This package was inspired by [phha/click_config_file](https://github.com/phha/click_config_file) and prototyped in [this issue](https://github.com/tiangolo/typer/issues/86#issuecomment-996374166). It allows you to set values for CLI parameters using a configuration file. 

```bash
# Long commands like this:
$ my-typer-app --opt1 foo --opt2 bar arg1 arg2

# Can become this:
$ my-typer-app --config config.yml
```

## Quickstart

You can use a decorator to quickly add a configuration parameter to your `typer` application:

```py
import typer
from typer_config import use_yaml_config  # other formats available (1)

app = typer.Typer()


@app.command()
@use_yaml_config()  # MUST BE AFTER @app.command() (2)
def main(foo: FooType): ...


if __name__ == "__main__":
    app()
```

1. This package also provides `use_json_config`, `use_toml_config`, `use_ini_config`, and `use_dotenv_config` for those file formats.
   You can also use your own loader function and the `@use_config(loader_func)` decorator.
   > Note that since INI requires a top-level section `use_ini_config` requires a list of strings that express the path to the section
   you wish to use, e.g. `@use_ini_config(["section", "subsection", ...])`. 

2. The `app.command()` decorator registers the function object in a lookup table, so we must transform our command before registration.

Your typer command will now include a `--config CONFIG_FILE` option at the command line.

See [Examples](examples/simple_yaml) for more use cases.