import typer

from typer_config import yaml_conf_callback
from typer_config.decorators import use_config

app = typer.Typer()


@app.command()
@use_config(yaml_conf_callback)
def main(
    arg1: str,
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
