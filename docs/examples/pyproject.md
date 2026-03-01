# Pyproject TOML loader

If you use an unsupported file format or need to do extra processing of the file, you can make your own file loader and construct an appropriate callback.

Suppose you want to specify parameters in a section of `pyproject.toml`:

```toml title='pyproject.toml'
[tool.my_tool.parameters]
name = "World"
greeting = "Hello"
suffix = "!"
```

<!--- This is here for the doc tests to pass.
```toml title='other.toml'
[tool.my_tool.parameters]
name = "Alice"
greeting = "Hi"
suffix = "!!"
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
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
):
    typer.echo(f"{greeting}, {name}{suffix}")


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
Hello, World!

$ python my_tool.py Alice
Hello, Alice!

$ python my_tool.py --config other.toml
Hi, Alice!!
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
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
):
    typer.echo(f"{greeting}, {name}{suffix}")


if __name__ == "__main__":
    app()
```

```bash
$ ls .
my_tool.py
other.toml
pyproject.toml

$ python my_tool.py
Hello, World!

$ python my_tool.py Alice
Hello, Alice!

$ python my_tool.py --config other.toml
Hi, Alice!!
```
--->