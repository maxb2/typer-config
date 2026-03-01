# Inheritance Config Example

This example demonstrates configuration inheritance where multiple config files
are merged together, with later files overriding earlier ones. Nested dictionaries
are deep-merged, preserving keys that aren't explicitly overridden.

This is useful for layered configuration like:
- System defaults (`/etc/myapp.yaml`)
- User overrides (`~/.config/myapp.yaml`)
- Project-local overrides (`./myapp.yaml`)

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config.decorators import use_multifile_config

app = typer.Typer()


@app.command()
@use_multifile_config(default_files=["base_config.yml", "local_config.yml"])
def main(
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
):
    typer.echo(f"{greeting}, {name}{suffix}")


if __name__ == "__main__":
    app()
```

With config files representing different layers:

```yaml title="base_config.yml"
name: World
greeting: Hello
suffix: "!"
```

```yaml title="local_config.yml"
greeting: Hey
```

Note that `local_config.yml` only overrides `greeting`, while `name` and `suffix`
are inherited from `base_config.yml`.

And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py
Hey, World!

$ python simple_app.py --suffix "!!"
Hey, World!!

$ python simple_app.py Alice
Hey, Alice!
```

Missing config files are silently skipped, so you can define optional override
locations:

```{.python exec="false"}
@app.command()
@use_multifile_config(default_files=[
    "/etc/myapp/config.yml",      # system defaults (may not exist)
    "~/.config/myapp/config.yml", # user config (may not exist)
    "./config.yml",               # local config (may not exist)
])
def main(...):
    ...
```


<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()


result = RUNNER.invoke(app)

assert result.exit_code == 0, f"Loading failed\n\n{result.stdout}"
assert result.stdout.strip() == "Hey, World!", f"Unexpected output: {result.stdout}"


result = RUNNER.invoke(app, ["--suffix", "!!"])

assert result.exit_code == 0, f"Loading failed\n\n{result.stdout}"
assert result.stdout.strip() == "Hey, World!!", f"Unexpected output: {result.stdout}"

result = RUNNER.invoke(app, ["Alice"])

assert result.exit_code == 0, f"Loading failed\n\n{result.stdout}"
assert result.stdout.strip() == "Hey, Alice!", f"Unexpected output: {result.stdout}"
```
--->