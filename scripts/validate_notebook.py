"""Execute a notebook copy and export local review artifacts without saving the source."""

import argparse
from pathlib import Path
import tempfile

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--timeout", type=int, default=600, help="Seconds per cell")
    args = parser.parse_args()
    source = args.notebook.resolve(strict=True)
    if source.suffix != ".ipynb":
        parser.error("Expected an .ipynb file")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    notebook = nbformat.read(source, as_version=4)
    nbformat.validate(notebook)
    NotebookClient(
        notebook,
        timeout=args.timeout,
        kernel_name="python3",
        allow_errors=False,
        resources={"metadata": {"path": str(source.parent)}},
    ).execute()

    output_dir = Path(tempfile.mkdtemp(prefix="qec-notebook-review-"))
    executed = output_dir / source.name
    nbformat.write(notebook, executed)
    html, _ = HTMLExporter().from_notebook_node(notebook)
    rendered = output_dir / f"{source.stem}.html"
    rendered.write_text(html, encoding="utf-8")
    print(f"PASS: {source.name} executed in a fresh kernel without cell errors.")
    print(f"Executed copy: {executed}")
    print(f"HTML for visual review: {rendered}")
    print("Source notebook was not saved. Visual review remains a separate step.")


if __name__ == "__main__":
    main()
