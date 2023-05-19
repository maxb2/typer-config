# Simple YAML Example

This simple example uses a `--config` option to load a configuration from a YAML file.

An example typer app:
```python title="simple_app.py"
import typer
from typer_config import yaml_conf_callback

app = typer.Typer( )

@app.command()
def main(
    arg1: str,
    config: str = typer.Option(
        "",
        callback=yaml_conf_callback,
        is_eager=True,  # THIS IS REALLY IMPORTANT (1)
    ),
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
```

1. You _must_ use `is_eager=True` in the parameter definition because that will cause it to be processed first.
   If you don't use `is_eager`, then your parameter values will depend on the order in which they were processed (read: unpredictably).

With a config file:

```yaml title="config.yml"
arg1: stuff
opt1: things
opt2: nothing
```

And invoked with python:

```bash
$ python simple_app.py --config config.yml
things nothing stuff

$ python simple_app.py --config config.yml others
things nothing others

$ python simple_app.py --config config.yml --opt1 people
people nothing stuff
```

> **Note**: this package also provides `json_conf_callback`, `toml_conf_callback`, and `dotenv_conf_callback` for those file formats.
