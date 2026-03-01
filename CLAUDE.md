# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**typer-config** is a Python library that provides utilities for using configuration files (YAML, TOML, JSON, INI, .env) to set parameters for [Typer](https://github.com/tiangolo/typer) CLI applications. It works by mutating Click's `context.default_map` before command execution.

## Common Commands

```bash
# Install dependencies
uv sync --all-extras

# Run tests with coverage
make test
# Equivalent: uv run --all-extras pytest --cov=typer_config --cov-report=xml

# Run a single test
uv run --all-extras pytest tests/test_example.py::test_name -v

# Lint and type-check
make check          # ruff + ty
make ruff           # ruff only
make check-types    # ty only

# Format code
make fmt            # isort + black
```

## Architecture

The library is in `src/typer_config/` with this module hierarchy:

- **decorators.py** — Primary user-facing API. Decorators like `use_config()`, `use_yaml_config()`, `use_json_config()`, `use_toml_config()`, `dump_config()`, `use_multifile_config()`, `use_fallback_config()` that attach config-loading behavior to Typer commands.
- **callbacks.py** — Typer parameter callbacks created via `conf_callback_factory()`. These are the mechanism decorators use internally to inject config values into Click's default_map.
- **loaders.py** — Functions that read config files and return `ConfigDict` (a dict). Includes format-specific loaders and `loader_transformer()` for composing transformations (e.g., extracting a subsection).
- **dumpers.py** — Functions that write `ConfigDict` to config file formats (JSON, YAML, TOML).
- **utils.py** — Helpers: `get_dict_section()` for nested dict navigation, file validation.
- **__typing.py** — Type aliases (`ConfigDict`, `ConfigLoader`, `ConfigDumper`, `TyperCommand`, etc.).
- **__optional_imports.py** — Lazy import handling for optional deps (pyyaml, toml, python-dotenv) via `try_import()`.

**Data flow**: Decorator → creates a callback → callback uses a loader to read config → merges into `ctx.default_map` → Typer/Click uses defaults for unspecified CLI params.

## Testable Documentation

Documentation examples in `docs/examples/*.md` and `docs/known_issues.md` are automatically tested via `tests/test_docs.py`. The test infrastructure in `tests/doc_examples.py` (inspired by [mktestdocs](https://github.com/koaning/mktestdocs)) parses fenced code blocks from markdown files and executes them:

- **Python blocks** with a `title` attribute (e.g., `` ```{.python title="app.py"} ``) are written to a temp file and executed.
- **YAML/TOML blocks** with a `title` attribute are written as files in a temp directory.
- **Bash blocks** parse `$ command` / `expected output` pairs and assert the output matches.
- **Hidden test blocks** (inside `<!-- -->` HTML comments) run additional assertions (e.g., using `typer.testing.CliRunner`) without being visible in rendered docs.
- Blocks can opt out of execution with `exec="false"` in their fence attributes.

When editing documentation examples, run `make test` to verify they still execute correctly.

## Code Style

- **Docstrings**: Google style convention (enforced by ruff rule D)
- **Linting**: Ruff with extensive rule set. Tests have relaxed rules (no annotations, security, etc.)
- **Formatting**: black + isort
- **Type checking**: ty (not mypy)
- **Python**: >=3.10, tested on 3.10–3.14

## Build System

Uses `uv` with `uv_build` backend. Dependencies and lock file managed via `uv`. Optional dependency groups: `yaml`, `toml`, `python-dotenv`, `all`.
