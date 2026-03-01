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
    name: str
    greeting: str
    suffix: str


def validator_loader(param_value: str) -> dict[str, Any]:
    conf = yaml_loader(param_value)
    AppConfig.model_validate(conf)  # raises an exception if not valid
    return conf


validator_callback = conf_callback_factory(validator_loader)

app = typer.Typer()


@app.command()
@use_config(validator_callback)
def main(
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
):
    typer.echo(f"{greeting}, {name}{suffix}")


if __name__ == "__main__":
    app()
```

With a config file:

```yaml title="config.yml"
name: World
greeting: Hello
suffix: "!"
```

And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py --config config.yml
Hello, World!

$ python simple_app.py --config config.yml Alice
Hello, Alice!

$ python simple_app.py --config config.yml --greeting Hi
Hi, World!
```



<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

conf = "config.yml"


result = RUNNER.invoke(app, ["--config", conf])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "Hello, World!", f"Unexpected output for {conf}"


result = RUNNER.invoke(app, ["--config", conf, "Alice"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "Hello, Alice!", f"Unexpected output for {conf}"

result = RUNNER.invoke(app, ["--config", conf, "--greeting", "Hi"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "Hi, World!", f"Unexpected output for {conf}"
```
--->
