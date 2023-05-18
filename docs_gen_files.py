from pathlib import Path

import mkdocs_gen_files


def copy_file(source: Path, out: Path):
    """Copy a file into the mkdoc build.

    Args:
        source (Path): source file
        out (Path): output file (relative to the mkdocs docs/ folder)
    """
    with open(source, "rb") as f_source:
        with mkdocs_gen_files.open(out, "wb") as f_out:
            f_out.write(f_source.read())


def main():
    # Copy changelog to docs
    copy_file("CHANGELOG.md", "changelog.md")


main()
