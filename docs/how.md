# How it works

This library works by mutating the default values in the [underlying click context](https://click.palletsprojects.com/en/8.1.x/api/#context) (`click.Context.default_map`) before the command is executed (see [phha/click_config_file](https://github.com/phha/click_config_file)).
It is essentially overwriting the default values that you specified in your source code. Then, the shell environment variables and CLI parameters are parsed by typer to override the values already set.

The `@use_config` decorator works by modifying your function's signature to include a `config` parameter with a sane default.
The `typer` library then sees this extended signature and parses/generates the help text for the `config` parameter.
Internally, the decorator then removes the `config` parameter from the arguments passed to the actual implementation that you wrote.
Otherwise, your function would error with an unknown argument.

If you use the `config` parameter directly in your function, you **must** use `is_eager=True` in the parameter definition because that will cause it to be processed first.
For example:
```python
config: str = typer.Option("", is_eager=True, callback=...)
```
If you don't use `is_eager`, then your parameter values will depend on the order in which they were processed (read: unpredictably).