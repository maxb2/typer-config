# Pydantic Validation Example

This simple example uses a `--config` option to load a configuration from a YAML file and uses [pydantic](https://pydantic.dev/) to validate the file before continuing.

An example typer app:
```python title="simple_app.py"
from typing import Any, Dict
from typing_extensions import Annotated

from pydantic import BaseModel
import typer
from typer_config.loaders import yaml_loader
from typer_config.callbacks import conf_callback_factory
from typer_config.decorators import use_config


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
@use_config(validator_callback)
def main(
    arg1: str,
    opt1: Annotated[str, typer.Option()],
    opt2: Annotated[str, typer.Option()] = "hello",
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

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
