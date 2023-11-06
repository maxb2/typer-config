"""Utilities."""
from __future__ import annotations

from typing import Any, Dict, List, Optional


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
