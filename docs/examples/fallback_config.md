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
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
):
    typer.echo(f"{greeting}, {name}{suffix}")


if __name__ == "__main__":
    app()
```

With a default config file (local.yml doesn't exist in this example):

```yaml title="default.yml"
name: World
greeting: Hello
suffix: "!"
```

Since `local.yml` doesn't exist, `default.yml` is used:

```{.bash title="Terminal"}
$ python simple_app.py
Hello, World!

$ python simple_app.py --greeting Hi
Hi, World!
```

Now if we create a local config, it takes priority:

```yaml title="local.yml"
name: Team
greeting: Hey
suffix: "!!"
```

```{.bash title="Terminal (with local.yml)"}
$ python simple_app.py
Hey, Team!!
```

The `--config` option always takes priority over the fallback list:

```yaml title="override.yml"
name: Boss
greeting: Yo
suffix: "!!!"
```

```{.bash title="Terminal (with --config)"}
$ python simple_app.py --config override.yml
Yo, Boss!!!
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
assert result.stdout.strip() == "Hey, Team!!", f"Unexpected output: {result.stdout}"


result = RUNNER.invoke(app, ["--greeting", "Hi"])

assert result.exit_code == 0, f"Loading failed\n\n{result.stdout}"
assert result.stdout.strip() == "Hi, Team!!", f"Unexpected output: {result.stdout}"

result = RUNNER.invoke(app, ["--config", "override.yml"])

assert result.exit_code == 0, f"Loading failed\n\n{result.stdout}"
assert result.stdout.strip() == "Yo, Boss!!!", f"Unexpected output: {result.stdout}"
```
--->