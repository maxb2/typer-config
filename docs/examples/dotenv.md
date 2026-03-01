# Dotenv Example

This simple example uses a `--config` option to load a configuration from a `.env` file.

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config.decorators import use_dotenv_config

app = typer.Typer()


@app.command()
@use_dotenv_config()
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

```{.dotenv title="config.env"}
arg1=stuff
opt1=things
opt2=nothing
```

And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py --config config.env
things nothing stuff

$ python simple_app.py --config config.env others
things nothing others

$ python simple_app.py --config config.env --opt1 people
people nothing stuff
```



<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

conf = "config.env"


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
