"""Test Config Dumpers."""

from enum import Enum
from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

import typer_config
import typer_config.decorators as tcdec

RUNNER = CliRunner()

HERE = Path(__file__).parent.absolute()


class Things(Enum):
    """Dummy Enum."""

    a = "a"
    b = "b"
    c = "c"


@pytest.fixture()
def dumper_app():
    """Dumper Typer App Fixture."""

    def _app(dump, location):
        app = typer.Typer()

        @app.command()
        @dump(location)
        def main(
            arg1: str,
            config: str = typer.Option(
                "",
                is_eager=True,  # THIS IS REALLY IMPORTANT
            ),
            opt1: str = typer.Option(...),
            opt2: str = typer.Option("hello"),
            things: Things = typer.Option(Things.a.value),
        ):
            typer.echo(f"{opt1} {opt2} {arg1}")

        return app

    return _app


DUMPERS = [
    (
        tcdec.dump_json_config,
        HERE.joinpath("saved.json"),
        typer_config.loaders.json_loader,
    ),
    (
        tcdec.dump_yaml_config,
        HERE.joinpath("saved.yaml"),
        typer_config.loaders.yaml_loader,
    ),
    (
        tcdec.dump_toml_config,
        HERE.joinpath("saved.toml"),
        typer_config.loaders.toml_loader,
    ),
]


@pytest.mark.parametrize("dumper", DUMPERS, ids=str)
def test_dump_config(dumper_app, dumper):
    """Test dump config.

    Args:
        dumper_app: dumper app factory
        dumper: test tuple
    """

    dump, location, loader = dumper

    _app = dumper_app(dump, location)

    result = RUNNER.invoke(_app, ["--help"])
    assert (
        result.exit_code == 0
    ), f"Couldn't get to `--help` for {location}\n\n{result.stdout}"

    result = RUNNER.invoke(
        _app, ["--opt1", "foo", "--opt2", "bar", "baz", "--things", "b"]
    )
    assert result.exit_code == 0, f"Dumping failed for {location}\n\n{result.stdout}"
    assert result.stdout.strip() == "foo bar baz", f"Unexpected output for {location}"

    assert location.is_file(), f"{location} file should exist"

    assert loader(location) == {
        "config": "",
        "opt1": "foo",
        "opt2": "bar",
        "arg1": "baz",
        "things": "b",
    }, f"{location} does not match original parameters"

    location.unlink()
