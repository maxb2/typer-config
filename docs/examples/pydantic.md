# Pydantic Validation Example

> **Note:** This example uses an older and more verbose syntax. See [Decorator Syntax](/examples/decorator) for a cleaner way to write this.

This simple example uses a `--config` option to load a configuration from a YAML file and uses [pydantic](https://pydantic.dev/) to validate the file before continuing.

An example typer app:
```python title="simple_app.py"
from typing import Any, Dict
from typing_extensions import Annotated

from pydantic import BaseModel
import typer
from typer_config import yaml_loader, conf_callback_factory


class AppConfig(BaseModel):
    arg1: str
    opt1: str
    opt2: str


def validator_loader(param_value: str) -> Dict[str, Any]:
    conf = yaml_loader(param_value)
    AppConfig.validate(conf)  # raises an exception if not valid
    return conf


validator_callback = conf_callback_factory(validator_loader)

app = typer.Typer()


@app.command()
def main(
    arg1: str,
    opt1: Annotated[str, typer.Option()],
    opt2: Annotated[str, typer.Option()] = "hello",
    config: Annotated[
        str,
        typer.Option(
            callback=validator_callback,
            is_eager=True,  # THIS IS REALLY IMPORTANT (1)
        ),
    ] = "",
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

1. You _must_ use `is_eager=True` in the parameter definition because that will cause it to be processed first.
   If you don't use `is_eager`, then your parameter values will depend on the order in which they were processed (read: unpredictably).

With a config file:

```yaml title="config.yml"
arg1: stuff
opt1: things
opt2: nothing
```

And invoked with python:

```bash
$ python simple_app.py --config config.yml
things nothing stuff

$ python simple_app.py --config config.yml others
things nothing others

$ python simple_app.py --config config.yml --opt1 people
people nothing stuff
```

> **Note**: this package also provides `json_conf_callback`, `toml_conf_callback`, and `dotenv_conf_callback` for those file formats.
