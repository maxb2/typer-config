from pathlib import Path

from .doc_examples import check_typer_md_file


def test_doc_examples():
    for md_file in Path("docs/examples").glob("*.md"):
        check_typer_md_file(md_file)
