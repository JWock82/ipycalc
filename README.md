# ipycalc
Engineering calculations in Jupyter, formatted for clear review and professional reports.

`ipycalc` helps engineers move from raw notebook math to readable, auditable calculations. Write equations in Python, add descriptions and references, and get polished output that is easier to check, share, and print.

## Why Use ipycalc?

- Turn opaque code cells into presentation-ready engineering calculations.
- Keep the speed and flexibility of Python while improving readability.
- Add units, references, and notation in one place.
- Export cleaner PDFs with the built-in `nbconvert` template.
- Reuse project variables across notebooks without manual copy/paste.

If you already use Jupyter for design work, `ipycalc` helps close the gap between computation and documentation.

## Quick Start

1. Install:

```bash
pip install ipycalc
```

2. Import in your notebook:

```python
from ipycalc import calc
```

3. Start a calc cell with `%%calc`.

## Basic Syntax

```text
Variable Description: variable_name = python_expression -> result_decimal_places*result_unit # Reference Text
```

Example (flexural strength of a concrete beam):

![Example](/Example.png)

## Syntax Reference

- `:` (required) Description appears before this character.
- `=` (optional) Assign a Python expression to a variable. Omit to reprint a previously defined variable.
- `->` (optional) Separates the expression from result formatting rules.
- `*` (optional) Set decimal places to the left and result units to the right.
- `#` (optional) Add right-side reference text (equation references, code references, notes).

## Useful Notes

- Subscripts: use `_` to indicate the start of a subscript.
- Greek in expressions: write names directly (for example `epsilon`).
- Greek in descriptions/reference text: use Jupyter Markdown LaTeX (for example `$\epsilon$`).
- `psi` is ambiguous with pressure units; use `\grpsi` when you need the Greek character.
- Stacked fractions: wrap numerator and denominator in parentheses, for example `(num)/(denom)` renders as $\dfrac{num}{denom}$.
- Conditionals: use Python inline ternary notation.
- Square roots: use `sqrt`.
- Prime notation: use `^prime`.
- Manual line breaks: insert `\\` where needed to avoid overflow in print layouts.
- Printing: `ipycalc` includes an `nbconvert` template named `ipycalc` that behaves like `webpdf`, but with improved margins and better page-break behavior after headers.
- Numbered/sectioned printing: use the `ipycalc_numbered` exporter to automatically number section headers (`h2` and below). This is useful for formal calculation packages where references to section numbers are required.
- Tag a cell with one of the following tags to change the way it prints to PDF:
	- `hide_cell` excludes the entire cell.
	- `hide_input` prints output only.
- In Jupyter, export with:
	- `File -> Save and Export Notebook As... -> Ipycalc`
	- `File -> Save and Export Notebook As... -> Ipycalc (Numbered)`
- From the command line, you can also export with `jupyter nbconvert --to ipycalc` or `jupyter nbconvert --to ipycalc_numbered`.

## Sharing Variables Between Notebooks

`ipycalc` can save variables from one notebook and import them into another. This is useful for multi-notebook workflows, such as loads feeding into member design.

Saving variables:

```python
from ipycalc import save_vars
save_vars('my_notebook.ipynb')
```

This writes user-defined variables (including `pint` quantities with units) to `.ipycalc_vars/my_notebook.json` in the notebook's directory. The notebook file itself is never modified.

Importing variables:

```python
from ipycalc import import_vars
import_vars('my_notebook.ipynb')           # import all saved variables
import_vars('my_notebook.ipynb', 'P', 'L') # import specific variables only
```

Both functions are also available directly inside a `%%calc` cell with no import statement required.

Variables are saved and loaded by filename only. Both notebooks must be in the same working directory.

## Project Status

`ipycalc` is actively evolving. Validate results as part of your normal engineering QA process.

Special thanks to @connorferster and the `handcalcs` project for inspiration:
https://github.com/connorferster/handcalcs
