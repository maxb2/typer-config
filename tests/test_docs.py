"""Test examples in documentation."""
from pathlib import Path

import pytest

from .doc_examples import check_typer_md_file


@pytest.mark.parametrize("fpath", Path("docs/examples").glob("*.md"), ids=str)
def test_doc_examples(fpath: Path):
    """Test doc file.

    Args:
        fpath (Path): file to test
    """
    check_typer_md_file(fpath)
