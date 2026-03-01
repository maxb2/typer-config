# Pydantic Validation Example

This simple example uses a `--config` option to load a configuration from a YAML file and uses [pydantic](https://pydantic.dev/) to validate the file before continuing.

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing import Any
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


def validator_loader(param_value: str) -> dict[str, Any]:
    conf = yaml_loader(param_value)
    AppConfig.model_validate(conf)  # raises an exception if not valid
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

```{.bash title="Terminal"}
$ python simple_app.py --config config.yml
things nothing stuff

$ python simple_app.py --config config.yml others
things nothing others

$ python simple_app.py --config config.yml --opt1 people
people nothing stuff
```



<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

conf = "config.yml"


result = RUNNER.invoke(app, ["--config", conf])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "things nothing stuff", f"Unexpected output for {conf}"


result = RUNNER.invoke(app, ["--config", conf, "others"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "things nothing others", f"Unexpected output for {conf}"

result = RUNNER.invoke(app, ["--config", conf, "--opt1", "people"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "people nothing stuff", f"Unexpected output for {conf}"
```
--->
