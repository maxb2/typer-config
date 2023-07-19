# Pyproject TOML loader

If you use an unsupported file format or need to do extra processing of the file, you can make your own file loader and construct an appropriate callback.

Suppose you want to specify parameters in a section of `pyproject.toml`:

```toml title='pyproject.toml'
[tool.my_tool.parameters]
arg1 = "stuff"
opt1 = "things"
opt2 = "nothing"
```

<!--- This is here for the doc tests to pass.
```toml title='other.toml'
[tool.my_tool.parameters]
arg1 = "entirely"
opt1 = "something"
opt2 = "else"
```
--->

Then, we can read the values in our typer CLI:

```python title="my_tool.py"
from typing import Any, Dict
from typing_extensions import Annotated

import typer
from typer_config import conf_callback_factory
from typer_config.loaders import toml_loader
from typer_config.decorators import use_config


def pyproject_loader(param_value: str) -> Dict[str, Any]:
    if not param_value:  # set a default path to read from
        param_value = "pyproject.toml"
    pyproject = toml_loader(param_value)
    conf = pyproject["tool"]["my_tool"]["parameters"]
    return conf


### You can define the same loader using the loader_transformer combinator:
#
# from typer_config.loaders import loader_transformer

# pyproject_loader = loader_transformer(
#     toml_loader,
#     param_transformer=lambda param: param or "pyproject.toml",
#     config_transformer=lambda config: config["tool"]["my_tool"]["parameters"],
# )

pyproject_callback = conf_callback_factory(pyproject_loader)

app = typer.Typer()


@app.command()
@use_config(pyproject_callback)
def main(
    arg1: str,
    opt1: Annotated[str, typer.Option()],
    opt2: Annotated[str, typer.Option()] = "hello",
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

And we get this behavior:

```bash
$ ls .
my_tool.py
other.toml
pyproject.toml

$ python my_tool.py
things nothing stuff

$ python my_tool.py others
things nothing others

$ python my_tool.py --config other.toml
something else entirely
```

<!--- Test the combinator

```python title="my_tool.py"
from typing import Any, Dict
from typing_extensions import Annotated

import typer
from typer_config import conf_callback_factory
from typer_config.loaders import toml_loader
from typer_config.decorators import use_config


### You can define the same loader using the loader_transformer combinator:
#
from typer_config.loaders import loader_transformer

pyproject_loader = loader_transformer(
    toml_loader,
    param_transformer=lambda param: param or "pyproject.toml",
    config_transformer=lambda config: config["tool"]["my_tool"]["parameters"],
)

pyproject_callback = conf_callback_factory(pyproject_loader)

app = typer.Typer()


@app.command()
@use_config(pyproject_callback)
def main(
    arg1: str,
    opt1: Annotated[str, typer.Option()],
    opt2: Annotated[str, typer.Option()] = "hello",
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

```bash
$ ls .
my_tool.py
other.toml
pyproject.toml

$ python my_tool.py
things nothing stuff

$ python my_tool.py others
things nothing others

$ python my_tool.py --config other.toml
something else entirely
```
--->