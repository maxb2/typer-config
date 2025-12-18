# Default Multiple Config File Example

This example loads a configuration from a list of default YAML files.
Each file updates the values from the previous one.

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config.decorators import use_multifile_config

app = typer.Typer()


@app.command()
@use_multifile_config(default_files=["config.yml", "config2.yml"])
def main(
    arg1: str,
    opt1: Annotated[str, typer.Option()],
    opt2: Annotated[str, typer.Option()] = "hello",
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

With config files:

```yaml title="config.yml"
arg1: stuff
opt1: things
opt2: nothing
```

```yaml title="config2.yml"
arg1: stuff
opt1: things
opt2: config2
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
$ python simple_app.py
things config2 stuff

$ python simple_app.py others
things config2 others

$ python simple_app.py --opt1 people
people config2 stuff

$ python simple_app.py --opt2 places
things places stuff

$ python simple_app.py --config other.yml
foo bar baz
```



<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

conf = "config.yml"


result = RUNNER.invoke(app)

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "things config2 stuff", f"Unexpected output for {conf}"


result = RUNNER.invoke(app, ["others"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "things config2 others", f"Unexpected output for {conf}"

result = RUNNER.invoke(app, ["--opt1", "people"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "people config2 stuff", f"Unexpected output for {conf}"

result = RUNNER.invoke(app, ["--opt2", "places"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "things places stuff", f"Unexpected output for {conf}"

result = RUNNER.invoke(app, ["--config", "other.yml"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "foo bar baz", f"Unexpected output for {conf}"
```
--->