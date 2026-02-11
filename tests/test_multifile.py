"""Test Multifile Configuration."""

from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

import typer_config
from typer_config.loaders import multifile_fallback_loader, multifile_loader

RUNNER = CliRunner(mix_stderr=False)

HERE = Path(__file__).parent.absolute()


@pytest.fixture
def multifile_app():
    """Multifile config app fixture."""

    def _app(decorator, **dec_kwargs):
        app = typer.Typer()

        @app.command()
        @decorator(**dec_kwargs)
        def main(
            arg1: str = typer.Argument("default_arg"),
            opt1: str = typer.Option("default_opt1"),
            opt2: str = typer.Option("default_opt2"),
        ):
            typer.echo(f"{opt1} {opt2} {arg1}")

        return app

    return _app


class TestMultifileLoader:
    """Tests for multifile_loader."""

    def test_merge_multiple_files(self):
        """Test merging multiple config files."""
        files = [
            str(HERE / "config.yml"),
            str(HERE / "other.yml"),
        ]
        result = multifile_loader(files)

        # other.yml should override config.yml
        assert result["opt1"] == "foo"
        assert result["opt2"] == "bar"
        assert result["arg1"] == "baz"
        # simple_app from config.yml should remain
        assert "simple_app" in result

    def test_deep_merge(self):
        """Test deep merging of nested dictionaries."""
        files = [
            str(HERE / "nested_base.yml"),
            str(HERE / "nested_override.yml"),
        ]
        result = multifile_loader(files)

        expected_port = 5432

        # Overridden values
        assert result["database"]["host"] == "production.db.example.com"
        assert result["database"]["credentials"]["password"] == "supersecret"
        assert result["logging"]["level"] == "DEBUG"

        # Preserved values from base
        assert result["database"]["port"] == expected_port
        assert result["database"]["credentials"]["username"] == "admin"
        assert result["logging"]["format"] == "simple"

    def test_shallow_merge_option(self):
        """Test shallow merge when deep_merge=False."""
        files = [
            str(HERE / "nested_base.yml"),
            str(HERE / "nested_override.yml"),
        ]
        result = multifile_loader(files, deep_merge=False)

        # Override replaces entire nested dict
        assert result["database"]["host"] == "production.db.example.com"
        assert result["database"]["credentials"]["password"] == "supersecret"
        # These should be gone with shallow merge
        assert "port" not in result["database"]
        assert "username" not in result["database"]["credentials"]

    def test_skip_missing_files(self):
        """Test that missing files are skipped."""
        files = [
            str(HERE / "config.yml"),
            str(HERE / "nonexistent.yml"),
            str(HERE / "other.yml"),
        ]
        result = multifile_loader(files)

        assert result["opt1"] == "foo"

    def test_skip_missing_false_raises(self):
        """Test that skip_missing=False raises error for missing files."""
        files = [
            str(HERE / "nonexistent.yml"),
        ]
        with pytest.raises(FileNotFoundError):
            multifile_loader(files, skip_missing=False)

    def test_empty_file_list(self):
        """Test empty file list returns empty dict."""
        result = multifile_loader([])
        assert result == {}

    def test_skip_empty_paths(self):
        """Test that empty paths are skipped."""
        files = [
            "",
            str(HERE / "config.yml"),
            None,
        ]
        result = multifile_loader(files)
        assert result["opt1"] == "things"


class TestMultifileFallbackLoader:
    """Tests for multifile_fallback_loader."""

    def test_uses_first_existing(self):
        """Test that first existing file is used."""
        files = [
            str(HERE / "nonexistent.yml"),
            str(HERE / "other.yml"),
            str(HERE / "config.yml"),
        ]
        result = multifile_fallback_loader(files)

        # Should use other.yml (first existing)
        assert result["opt1"] == "foo"
        assert result["opt2"] == "bar"
        # Should NOT have simple_app from config.yml
        assert "simple_app" not in result

    def test_no_existing_files(self):
        """Test empty dict when no files exist."""
        files = [
            str(HERE / "nonexistent1.yml"),
            str(HERE / "nonexistent2.yml"),
        ]
        result = multifile_fallback_loader(files)
        assert result == {}

    def test_empty_file_list(self):
        """Test empty file list returns empty dict."""
        result = multifile_fallback_loader([])
        assert result == {}


class TestUseMultifileConfig:
    """Tests for use_multifile_config decorator."""

    def test_merge_configs(self, multifile_app):
        """Test merging multiple config files."""
        app = multifile_app(
            typer_config.decorators.use_multifile_config,
            default_files=[
                str(HERE / "config.yml"),
                str(HERE / "other.yml"),
            ],
        )

        result = RUNNER.invoke(app, [])
        assert result.exit_code == 0, result.stdout
        # other.yml values should override config.yml
        assert result.stdout.strip() == "foo bar baz"

    def test_cli_overrides_config(self, multifile_app):
        """Test CLI args override merged config."""
        app = multifile_app(
            typer_config.decorators.use_multifile_config,
            default_files=[
                str(HERE / "config.yml"),
                str(HERE / "other.yml"),
            ],
        )

        result = RUNNER.invoke(app, ["--opt1", "cli_value"])
        assert result.exit_code == 0, result.stdout
        assert result.stdout.strip() == "cli_value bar baz"

    def test_config_option_appends(self, multifile_app):
        """Test --config option adds to the list."""
        app = multifile_app(
            typer_config.decorators.use_multifile_config,
            default_files=[
                str(HERE / "config.yml"),
            ],
        )

        # --config should override default files
        result = RUNNER.invoke(app, ["--config", str(HERE / "other.yml")])
        assert result.exit_code == 0, result.stdout
        # other.yml is loaded last, so its values take precedence
        assert result.stdout.strip() == "foo bar baz"

    def test_missing_files_skipped(self, multifile_app):
        """Test missing files are skipped."""
        app = multifile_app(
            typer_config.decorators.use_multifile_config,
            default_files=[
                str(HERE / "nonexistent.yml"),
                str(HERE / "config.yml"),
            ],
        )

        result = RUNNER.invoke(app, [])
        assert result.exit_code == 0, result.stdout
        assert result.stdout.strip() == "things nothing stuff"

    def test_section_support(self, multifile_app):
        """Test section parameter."""
        app = multifile_app(
            typer_config.decorators.use_multifile_config,
            default_files=[
                str(HERE / "config.yml"),
            ],
            section=["simple_app"],
        )

        result = RUNNER.invoke(app, [])
        assert result.exit_code == 0, result.stdout
        assert result.stdout.strip() == "things2 nothing2 stuff2"


class TestUseFallbackConfig:
    """Tests for use_fallback_config decorator."""

    def test_uses_first_existing(self, multifile_app):
        """Test first existing file is used."""
        app = multifile_app(
            typer_config.decorators.use_fallback_config,
            fallback_files=[
                str(HERE / "nonexistent.yml"),
                str(HERE / "other.yml"),
                str(HERE / "config.yml"),
            ],
        )

        result = RUNNER.invoke(app, [])
        assert result.exit_code == 0, result.stdout
        # Should use other.yml (first existing)
        assert result.stdout.strip() == "foo bar baz"

    def test_cli_option_takes_priority(self, multifile_app):
        """Test --config option takes priority over fallback list."""
        app = multifile_app(
            typer_config.decorators.use_fallback_config,
            fallback_files=[
                str(HERE / "other.yml"),
            ],
        )

        # --config should be checked before fallback list
        result = RUNNER.invoke(app, ["--config", str(HERE / "config.yml")])
        assert result.exit_code == 0, result.stdout
        assert result.stdout.strip() == "things nothing stuff"

    def test_no_config_uses_defaults(self, multifile_app):
        """Test that no config falls back to CLI defaults."""
        app = multifile_app(
            typer_config.decorators.use_fallback_config,
            fallback_files=[
                str(HERE / "nonexistent1.yml"),
                str(HERE / "nonexistent2.yml"),
            ],
        )

        result = RUNNER.invoke(app, [])
        assert result.exit_code == 0, result.stdout
        assert result.stdout.strip() == "default_opt1 default_opt2 default_arg"

    def test_section_support(self, multifile_app):
        """Test section parameter."""
        app = multifile_app(
            typer_config.decorators.use_fallback_config,
            fallback_files=[
                str(HERE / "config.yml"),
            ],
            section=["simple_app"],
        )

        result = RUNNER.invoke(app, [])
        assert result.exit_code == 0, result.stdout
        assert result.stdout.strip() == "things2 nothing2 stuff2"
