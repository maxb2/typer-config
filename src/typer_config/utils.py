"""Utilities."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any
from warnings import showwarning

if TYPE_CHECKING:  # pragma: no cover
    from types import TracebackType

ORIGINAL_WARNING_FORMATTER = warnings.formatwarning


def get_dict_section(
    _dict: dict[Any, Any], keys: list[Any] | None = None
) -> dict[Any, Any]:
    """Get section of a dictionary.

    Args:
        _dict (dict[str, Any]): dictionary to access
        keys (list[str]): list of keys to successively access in the dictionary

    Returns:
        dict[str, Any]: section of dictionary requested
    """
    if keys is not None:
        for key in keys:
            _dict = _dict.get(key, {})

    return _dict


class SimpleWarningFormat:
    """Simple Warning Formatter."""

    def __enter__(self: SimpleWarningFormat) -> None:  # noqa: D105
        def _fmt(
            message: Warning | str,
            category: type[Warning],
            filename: str,  # noqa: ARG001
            lineno: int,  # noqa: ARG001
            line: str | None = None,  # noqa: ARG001
        ) -> str:
            return f"{category.__name__}: {message}\n"

        warnings.formatwarning = _fmt  # type: ignore

    def __exit__(  # noqa: D105
        self: SimpleWarningFormat,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        warnings.formatwarning = ORIGINAL_WARNING_FORMATTER


def file_exists_and_warn(file_path: Path | str) -> bool:
    """Check if file exists and warn if it doesn't exist.

    Args:
        file_path (Path | str): file path to check

    Returns:
        bool: whether file exists
    """

    file_path_exists = Path(file_path).is_file()

    if not file_path_exists:
        msg = f"No such file: '{file_path}'"

        with SimpleWarningFormat():
            showwarning(msg, UserWarning, "", 0)

    return file_path_exists
