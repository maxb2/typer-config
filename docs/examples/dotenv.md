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
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
):
    typer.echo(f"{greeting}, {name}{suffix}")


if __name__ == "__main__":
    app()
```

With a config file:

```{.dotenv title="config.env"}
name=World
greeting=Hello
suffix=!
```

And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py --config config.env
Hello, World!

$ python simple_app.py --config config.env Alice
Hello, Alice!

$ python simple_app.py --config config.env --greeting Hi
Hi, World!
```



<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

conf = "config.env"


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