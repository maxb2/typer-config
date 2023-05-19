"""
Test examples in docs.

Note: heavily inspired by https://github.com/koaning/mktestdocs
"""

import os
import re
from dataclasses import dataclass
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import Any, Dict, List, Optional, Tuple

from pymdownx.superfences import RE_NESTED_FENCE_START as RE_FENCE_START
from pymdownx.superfences import RE_OPTIONS

# NOTE: this is modified from
# `markdown.extensions.fenced_code.FencedBlockPreprocessor.FENCED_BLOCK_RE`
# to include options from `pymdownx/superfences.RE_OPTIONS`
FENCED_BLOCK_RE = re.compile(
    dedent(
        r"""
        (?P<raw>
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*                          # opening fence
            ((\{(?P<attrs>[^\}\n]*)\})|                              # (optional {attrs} or
            (\.?(?P<lang>[\w#.+-]*)[ ]*)?                            # optional (.)lang
            (?P<options>
                (?:
                    (?:\b[a-zA-Z][a-zA-Z0-9_]*(?:=(?P<oquot>"|').*?(?P=oquot))?[ \t]*) |  # Options
                )*
            )
            (hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot)[ ]*)?) # optional hl_lines)
            \n                                                       # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)                                     # the code block
            (?P=fence)[ ]*$                                          # closing fence
        )
        """
    ),
    re.MULTILINE | re.DOTALL | re.VERBOSE,
)


class WorkingDirectory:
    """Sets the cwd within the context"""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.origin = Path().absolute()

    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.chdir(self.origin)


_executors = {}


def register_executor(lang, executor):
    """Add a new executor for markdown code blocks

    lang should be the tag used after the opening ```
    executor should be a callable that takes one argument:
        the code block found
    """
    _executors[lang] = executor


def options_from_str(raw: str) -> Dict[str, Any]:
    options = {}
    while raw:
        match = RE_OPTIONS.match(raw)
        if match is None:
            break
        options[match.groupdict()["key"]] = match.groupdict()["value"]
        raw = raw[match.span()[1] :]
    return options


@dataclass
class Fence:
    fence: str = ""
    lang: Optional[str] = None
    attrs: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None
    contents: str = ""
    _raw: Optional[str] = None

    def from_re_groups(groups: Tuple[str]) -> "Fence":
        # NOTE: tightly coupled to `FENCED_BLOCK_RE`
        return Fence(
            fence=groups[1],
            lang=groups[6],
            attrs=groups[4],
            options=options_from_str(groups[7]),
            contents=groups[12],
            _raw=groups[0],
        )

    def from_str(raw: str) -> "Fence":
        lines = raw.strip().splitlines()

        match = RE_FENCE_START.match(lines[0])
        if match is None:
            raise Exception(lines[0])
        groupdict = match.groupdict()

        fence = groupdict.get("fence")
        assert lines[-1].strip() == fence, raw

        # TODO: support getting lang from attrs
        lang = groupdict.get("lang", None)

        # TODO: parse the attrs
        attrs = None

        _options = groupdict.get("options", None)
        if _options:
            options = options_from_str(_options)

        # NOTE: this assumes the last line is just the fence
        contents = "\n".join(lines[1:-1])

        return Fence(
            fence=fence,
            lang=lang,
            attrs=attrs,
            options=options,
            contents=contents,
            _raw=raw,
        )


def grab_fences(source: str):
    return [Fence.from_re_groups(groups) for groups in FENCED_BLOCK_RE.findall(source)]


def exec_file_fence(fence: Fence, **kwargs):
    fname = fence.options["title"]
    with open(fname, "w") as f:
        f.write(fence.contents)


register_executor("yaml", exec_file_fence)
register_executor("yml", exec_file_fence)
register_executor("toml", exec_file_fence)


def exec_python_fence(fence: Fence, globals: Dict = {}):
    if fence.options.get("title", False):
        exec_file_fence(fence)
    try:
        exec(fence.contents, globals)
    except Exception:
        print(fence.contents)
        raise


# register_executor("python", exec_python_fence)
# register_executor("py", exec_python_fence)

register_executor("python", exec_file_fence)
register_executor("py", exec_file_fence)


def exec_bash_fence(fence: Fence, globals: Dict = {}, **kwargs):
    _cmds = fence.contents.split("$ ")
    commands: List[Dict] = []
    for _cmd in _cmds:
        if not _cmd:
            continue
        lines = _cmd.splitlines()
        commands.append({"input": lines[0], "output": "\n".join(lines[1:])})

    for command in commands:
        result = run(command["input"], shell=True, check=True, capture_output=True)
        assert result.stdout.decode().strip() == command["output"].strip()


register_executor("bash", exec_bash_fence)


def check_typer_md_file(fpath: Path):
    with open(fpath, "r") as f:
        source = f.read()
    fences = grab_fences(source)

    _globals = {"__MODULE__": "__main__"}

    with TemporaryDirectory() as td:
        with WorkingDirectory(td) as wd:
            for fence in fences:
                _executors[fence.lang](fence, globals=_globals)
