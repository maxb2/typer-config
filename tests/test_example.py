import functools
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


@pytest.fixture
def simple_app_decorated():
    def _app(decorator):
        app = typer.Typer()

        @app.command()
        @decorator()
        def main(
            arg1: str,
            opt1: str = typer.Option(...),
            opt2: str = typer.Option("hello"),
        ):
            typer.echo(f"{opt1} {opt2} {arg1}")

        return app

    return _app


# Have to make one dynamically because of the required INI section
INI_CALLBACK = typer_config.conf_callback_factory(
    typer_config.loaders.loader_transformer(
        typer_config.loaders.subpath_loader(
            typer_config.loaders.ini_loader, ["simple_app"]
        ),
        loader_conditional=lambda param_value: param_value,
    )
)

CONFS = [
    (
        str(HERE.joinpath("config.yml")),
        typer_config.yaml_conf_callback,
        typer_config.decorators.use_yaml_config,
    ),
    (
        str(HERE.joinpath("config.json")),
        typer_config.json_conf_callback,
        typer_config.decorators.use_json_config,
    ),
    (
        str(HERE.joinpath("config.toml")),
        typer_config.toml_conf_callback,
        typer_config.decorators.use_toml_config,
    ),
    (
        str(HERE.joinpath("config.env")),
        typer_config.dotenv_conf_callback,
        typer_config.decorators.use_dotenv_config,
    ),
    (
        str(HERE.joinpath("config.ini")),
        INI_CALLBACK,
        functools.partial(typer_config.decorators.use_config, callback=INI_CALLBACK),
    ),
]


@pytest.mark.parametrize("confs", CONFS, ids=str)
def test_simple_example(simple_app, confs):
    conf, callback, _ = confs
    _app = simple_app(callback)

    result = RUNNER.invoke(_app, ["--help"])
    assert (
        result.exit_code == 0
    ), f"Couldn't get to `--help` for {conf}\n\n{result.stdout}"

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

    result = RUNNER.invoke(_app, ["--config", conf + ".non_existent"])
    assert result.exit_code != 0, f"Should have failed for {conf}\n\n{result.stdout}"
    assert "No such file" in result.stdout, f"Wrong error message for {conf}"


@pytest.mark.parametrize("confs", CONFS, ids=str)
def test_simple_example_decorated(simple_app_decorated, confs):
    conf, _, dec = confs
    _app = simple_app_decorated(dec)

    result = RUNNER.invoke(_app, ["--help"])
    assert (
        result.exit_code == 0
    ), f"Couldn't get to `--help` for {conf}\n\n{result.stdout}"

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

    result = RUNNER.invoke(_app, ["--config", conf + ".non_existent"])
    assert result.exit_code != 0, f"Should have failed for {conf}\n\n{result.stdout}"
    assert "No such file" in result.stdout, f"Wrong error message for {conf}"


def test_pyproject_example_deprecated(simple_app):
    from typer_config.loaders import default_value_loader, subpath_loader, toml_loader

    pyproject_loader = subpath_loader(
        default_value_loader(toml_loader, lambda: str(HERE.joinpath("pyproject.toml"))),
        ["tool", "my_tool", "parameters"],
    )

    pyproject_callback = typer_config.conf_callback_factory(pyproject_loader)

    _app = simple_app(pyproject_callback)

    result = RUNNER.invoke(_app, ["--help"])

    assert result.exit_code == 0, f"{result.stdout}"

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


def test_pyproject_example(simple_app):
    from typer_config.loaders import loader_transformer, toml_loader

    pyproject_loader = loader_transformer(
        toml_loader,
        param_transformer=lambda param: param
        if param
        else str(HERE.joinpath("pyproject.toml")),
        config_transformer=lambda config: config["tool"]["my_tool"]["parameters"],
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
