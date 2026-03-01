# Save Config Files

This example shows you how save the parameters of the invoked command to a configuration file using the `@dump_config` decorator which operates on Typer commands (requested in [issue #25](https://github.com/maxb2/typer-config/issues/25)).

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config.decorators import (
    dump_json_config,  # other formats available (1)
    use_json_config,
)

app = typer.Typer()


@app.command()
@use_json_config()  # before dump decorator (2)
@dump_json_config("./dumped.json")
def main(
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
):
    typer.echo(f"{greeting}, {name}{suffix}")


if __name__ == "__main__":
    app()
```

1. This package also provides `@dump_yaml_config` and `@dump_toml_config` for those file formats.

2. If you put `@use_json_config` before `@dump_json_config`, you will not capture the `config` parameter in your config dump. You probably want this behavior to avoid cascading config files.


And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py --greeting Hello --suffix "!" World
Hello, World!

$ cat ./dumped.json
{"name": "World", "greeting": "Hello", "suffix": "!"}
```

<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

import json, os

RUNNER = CliRunner()

result = RUNNER.invoke(app, ["--greeting", "Hello", "--suffix", "!", "World"])

assert result.exit_code == 0, "Application failed"
assert result.stdout.strip() == "Hello, World!", "Unexpected output"


assert os.path.isfile("./dumped.json"), "Saved file does not exist"

with open("./dumped.json", "r") as f:
    assert json.load(f) == {
        "greeting": "Hello",
        "suffix": "!",
        "name": "World",
    }, "Saved file has wrong contents"
```
--->