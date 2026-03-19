import nbformat
from nbconvert.exporters import HTMLExporter
import os, re

nb = nbformat.v4.new_notebook()
nb.cells = [
    nbformat.v4.new_markdown_cell("# Chapter One"),
    nbformat.v4.new_markdown_cell("## Section A"),
    nbformat.v4.new_markdown_cell("## Section B"),
]
nb.metadata["toc-autonumbering"] = True

pkg_dir = os.path.join(os.path.abspath("."), "ipycalc")
e = HTMLExporter(extra_template_basedirs=[pkg_dir], template_name="nbconvert_template")
html, _ = e.from_notebook_node(nb)

with open("test_output.html", "w", encoding="utf-8") as f:
    f.write(html)

headings = re.findall(r"<h[1-6][^>]*>", html)
print("Headings found:", headings)
print("jp-Notebook present:", "jp-Notebook" in html)
print("counter-increment present:", "counter-increment" in html)

# Find what wraps the headings
for m in re.finditer(r"<h[1-6]", html):
    chunk = html[max(0, m.start()-300):m.start()]
    classes = re.findall(r'class="([^"]*)"', chunk)
    print(f"Heading at {m.start()}, parent classes: {classes[-5:]}")
