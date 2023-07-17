from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

import typer_config
import typer_config.decorators as tcdec
import typer_config.dumpers as tcdump

RUNNER = CliRunner()

HERE = Path(__file__).parent.absolute()


@pytest.fixture
def dumper_app():
    def _app(dumper, location):
        app = typer.Typer()

        @app.command()
        @tcdec.save_config(dumper, location)
        def main(
            arg1: str,
            config: str = typer.Option(
                "",
                is_eager=True,  # THIS IS REALLY IMPORTANT
            ),
            opt1: str = typer.Option(...),
            opt2: str = typer.Option("hello"),
        ):
            typer.echo(f"{opt1} {opt2} {arg1}")

        return app

    return _app


DUMPERS = [
    (
        tcdump.json_dumper,
        HERE.joinpath("saved.json"),
        typer_config.loaders.json_loader,
    ),
    (
        tcdump.yaml_dumper,
        HERE.joinpath("saved.yaml"),
        typer_config.loaders.yaml_loader,
    ),
    (
        tcdump.toml_dumper,
        HERE.joinpath("saved.toml"),
        typer_config.loaders.toml_loader,
    ),
]


@pytest.mark.parametrize("dumper", DUMPERS, ids=str)
def test_save_config(dumper_app, dumper):
    dumper, location, loader = dumper

    _app = dumper_app(dumper, location)

    result = RUNNER.invoke(_app, ["--help"])
    assert (
        result.exit_code == 0
    ), f"Couldn't get to `--help` for {location}\n\n{result.stdout}"

    result = RUNNER.invoke(_app, ["--opt1", "foo", "--opt2", "bar", "baz"])
    assert result.exit_code == 0, f"Dumping failed for {location}\n\n{result.stdout}"
    assert result.stdout.strip() == "foo bar baz", f"Unexpected output for {location}"

    assert location.is_file(), f"{location} file should exist"

    assert loader(location) == {
        "config": "",
        "opt1": "foo",
        "opt2": "bar",
        "arg1": "baz",
    }, f"{location} does not match original parameters"

    location.unlink()
