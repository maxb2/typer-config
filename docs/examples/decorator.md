# Decorator Syntax

**New in [0.6.0](https://github.com/maxb2/typer-config/releases/tag/0.6.0)**

You can use a decorator to indicate that your `typer` command uses a config option.
This is meant to reduce boiler-plate code (compare to the [verbose example](/examples/simple_yaml)).

## Simple YAML Example

An example typer app:
```{.python title="simple_app.py" test="true"}
import typer
from typer_config import use_yaml_config

app = typer.Typer()


@app.command()
@use_yaml_config() # MUST BE AFTER @app.command() (1)
def main(
    arg1: str,
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

1. The `app.command()` decorator registers the function object in a lookup table, so we must transform our command before registration.

This dynamically injects the `config` parameter into your command's signature such that `typer` is aware of it when parsing the command line.
The `@use_*_config()` decorators take extra parameters, `param_name` and `param_help` to customize the appearance of the config parameter in the `typer` help menu. See the [API reference](/api/#typer_config.decorators.use_config) for more details.

And for the sake of completeness, it works the same as the other example:

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

> **Note**: this package also provides `use_json_config`, `use_toml_config`, and `use_dotenv_config` for those file formats.

<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

conf = "config.yml"


result = RUNNER.invoke(app, ["--config", conf])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert (
    result.stdout.strip() == "things nothing stuff"
), f"Unexpected output for {conf}"


result = RUNNER.invoke(app, ["--config", conf, "others"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert (
    result.stdout.strip() == "things nothing others"
), f"Unexpected output for {conf}"

result = RUNNER.invoke(app, ["--config", conf, "--opt1", "people"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert (
    result.stdout.strip() == "people nothing stuff"
), f"Unexpected output for {conf}"

```
--->

## Save Config Files

This example lets you save the parameters of the invoked command to a configuration file using the `@dump_config` decorator which operates on Typer commands (requested in [issue #25](https://github.com/maxb2/typer-config/issues/25)).

An example typer app:
```{.python title="simple_app.py" test="true"}
import typer
from typer_config import json_conf_callback
from typer_config.decorators import dump_config
from typer_config.dumpers import json_dumper


app = typer.Typer()

@app.command()
@dump_config(json_dumper, "./saved.json") # MUST BE AFTER app.command() (2)
def main(
    arg1: str,
    config: str = typer.Option(
        "",
        callback=json_conf_callback,
        is_eager=True,  # THIS IS REALLY IMPORTANT (1)
    ),
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

1. You _must_ use `is_eager=True` in the parameter definition because that will cause it to be processed first.
   If you don't use `is_eager`, then your parameter values will depend on the order in which they were processed (read: unpredictably).

2. The `app.command()` decorator registers the function object in a lookup table, so we must transform our command before registration.

And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py --opt1 foo --opt2 bar baz
foo bar baz

$ cat ./saved.json
{"arg1": "baz", "config": "", "opt1": "foo", "opt2": "bar"}
```

> **Note**: this package also provides `yaml_dumper` and `toml_dumper` for those file formats.

<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

import json, os

RUNNER = CliRunner()

result = RUNNER.invoke(app, ["--opt1", "foo", "--opt2", "bar", "baz"])

assert result.exit_code == 0, "Application failed"
assert (
    result.stdout.strip() == "foo bar baz"
), "Unexpected output"


assert os.path.isfile("./saved.json"), "Saved file does not exist"

with open("./saved.json", "r") as f:
    assert json.load(f) == {"opt1": "foo", "config": "", "opt2": "bar", "arg1": "baz"}, "Saved file has wrong contents"

```
--->