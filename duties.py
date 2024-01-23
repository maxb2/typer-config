"""Project Duties."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional, Tuple

from duty import duty
from duty.callables import blacken_docs, mkdocs, mypy
from git_changelog.cli import build_and_render

if TYPE_CHECKING:
    from duty.context import Context
    from git_changelog import Changelog

CI = os.environ.get("CI", "0") in {"1", "true", "yes", ""}
WINDOWS = os.name == "nt"
PTY = not WINDOWS and not CI


def _changelog() -> Tuple[Changelog, str]:
    """Update changelog in-place.

    Returns:
        Tuple[Changelog, str]: changelog object and contents
    """
    return build_and_render(
        repository=".",
        output="CHANGELOG.md",
        convention="conventional",
        template="keepachangelog",
        parse_trailers=True,
        parse_refs=False,
        bump="auto",
        in_place=True,
    )


@duty(aliases=["format_docs"])
def fmt_docs(ctx: Context):
    """Format code in docs.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    ctx.run(
        blacken_docs.run("./", exts=[".md"]),
        nofail=True,
        title="Formatting docs (blacken-docs)",
    )



@duty
def check_api(ctx: Context) -> None:
    """Check for API breaking changes.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    from griffe.cli import check as g_check

    ctx.run(
        lambda: g_check("typer_config"),
        title="Checking for API breaking changes (griffe)",
        nofail=True,
    )


@duty
def changelog(ctx: Context):
    """Update the changelog in-place with latest commits.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    ctx.run(_changelog, title="Generating changelog (git-changelog)")


@duty()
def release(ctx: Context, version: Optional[str] = None):
    """Release a new Python package.

    Args:
        ctx (Context): The context instance (passed automatically).
        version (str, optional): The new version number to use. Defaults to None.
    """
    if version is None:
        res: Tuple[Changelog, str] = _changelog()
        version: str = res[0].versions_list[0].planned_tag
    ctx.run(f"poetry version {version}", title="Bumping version (poetry)")
    ctx.run("git add pyproject.toml CHANGELOG.md", title="Staging files (git)")
    ctx.run(
        ["git", "commit", "-m", f"chore: Prepare release {version}"],
        title="Committing changes (git)",
        pty=PTY,
    )
    ctx.run("poetry publish --build", title="Publish package (poetry)")
    ctx.run(
        f"mike deploy --push --update-aliases {version} latest",
        title="Deploying documentation (mike)",
    )
    ctx.run(f"git tag {version}", title="Tagging commit (git)", pty=PTY)
    ctx.run("git push", title="Pushing commits (git)", pty=False)
    ctx.run("git push --tags", title="Pushing tags (git)", pty=False)
