# Known Issues

This is a collection of known issues and workarounds to address them.

## Argument list in config

> Related GitHub issues: [typer-config#117](https://github.com/maxb2/typer-config/issues/117), [typer-config#124](https://github.com/maxb2/typer-config/issues/124).

Providing values for a list argument in a config file doesn't work out of the box.
You must use a custom callback for list arguments to extract the values from the config.
Thanks to [@jlwhelan28](https://github.com/jlwhelan28) for the initial solution to this problem.
Below is a working example of how to deal with an argument list:

```{.python title="arg_list.py" test="true"}
from typing import List
import typer
from typer_config import use_yaml_config
from typer_config.callbacks import argument_list_callback

app = typer.Typer()


@app.command()
@use_yaml_config()
def main(
    name: str,
    nicknames: List[str] = typer.Argument(default=None, callback=argument_list_callback),
    greeting: str = typer.Option(...),
    suffix: str = typer.Option("!"),
):
    typer.echo(f"{greeting}, {name}{suffix}")
    typer.echo(f"{nicknames}")


if __name__ == "__main__":
    app()
```

```yaml title="config.yml"
# config.yml
greeting: "Hello"
suffix: "!"
name: "World"
nicknames: ["Globe", "Earth", "Terra"]
```

```{.bash title="Terminal"}
$ python arg_list.py --config config.yml
Hello, World!
['Globe', 'Earth', 'Terra']

$ python arg_list.py Friend Buddy Pal Mate --config config.yml
Hello, Friend!
['Buddy', 'Pal', 'Mate']
```

<!---
```{.python exec="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

result = RUNNER.invoke(app, ["--config", "config.yml"])
assert result.exit_code == 0, "Custom Types without Annotated[] failed!"
```
--->
