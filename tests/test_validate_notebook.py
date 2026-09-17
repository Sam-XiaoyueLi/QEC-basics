"""Regression coverage for portable notebook review images."""

import base64
from html.parser import HTMLParser
import sys

import nbformat

from scripts import validate_notebook


def test_export_embeds_relative_images_without_changing_source(tmp_path, monkeypatch):
    source_dir = tmp_path / "notebooks"
    assets = source_dir / "assets"
    assets.mkdir(parents=True)
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"/>'
    png = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8"
        "/x8AAwMCAO+aWQAAAABJRU5ErkJggg=="
    )
    (assets / "diagram.svg").write_bytes(svg)
    (assets / "pixel.png").write_bytes(png)
    source = source_dir / "example.ipynb"
    notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell(
        '![diagram](assets/diagram.svg)\n\n'
        '<img src="assets/pixel.png" alt="pixel">'
    )])
    nbformat.write(notebook, source)
    original = source.read_bytes()
    output = tmp_path / "export"
    output.mkdir()

    # Exercise the real exporter without starting a kernel for Markdown-only content.
    monkeypatch.setattr(validate_notebook.NotebookClient, "execute", lambda self: None)
    monkeypatch.setattr(validate_notebook.tempfile, "mkdtemp", lambda **kwargs: str(output))
    monkeypatch.setattr(sys, "argv", ["validate_notebook.py", str(source)])
    monkeypatch.chdir(tmp_path)  # Asset resolution must not depend on the shell's cwd.
    validate_notebook.main()

    class Images(HTMLParser):
        def __init__(self):
            super().__init__()
            self.sources = {}

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "img":
                self.sources[attrs.get("alt")] = attrs.get("src", "")

    images = Images()
    images.feed((output / "example.html").read_text())
    for alt, expected in [("diagram", svg), ("pixel", png)]:
        uri = images.sources[alt]
        assert uri.startswith("data:image/")
        assert base64.b64decode(uri.split(",", 1)[1]) == expected
    assert source.read_bytes() == original
    assert (output / "example.ipynb").is_file()
