"""Test that ipycalc templates work correctly: base has no numbering, numbered variant has JS numbering."""

import nbformat
from nbconvert import HTMLExporter
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ipycalc")
NUMBERING_MARKER = "counters[level]++"
IPYCALC_CSS_MARKER = "size: letter"


def make_notebook():
    """Create a minimal notebook with markdown headings."""
    nb = nbformat.v4.new_notebook()
    nb.cells = [
        nbformat.v4.new_markdown_cell("# Title"),
        nbformat.v4.new_markdown_cell("## Section A"),
        nbformat.v4.new_markdown_cell("### Subsection A1"),
        nbformat.v4.new_markdown_cell("### Subsection A2"),
        nbformat.v4.new_markdown_cell("## Section B"),
        nbformat.v4.new_markdown_cell("### Subsection B1"),
    ]
    return nb


def convert_notebook(nb, template_name):
    """Convert notebook to HTML using the specified template."""
    exporter = HTMLExporter(
        extra_template_basedirs=[TEMPLATE_DIR],
        template_name=template_name,
    )
    html, _ = exporter.from_notebook_node(nb)
    return html


def test_base_no_numbering():
    nb = make_notebook()
    html = convert_notebook(nb, "nbconvert_template")
    assert NUMBERING_MARKER not in html, "FAIL: Base template should NOT have numbering CSS"
    assert IPYCALC_CSS_MARKER in html, "FAIL: Base template should have ipycalc.css applied"
    print("PASS: Base template has no numbering, CSS applied")


def test_numbered_has_numbering():
    nb = make_notebook()
    html = convert_notebook(nb, "nbconvert_template_numbered")
    assert NUMBERING_MARKER in html, "FAIL: Numbered template should have numbering CSS"
    assert IPYCALC_CSS_MARKER in html, "FAIL: Numbered template should have ipycalc.css applied"
    print("PASS: Numbered template has numbering, CSS applied")


def test_numbered_skips_h1():
    nb = make_notebook()
    html = convert_notebook(nb, "nbconvert_template_numbered")
    assert "querySelectorAll('.jp-Notebook h2" in html, "FAIL: JS should only target h2+"
    assert "'.jp-Notebook h1" not in html, "FAIL: h1 should not be targeted by numbering"
    print("PASS: h1 headings are not numbered")


if __name__ == "__main__":
    test_base_no_numbering()
    test_numbered_has_numbering()
    test_numbered_skips_h1()
    print("\nAll tests passed!")

    print("\nAll tests passed!")
