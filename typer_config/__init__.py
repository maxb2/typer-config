import typer
import yaml

def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    if value:
        typer.echo(f"Loading config file: {value}")
        try: 
            with open(value, 'r') as f:    # Load config file
                conf = yaml.safe_load(f)
            ctx.default_map = ctx.default_map or {}   # Initialize the default map
            ctx.default_map.update(conf)   # Merge the config dict into default_map
        except Exception as ex:
            raise typer.BadParameter(str(ex))
    return value