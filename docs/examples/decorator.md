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