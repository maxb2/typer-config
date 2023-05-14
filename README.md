# typer-config

This is a collection of utilities to use configuration files to set parameters for a [typer](https://github.com/tiangolo/typer) CLI.
It is useful for typer commands with many options/arguments so you don't have to constantly rewrite long commands.
This package was inspired by [phha/click_config_file](https://github.com/phha/click_config_file) and prototyped in [this issue](https://github.com/tiangolo/typer/issues/86#issuecomment-996374166). It allows you to set values for CLI parameters using a configuration file. 

## Installation

```bash
$ pip install typer-config[all]
```

> **Note**: that will include libraries for reading from YAML and TOML files as well.
  Feel free to leave off the optional dependencies if you don't need YAML or TOML capabilities.

## Usage

```bash
# Long commands like this:
$ my-typer-app --opt1 foo --opt2 bar arg1 arg2

# Can become this:
$ my-typer-app --config config.yml
```

See the [documentation](https://maxb2.github.io/typer-config/examples/) for more examples using typer-config.