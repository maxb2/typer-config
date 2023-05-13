# Introduction

This is a collection of utilities to use configuration files to set parameters for a [typer](https://github.com/tiangolo/typer) CLI.
It is useful for typer commands with many options/arguments so you don't have to constantly rewrite long commands.
This package was inspired by [phha/click_config_file](https://github.com/phha/click_config_file) and prototyped in [this issue](https://github.com/tiangolo/typer/issues/86#issuecomment-996374166). It allows you to set values for CLI parameters using a configuration file. 

## Installation

```bash
$ pip install typer-config[all]
```

> **Note**: that will include libraries for reading from YAML and TOML files as well.
  Feel free to leave off the optional dependencies if you don't need YAML or TOML capabilities.

## How it works

This works by mutating the default values in the [underlying click context](https://click.palletsprojects.com/en/8.1.x/api/#context) (`click.Context.default_map`) before the command is executed.
It is essentially overwriting the default values that you specified in your source code.
> **Note**: You _must_ use `is_eager=True` in the parameter definition because that will cause it to be processed first.
  If you don't use `is_eager`, then your parameter values will depend on the order in which they were processed (read: unpredictably).