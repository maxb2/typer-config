# Fallback Config Example

This example demonstrates fallback configuration where the first existing config
file from a list is used. This is useful when you want to check multiple locations
for a config file and use the first one found.

This pattern is similar to how tools like Ansible look for `ansible.cfg`:
- Check current directory first
- Fall back to user's home directory
- Fall back to system-wide config

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config.decorators import use_fallback_config

app = typer.Typer()


@app.command()
@use_fallback_config(fallback_files=["local.yml", "default.yml"])
def main(
    host: Annotated[str, typer.Option()],
    port: Annotated[int, typer.Option()] = 8080,
    debug: Annotated[bool, typer.Option()] = False,
):
    typer.echo(f"Connecting to {host}:{port} (debug={debug})")


if __name__ == "__main__":
    app()
```

With a default config file (local.yml doesn't exist in this example):

```yaml title="default.yml"
host: default.example.com
port: 5432
debug: false
```

Since `local.yml` doesn't exist, `default.yml` is used:

```{.bash title="Terminal"}
$ python simple_app.py
Connecting to default.example.com:5432 (debug=False)

$ python simple_app.py --host custom.example.com
Connecting to custom.example.com:5432 (debug=False)
```

Now if we create a local config, it takes priority:

```yaml title="local.yml"
host: local.example.com
port: 3000
debug: true
```

```{.bash title="Terminal (with local.yml)"}
$ python simple_app.py
Connecting to local.example.com:3000 (debug=True)
```

The `--config` option always takes priority over the fallback list:

```yaml title="override.yml"
host: override.example.com
port: 9000
debug: false
```

```{.bash title="Terminal (with --config)"}
$ python simple_app.py --config override.yml
Connecting to override.example.com:9000 (debug=False)
```

A real-world example with typical config locations:

```{.python exec="false"}
@app.command()
@use_fallback_config(fallback_files=[
    "./myapp.yml",                # local project config (highest priority)
    "~/.config/myapp/config.yml", # user config
    "/etc/myapp/config.yml",      # system config (lowest priority)
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
# local.yml exists and takes priority
assert result.stdout.strip() == "Connecting to local.example.com:3000 (debug=True)", f"Unexpected output: {result.stdout}"


result = RUNNER.invoke(app, ["--host", "custom.example.com"])

assert result.exit_code == 0, f"Loading failed\n\n{result.stdout}"
assert result.stdout.strip() == "Connecting to custom.example.com:3000 (debug=True)", f"Unexpected output: {result.stdout}"

result = RUNNER.invoke(app, ["--config", "override.yml"])

assert result.exit_code == 0, f"Loading failed\n\n{result.stdout}"
assert result.stdout.strip() == "Connecting to override.example.com:9000 (debug=False)", f"Unexpected output: {result.stdout}"
```
--->
