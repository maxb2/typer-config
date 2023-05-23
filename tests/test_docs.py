from pathlib import Path

import pytest

from .doc_examples import check_typer_md_file


@pytest.mark.parametrize("fpath", Path("docs/examples").glob("*.md"), ids=str)
def test_doc_examples(fpath):
    for md_file in Path("docs/examples").glob("*.md"):
        check_typer_md_file(md_file)
