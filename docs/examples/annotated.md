# Simple YAML Example

This simple example uses a `--config` option to load a configuration from a YAML file.

An example typer app:
```{.python title="simple_app.py" test="true"}
from __future__ import annotations

from typing_extensions import Annotated

import typer
from typer_config import use_yaml_config  # other formats available


class CustomClass:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"<CustomClass: value={self.value}>"


def parse_custom_class(value: str):
    return CustomClass(value * 2)


FooType = Annotated[CustomClass, typer.Argument(parser=parse_custom_class)]

app = typer.Typer()


@app.command()
@use_yaml_config()
def main(foo: FooType = 1):
    print(foo)


if __name__ == "__main__":
    app()
```

1. This package also provides `use_json_config`, `use_toml_config`, and `use_dotenv_config` for those file formats.

With a config file:

```yaml title="config.yml"
foo: stuff
```

And invoked with python:

```{.bash title="Terminal"}
$ python simple_app.py --config config.yml
<CustomClass: value=stuffstuff>

$ python simple_app.py --config config.yml bar
<CustomClass: value=barbar>
```



<!---
```{.python test="false" write="false"}
from typer.testing import CliRunner

RUNNER = CliRunner()

conf = "config.yml"


result = RUNNER.invoke(app, ["--config", conf])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert (
    result.stdout.strip() == "<CustomClass: value=stuffstuff>"
), f"Unexpected output for {conf}"


result = RUNNER.invoke(app, ["--config", conf, "bar"])

assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
assert (
    result.stdout.strip() == "<CustomClass: value=barbar>"
), f"Unexpected output for {conf}"
```
--->