from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

import typer_config

RUNNER = CliRunner()

HERE = Path(__file__).parent.absolute()


@pytest.fixture
def simple_app():
    def _app(callback):
        app = typer.Typer()

        @app.command()
        def main(
            arg1: str,
            config: str = typer.Option(
                "",
                callback=callback,
                is_eager=True,  # THIS IS REALLY IMPORTANT
            ),
            opt1: str = typer.Option(...),
            opt2: str = typer.Option("hello"),
        ):
            typer.echo(f"{opt1} {opt2} {arg1}")

        return app

    return _app


def test_simple_example(simple_app):
    # All the formats and their callbacks
    confs = [
        (str(HERE.joinpath("config.yml")), typer_config.yaml_conf_callback),
        (str(HERE.joinpath("config.json")), typer_config.json_conf_callback),
        (str(HERE.joinpath("config.toml")), typer_config.toml_conf_callback),
    ]

    # Test all the combinations of formats and extra parameters
    for conf, callback in confs:
        _app = simple_app(callback)

        result = RUNNER.invoke(_app, ["--config", conf])

        assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
        assert (
            result.stdout.strip() == "things nothing stuff"
        ), f"Unexpected output for {conf}"

        result = RUNNER.invoke(_app, ["--config", conf, "others"])

        assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
        assert (
            result.stdout.strip() == "things nothing others"
        ), f"Unexpected output for {conf}"

        result = RUNNER.invoke(_app, ["--config", conf, "--opt1", "people"])

        assert result.exit_code == 0, f"Loading failed for {conf}\n\n{result.stdout}"
        assert (
            result.stdout.strip() == "people nothing stuff"
        ), f"Unexpected output for {conf}"


def test_pyproject_example(simple_app):
    from typer_config.loaders import default_value_loader, subpath_loader, toml_loader

    pyproject_loader = subpath_loader(
        default_value_loader(toml_loader, lambda: str(HERE.joinpath("pyproject.toml"))),
        ["tools", "my_tool", "parameters"],
    )

    pyproject_callback = typer_config.conf_callback_factory(pyproject_loader)

    _app = simple_app(pyproject_callback)

    result = RUNNER.invoke(_app)

    assert result.exit_code == 0, f"{result.stdout}"
    assert result.stdout.strip() == "things nothing stuff"

    result = RUNNER.invoke(_app, ["others"])

    assert result.exit_code == 0, f"{result.stdout}"
    assert result.stdout.strip() == "things nothing others"

    result = RUNNER.invoke(_app, ["--opt1", "people"])

    assert result.exit_code == 0, f"{result.stdout}"
    assert result.stdout.strip() == "people nothing stuff"

    result = RUNNER.invoke(_app, ["--config", str(HERE.joinpath("other.toml"))])

    assert result.exit_code == 0, f"{result.stdout}"
    assert result.stdout.strip() == "something else entirely"
