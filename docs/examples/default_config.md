# Default Config File Example

This example loads a configuration from a default YAML file if `--config` is not given.

An example typer app:
```{.python title="simple_app.py" test="true"}
from typing_extensions import Annotated

import typer
from typer_config.decorators import use_yaml_config  # other formats available (1)

app = typer.Typer()


@app.command()
@use_yaml_config(default_value="config.yml")
def main(
    name: str,
    greeting: Annotated[str, typer.Option()],
    suffix: Annotated[str, typer.Option()] = "!",
):
    typer.echo(f"{greeting}, {name}{suffix}")


if __name__ == "__main__":
    app()
```

1. This package also provides `use_json_config`, `use_toml_config`, `use_ini_config`, and `use_dotenv_config` for those file formats.
   > Note that since INI requires a top-level section `use_ini_config` requires a list of strings that express the path to the section
   you wish to use, e.g. `@use_ini_config(["section", "subsection", ...])`.

With a config file:

```yaml title="config.yml"
name: World
greeting: Hello
suffix: "!"
```

<!--- This is here for the doc tests to pass.
```yaml title="other.yml"
name: Alice
greeting: Hi
suffix: "!!"
```
--->

And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py
Hello, World!

$ python simple_app.py Alice
Hello, Alice!

$ python simple_app.py --greeting Hi
Hi, World!

$ python simple_app.py --config other.yml
Hi, Alice!!
```



<!---
```{.python test="true" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

conf = "config.yml"


result = RUNNER.invoke(app)

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "Hello, World!", f"Unexpected output for {conf}"


result = RUNNER.invoke(app, ["Alice"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "Hello, Alice!", f"Unexpected output for {conf}"

result = RUNNER.invoke(app, ["--greeting", "Hi"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert result.stdout.strip() == "Hi, World!", f"Unexpected output for {conf}"
```
--->