import nbformat
from nbconvert.exporters import HTMLExporter
import os

nb = nbformat.v4.new_notebook()
nb.cells = [
    nbformat.v4.new_markdown_cell("# Title"),
    nbformat.v4.new_markdown_cell("## Section A"),
    nbformat.v4.new_markdown_cell("### Subsection A1"),
    nbformat.v4.new_markdown_cell("### Subsection A2"),
    nbformat.v4.new_markdown_cell("## Section B"),
    nbformat.v4.new_markdown_cell("### Subsection B1"),
    nbformat.v4.new_markdown_cell("### Subsection B2"),
    nbformat.v4.new_markdown_cell("### Subsection B3"),
]

pkg_dir = os.path.join(os.path.abspath("."), "ipycalc")
e = HTMLExporter(extra_template_basedirs=[pkg_dir], template_name="nbconvert_template_numbered")
html, _ = e.from_notebook_node(nb)

with open("test_numbered_output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved test_numbered_output.html")
print("Expected numbering:")
print("  Title (no number)")
print("  1. Section A")
print("  1.1. Subsection A1")
print("  1.2. Subsection A2")
print("  2. Section B")
print("  2.1. Subsection B1")
print("  2.2. Subsection B2")
print("  2.3. Subsection B3")
