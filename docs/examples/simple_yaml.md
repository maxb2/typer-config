# Simple YAML Example

This simple example uses a `--config` option to load a configuration from a YAML file.

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config.decorators import use_yaml_config  # other formats available (1)

app = typer.Typer()


@app.command()
@use_yaml_config()
def main(
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
):
    typer.echo(f"{greeting}, {name}{suffix}")


if __name__ == "__main__":
    app()
```

1. This package also provides `use_json_config`, `use_toml_config`, and `use_dotenv_config` for those file formats.

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