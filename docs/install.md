# Installation

```bash
$ pip install typer-config
```

> **Note**: this only supports reading json files. See below for more file formats.

## Optional dependencies

Typer Config provides optional dependency sets to read certain file type:

```bash
$ pip install typer-config[yaml] # includes pyyaml

$ pip install typer-config[toml] # includes toml

$ pip install typer-config[python-dotenv] # includes python-dotenv

$ pip install typer-config[all] # includes all optional dependencies
```