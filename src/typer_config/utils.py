"""Utilities."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from warnings import showwarning

ORIGINAL_WARNING_FORMATTER = warnings.formatwarning


def get_dict_section(
    _dict: Dict[Any, Any], keys: Optional[List[Any]] = None
) -> Dict[Any, Any]:
    """Get section of a dictionary.

    Args:
        _dict (Dict[str, Any]): dictionary to access
        keys (List[str]): list of keys to successively access in the dictionary

    Returns:
        Dict[str, Any]: section of dictionary requested
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
        exc_type: Any,  # noqa: ANN401
        exc_value: Any,  # noqa: ANN401
        exc_tb: Any,  # noqa: ANN401
    ) -> None:
        warnings.formatwarning = ORIGINAL_WARNING_FORMATTER


def file_exists_and_warn(file_path: Union[Path, str]) -> bool:
    """Check if file exists and warn if it doesn't exist.

    Args:
        file_path (Union[Path, str]): file path to check

    Returns:
        bool: whether file exists
    """

    file_path_exists = Path(file_path).is_file()

    if not file_path_exists:
        msg = f"No such file: '{file_path}'"

        with SimpleWarningFormat():
            showwarning(msg, UserWarning, "", 0)

    return file_path_exists
