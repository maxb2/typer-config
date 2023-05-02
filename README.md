# typer-config

This is a collection of utilities to use configuration files to set parameters for a [typer](https://github.com/tiangolo/typer) CLI.
It is useful for typer commands with many options/arguments so you don't have to constantly rewrite long commands.
This package was inspired by [phha/click_config_file](https://github.com/phha/click_config_file) and prototyped in [this issue](https://github.com/tiangolo/typer/issues/86#issuecomment-996374166). It allows you to set values for CLI parameters using a configuration file. 

## Installation

```bash
$ pip install typer-config[all]
```

> **Note**: that will include libraries for reading from YAML and TOML files as well.
  Feel free to leave off the optional dependencies if you don't need YAML or TOML capabilities.

## Example

### Simple YAML

An example typer app:
```python
# typer_config.py
import typer
from typer_config import yaml_conf_callback

app = typer.Typer( )

@app.command()
def main(
    arg1: str,
    config: str = typer.Option(
        "",
        callback=yaml_conf_callback,
        is_eager=True,  # THIS IS REALLY IMPORTANT
    ),
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

With a config file:

```yaml
# config.yaml
arg1: stuff
opt1: things
opt2: nothing
```

And invoked with python:

```bash
$ python typer_config.py --config config.yml
things nothing stuff

$ python typer_config.py --config config.yml others
things nothing others

$ python typer_config.py --config config.yml --opt1 people
people nothing stuff
```

> **Note**: this package also provides `json_conf_callback` and `toml_conf_callback` for those file formats.

### Custom file loader

If you use an unsupported file format or need to do extra processing of the file, you can make your own file loader and construct an appropriate callback.

Suppose you want to specify parameters in a section of `pyproject.toml`:

```toml
[tools.my_tool.parameters]
arg1 = "stuff"
opt1 = "things"
opt2 = "nothing"
```

Then, we can read the values in our typer CLI:

```python
# my_tool.py
from typing import Any, Dict

import typer
from typer_config import conf_callback_factory
from typer_config.loaders import toml_loader


def pyproject_loader(param_value: str) -> Dict[str, Any]:
    if not param_value: # set a default path to read from
        param_value = "pyproject.toml"
        
    pyproject = toml_loader("pyproject.toml")
    conf = pyproject["tools"]["my_tool"]["parameters"]
    return conf

### You can define the same loader using some provided combinators:
#
# from typer_config.loaders import default_value_loader, subpath_loader, toml_loader
# 
# pyproject_loader = subpath_loader(
#     default_value_loader(toml_loader, lambda: "pyproject.toml"),
#     ["tools", "my_tool", "parameters"],
# )

pyproject_callback = conf_callback_factory(pyproject_loader)

app = typer.Typer( )

@app.command()
def main(
    arg1: str,
    config: str = typer.Option(
        "",
        callback=pyproject_callback,
        is_eager=True,  # THIS IS REALLY IMPORTANT
    ),
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

And we get this behavior:

```bash
$ ls .
my_tool.py other.toml pyproject.toml

$ python my_tool.py
things nothing stuff

$ python typer_config.py others
things nothing others

$ python my_tool.py --config other.toml
something else entirely
```

## How it works

This works by mutating the default values in the [underlying click context](https://click.palletsprojects.com/en/8.1.x/api/#context) (`click.Context.default_map`) before the command is executed.
It is essentially overwriting the default values that you specified in your source code.
> **Note**: You _must_ use `is_eager=True` in the parameter definition because that will cause it to be processed first.
  If you don't use `is_eager`, then your parameter values will depend on the order in which they were processed (read: unpredictably).