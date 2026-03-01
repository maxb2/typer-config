# Explicit Configuration Parameter

Instead of using the `@use_config()` decorator, you can explicitly add `config` to your typer command.
However, you **must** include `is_eager=True`.

## Simple YAML Example

This simple example uses a `--config` option to load a configuration from a YAML file.

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config.callbacks import yaml_conf_callback  # other formats available (1)

app = typer.Typer()


@app.command()
def main(
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
    config: Annotated[
        str,
        typer.Option(
            callback=yaml_conf_callback,
            is_eager=True,  # THIS IS REALLY IMPORTANT (2)
        ),
    ] = "",
):
    # possibly do something with config
    typer.echo(f"{greeting}, {name}{suffix}")


if __name__ == "__main__":
    app()
```

1. This package also provides `json_conf_callback`, `toml_conf_callback`, and `dotenv_conf_callback` for those file formats.

2. You _must_ use `is_eager=True` in the parameter definition because that will cause it to be processed first.
   If you don't use `is_eager`, then your parameter values will depend on the order in which they were processed (read: unpredictably).

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