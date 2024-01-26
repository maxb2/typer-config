"""Utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Union


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


def search_path_parents(filename: Union[str, Path]) -> Path:
    """Search parent directories for a file.

    Args:
        filename (Union[str, Path]): name of file to search

    Raises:
        FileNotFoundError: could not find file in any parents

    Returns:
        Path: found file path
    """
    path = Path(filename).absolute()

    for _dir in path.parents:
        _path = _dir.joinpath(path.name)
        if _path.exists():
            return _path

    msg = f"Could not find {path.name} in {path.parent} or any of its parents."
    raise FileNotFoundError(msg)
