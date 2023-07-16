import typer

from typer_config.decorators import yaml_config

app = typer.Typer()


@app.command()
@yaml_config(param_name="cfg")
def main(
    arg1: str,
    opt1: str = typer.Option(...),
    opt2: str = typer.Option("hello"),
):
    typer.echo(f"{opt1} {opt2} {arg1}")


if __name__ == "__main__":
    app()
