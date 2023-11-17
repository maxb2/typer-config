"""Test examples in docs.

Note: heavily inspired by https://github.com/koaning/mktestdocs

What I've written here is kind of a mess.
I'm working on rewriting it and PR'ing it upstream:
https://github.com/maxb2/mktestdocs/tree/feat/superfences

For now, it works.
"""

# NOTE: using "from __future__ import annotations" completely breaks
# this file for some reason.

import os
import re
from collections import OrderedDict
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

CLASS_RE = re.compile(
    dedent(
        r"""
        [ \t]*
        \.
        (?P<class>[a-zA-Z][a-zA-Z0-9_\-]*)
        [ \t]*
        """
    ),
    re.DOTALL | re.VERBOSE,
)

ID_RE = re.compile(
    dedent(
        r"""
        [ \t]*
        \#
        (?P<id>[a-zA-Z][a-zA-Z0-9_\-]*)
        [ \t]*
        """
    ),
    re.DOTALL | re.VERBOSE,
)

KEY_VAL_RE = re.compile(
    dedent(
        r"""
        [ \t]*
        (?P<key>\b[a-zA-Z][a-zA-Z0-9_]*)
        (?:
            =
            (?P<quot>"|')
            (?P<value>.*?)
            (?P=quot)
        )?
        [ \t]*
        """
    ),
    re.DOTALL | re.VERBOSE,
)

# NOTE: this is modified from
# `markdown.extensions.fenced_code.FencedBlockPreprocessor.FENCED_BLOCK_RE`
# to include options from `pymdownx/superfences.RE_OPTIONS`
FENCED_BLOCK_RE = re.compile(
    dedent(
        r"""
        (?P<raw>
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*           # opening fence
            (
                (\{(?P<attrs>[^\}\n]*)\})|            # (optional {attrs} or
                (\.?(?P<lang>[\w#.+-]*)[ ]*)?         # optional (.)lang
                (?P<options>                          # optional "options"
                    (?:                               # key-value pairs
                        (?:
                            \b[a-zA-Z][a-zA-Z0-9_]*
                            (?:
                                =
                                (?P<quot>"|')
                                .*?
                                (?P=quot)
                            )?
                            [ \t]*
                        ) |                           
                    )*
                )
            )
            \n                                        # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)                      # the code block
            (?P=fence)[ ]*$                           # closing fence
        )
        """
    ),
    re.MULTILINE | re.DOTALL | re.VERBOSE,
)


class Attr(NamedTuple):
    """Attribute in a fence."""

    value: str
    type_: str


# @dataclass
class Fence(NamedTuple):
    """Markdown Fence."""

    fence: str = ""
    lang: Optional[str] = None
    attrs: "Optional[OrderedDict[str, Attr]]" = None
    options: Optional[Dict[str, Any]] = None
    contents: str = ""
    raw: Optional[str] = None

    def options_from_str(raw: str) -> Dict[str, Any]:
        """Markdown fence options dict from string.

        Args:
            raw (str): string of options

        Returns:
            Dict[str, Any]: dict of options
        """
        options = {}
        while raw:
            match = KEY_VAL_RE.match(raw)
            if match is None:
                break
            options[match.groupdict()["key"]] = match.groupdict()["value"]
            raw = raw[match.span()[1] :]
        return options

    def attrs_from_str(raw: str) -> "OrderedDict[str, Attr]":
        """Markdown fence attributes from string.

        Args:
            raw (str): string of attributes

        Returns:
            Dict[str, Any]: dict of attrs
        """

        attrs = OrderedDict()

        while raw:
            if match := CLASS_RE.match(raw):
                attrs[match.groupdict()["class"]] = Attr(value=None, type_="class")
            elif match := ID_RE.match(raw):
                attrs[match.groupdict()["id"]] = Attr(value=None, type_="id")
            elif match := KEY_VAL_RE.match(raw):
                attrs[match.groupdict()["key"]] = Attr(
                    value=match.groupdict()["value"], type_="keyval"
                )
            else:
                break
            raw = raw[match.span()[1] :]
        return attrs

    def from_re_groups(groups: Tuple[str]) -> "Fence":
        """Make Fence from regex groups.

        Notes:
            This is tightly coupled to `FENCED_BLOCK_RE`.

        Args:
            groups (Tuple[str]): regex match groups

        Returns:
            Fence: markdown fence
        """

        attrs = Fence.attrs_from_str(groups[4])

        try:
            lang_attr = list(attrs.items())[0]
            _lang = lang_attr[0] if lang_attr[1].type_ == "class" else None
        except IndexError:
            _lang = None

        lang = groups[6] or _lang

        return Fence(
            fence=groups[1],
            lang=lang,
            attrs=attrs,
            options=Fence.options_from_str(groups[7]),
            contents=groups[9],
            raw=groups[0],
        )

    def from_str(raw: str) -> "Fence":
        """Fence from markdown string.

        Args:
            raw (str): markdown string

        Raises:
            Exception: couldn't find a markdown fence

        Returns:
            Fence: markdown fence
        """
        return Fence.from_re_groups(FENCED_BLOCK_RE.match(raw).groups())


class WorkingDirectory:
    """Sets the cwd within the context."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.origin = Path().absolute()

    def __enter__(self):
        """Enter context."""
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit context."""
        os.chdir(self.origin)


_executors = {}


def register_executor(lang, executor):
    """Add a new executor for markdown code blocks.

    lang should be the tag used after the opening ```
    executor should be a callable that takes one argument:
        the code block found
    """
    _executors[lang] = executor


def grab_fences(source: str) -> List[Fence]:
    """Grab fences in  markdown.

    Args:
        source (str): markdown string

    Returns:
        List[Fence]: list of fences in markdown
    """
    return [Fence.from_re_groups(groups) for groups in FENCED_BLOCK_RE.findall(source)]


def exec_file_fence(fence: Fence, **kwargs):
    """Executor that writes out file.

    Args:
        fence (Fence): markdown fence
        **kwargs: not used
    """
    fname = fence.options.get("title", None) or fence.attrs.get("title", [None])[0]
    with open(fname, "w") as f:
        f.write(fence.contents)


register_executor("yaml", exec_file_fence)
register_executor("yml", exec_file_fence)
register_executor("toml", exec_file_fence)


def exec_python_fence(fence: Fence, globals_: Optional[Dict] = None):
    """Python fence executor.

    Args:
        fence (Fence): markdown fence
        globals_ (Dict, optional): python globals to pass to exec. Defaults to {}.
    """
    if fence.options.get("title", False) or fence.attrs.get("title", False):
        exec_file_fence(fence)
    try:
        if globals_ is None:
            globals_ = {}
        exec(fence.contents, globals_)
    except Exception:
        print(fence.contents)  # noqa: T201
        raise


register_executor("python", exec_python_fence)
register_executor("py", exec_python_fence)


def exec_bash_fence(fence: Fence, **kwargs):
    """Bash fence executor.

    Args:
        fence (Fence): markdown fence
        **kwargs: not used
    """
    _cmds = fence.contents.split("$ ")
    commands: List[Dict] = []
    for _cmd in _cmds:
        if not _cmd:
            continue
        lines = _cmd.splitlines()
        commands.append({"input": lines[0], "output": "\n".join(lines[1:])})

    for command in commands:
        result = run(command["input"], shell=True, check=True, capture_output=True)
        assert (
            result.stdout.decode()
            .strip()
            .replace("\r", "")  # NOTE: fixing windows line ends
            == command["output"].strip()
        )


register_executor("bash", exec_bash_fence)


def check_typer_md_file(fpath: Path):
    """Check a markdown file with typer apps defined in it.

    Args:
        fpath (Path): path to markdown file
    """
    with open(fpath, "r") as f:
        source = f.read()
    fences = grab_fences(source)

    globals_ = {"__MODULE__": "__main__"}

    with TemporaryDirectory() as td, WorkingDirectory(td):
        for fence in fences:
            _executors[fence.lang](fence, globals_=globals_)
