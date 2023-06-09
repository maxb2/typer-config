# How it works

This works by mutating the default values in the [underlying click context](https://click.palletsprojects.com/en/8.1.x/api/#context) (`click.Context.default_map`) before the command is executed (see [phha/click_config_file](https://github.com/phha/click_config_file)).
It is essentially overwriting the default values that you specified in your source code. Then, the shell environment variables and CLI parameters are parsed by typer to override the values already set.

> **Note**: You _must_ use `is_eager=True` in the parameter definition because that will cause it to be processed first.
  If you don't use `is_eager`, then your parameter values will depend on the order in which they were processed (read: unpredictably).