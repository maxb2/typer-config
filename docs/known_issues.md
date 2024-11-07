# Known Issues

This is a collection of known issues and workarounds to address them.

## Argument list in config

> Related GitHub issues: [typer-config#117](https://github.com/maxb2/typer-config/issues/117), [typer-config#124](https://github.com/maxb2/typer-config/issues/124).

Providing values for a list argument in a config file doesn't work out of the box.
You must use a custom callback for list arguments to extract the values from the config.
Thanks to [@jlwhelan28](https://github.com/jlwhelan28) for the inital solution to this problem.
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
    arg1: str,
    arg2: List[str] = typer.Argument(default=None, callback=argument_list_callback),
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    typer.echo(f"{opt1} {opt2} {arg1}")
    typer.echo(f"{arg2}")


if __name__ == "__main__":
    app()
```

```yaml title="config.yml"
# config.yml
opt1: "apple"
opt2: "pear"
arg1: "lemon"
arg2: ["oak", "aspen", "maple"]
```

```{.bash title="Terminal"}
$ python arg_list.py --config config.yml
apple pear lemon
['oak', 'aspen', 'maple']

$ python arg_list.py strawberry bear wolf snake tiger --config config.yml
apple pear strawberry
['bear', 'wolf', 'snake', 'tiger']
```

## Custom Types with `Annotated` and `from __future__ import annotations`

> Related Github issue: [typer-config#295](https://github.com/maxb2/typer-config/issues/295).
> Thanks to [@ElliottKasoar](https://github.com/ElliottKasoar) for catching this!

When [custom types](https://typer.tiangolo.com/tutorial/parameter-types/custom-types/) are combined with annotations, a `RuntimeError` is thrown.
This is because `from __future__ import annotations` converts all annotations to strings at runtime, but the `click` parser needs the class at runtime.
The `eval_str` option was added to `inspect.signature()` in python 3.10 to fix this, however there is no solution for 3.9.

```{.python title="annotated.py"}
from __future__ import annotations

from typing_extensions import Annotated

import typer
from typer_config import use_yaml_config


class CustomClass:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"<CustomClass: value={self.value}>"


def parse_custom_class(value: str):
    return CustomClass(value * 2)


# NOTE: only works for python 3.10+
FooType = Annotated[CustomClass, typer.Argument(parser=parse_custom_class)]

app = typer.Typer()


@app.command()
@use_yaml_config()
def main(foo: FooType = 1):
    print(foo)


if __name__ == "__main__":
    app()
```

```{.bash title="Terminal" exec="false"}
# fails for python 3.9 or below
$ python3.9 annotated.py foo
RuntimeError: ...

# works for python 3.10 or above
$ python3.10 annotated.py foo
<CustomClass: value=foofoo>
```

<!---
```{.python exec="true" write="false"}
from typer.testing import CliRunner

import sys

RUNNER = CliRunner()


if sys.version_info < (3, 10):
    try:
        result = RUNNER.invoke(app, ["foo"])
        raise Exception("Should have failed!")
    except RuntimeError:
        pass
else:
    result = RUNNER.invoke(app, ["foo"])
    assert result.exit_code == 0, "Custom Types with Annotated[] failed!"
    assert (
        result.stdout.strip() == "<CustomClass: value=foofoo>"
    ), f"Unexpected output for Annotated[] example"
```
--->

Alternatively, you can use the non-annotated way to define typer arguments/options:

```{.python title="non-annotated.py"}
from __future__ import annotations

from typing_extensions import Annotated

import typer
from typer_config import use_yaml_config


class CustomClass:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"<CustomClass: value={self.value}>"


def parse_custom_class(value: str):
    return CustomClass(value * 2)


app = typer.Typer()


@app.command()
@use_yaml_config()
def main(foo: CustomClass = typer.Argument(parser=parse_custom_class)):
    print(foo)


if __name__ == "__main__":
    app()
```

```{.bash title="Terminal"}
# works for  all python versions
$ python non-annotated.py foo
<CustomClass: value=foofoo>
```

<!---
```{.python exec="true" write="false"}
from typer.testing import CliRunner

import sys

RUNNER = CliRunner()

result = RUNNER.invoke(app, ["foo"])
assert result.exit_code == 0, "Custom Types without Annotated[] failed!"
assert (
    result.stdout.strip() == "<CustomClass: value=foofoo>"
), f"Unexpected output for non-annotated example"
```
--->
