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
    host: Annotated[str, typer.Option()],
    port: Annotated[int, typer.Option()] = 8080,
    debug: Annotated[bool, typer.Option()] = False,
):
    typer.echo(f"Connecting to {host}:{port} (debug={debug})")


if __name__ == "__main__":
    app()
```

With config files representing different layers:

```yaml title="base_config.yml"
host: localhost
port: 5432
debug: false
```

```yaml title="local_config.yml"
host: dev.example.com
debug: true
```

Note that `local_config.yml` only overrides `host` and `debug`, while `port`
is inherited from `base_config.yml`.

And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py
Connecting to dev.example.com:5432 (debug=True)

$ python simple_app.py --port 3000
Connecting to dev.example.com:3000 (debug=True)

$ python simple_app.py --host production.example.com
Connecting to production.example.com:5432 (debug=True)
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
assert result.stdout.strip() == "Connecting to dev.example.com:5432 (debug=True)", f"Unexpected output: {result.stdout}"


result = RUNNER.invoke(app, ["--port", "3000"])

assert result.exit_code == 0, f"Loading failed\n\n{result.stdout}"
assert result.stdout.strip() == "Connecting to dev.example.com:3000 (debug=True)", f"Unexpected output: {result.stdout}"

result = RUNNER.invoke(app, ["--host", "production.example.com"])

assert result.exit_code == 0, f"Loading failed\n\n{result.stdout}"
assert result.stdout.strip() == "Connecting to production.example.com:5432 (debug=True)", f"Unexpected output: {result.stdout}"
```
--->
