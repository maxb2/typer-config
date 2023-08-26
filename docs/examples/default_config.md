# Default Config File Example

This example loads a configuration from a default YAML file if `--config` is not given.

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config.decorators import use_yaml_config  # other formats available (1)

app = typer.Typer()


@app.command()
@use_yaml_config(default_value="config.yml")
def main(
    arg1: str,
    opt1: Annotated[str, typer.Option()],
    opt2: Annotated[str, typer.Option()] = "hello",
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

1. This package also provides `use_json_config`, `use_toml_config`, and `use_dotenv_config` for those file formats.

With a config file:

```yaml title="config.yml"
arg1: stuff
opt1: things
opt2: nothing
```

<!--- This is here for the doc tests to pass.
```yaml title="other.yml"
arg1: baz
opt1: foo
opt2: bar
```
--->

And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py # these all use config.yml by default
things nothing stuff

$ python simple_app.py others
things nothing others

$ python simple_app.py --opt1 people
people nothing stuff

$ python simple_app.py --config other.yml # use a different config
foo bar baz
```



<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

conf = "config.yml"


result = RUNNER.invoke(app)

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "things nothing stuff", f"Unexpected output for {conf}"


result = RUNNER.invoke(app, ["others"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "things nothing others", f"Unexpected output for {conf}"

result = RUNNER.invoke(app, ["--opt1", "people"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "people nothing stuff", f"Unexpected output for {conf}"
```
--->