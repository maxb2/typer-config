# Simple YAML Example

> **Note:** This example uses an older and more verbose syntax. See [Decorator Syntax](../decorator) for a cleaner way to write this.

This simple example uses a `--config` option to load a configuration from a YAML file.

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config import yaml_conf_callback # other formats available (1)

app = typer.Typer()


@app.command()
def main(
    arg1: str,
    opt1: Annotated[str, typer.Option()],
    opt2: Annotated[str, typer.Option()] = "hello",
    config: Annotated[
        str,
        typer.Option(
            callback=yaml_conf_callback,
            is_eager=True,  # THIS IS REALLY IMPORTANT (2)
        ),
    ] = "",
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

1. This package also provides `json_conf_callback`, `toml_conf_callback`, and `dotenv_conf_callback` for those file formats.

2. You _must_ use `is_eager=True` in the parameter definition because that will cause it to be processed first.
   If you don't use `is_eager`, then your parameter values will depend on the order in which they were processed (read: unpredictably).

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