# ipycalc
Simple Engineering Calculations in Python

Turn the contents of a Jupyter cell into a formatted calculation by following the steps below:

1. Install `ipycalc` using `pip install ipycalc`
2. Use `from ipycalc import calc` to bring `ipycalc` into your notebook's namespace.
3. Use `%%calc` as the first line of a cell to indicate that you want to run `ipycalc` on the contents of a cell.

The basic calculation syntax is:

Variable Description: `variable_name` = `python_expression` -> `result_decimal_places`*`result_unit` # Reference Text

Here's a simple example that calculates the flexural strength of a concrete beam:

![Example](/Example.png)

Key components of the `ipycalc` syntax are:

* `:` (required) The description must come before this character.
* `=` (optional) Used to assign a python expression to a variable name. Omit this if you simply want to reprint a previously defined variable.
* `->` (optional) Separates the python expression from the results formatting rules.
* `*` (optional) Indicate the number of decimals you want to see in the result to the left of the `*`, and the units you want to see in the result to the right.
* `#` (optional) Indicates reference text to the side of the calculation - handy for equation references or code references.

Here are a few useful things to keep in mind when using `ipycalc`:

* Subscripts can be added by using the `_` character to indicate the start of a subscript.
* Greek characters included in the `python_expression` can just be written out (e.g. `epsilon`). To include greek characters in the Variable Description or the Reference Text, you can use Jupyter's Markdown Latex tags (e.g. `$\epsilon$`).
* To stack fractions place the numerator and denominater in parentheses: (num)/(denom) yields $\dfrac{num}{denom}$.
* `if` statements and `else` statements are available using python's inline `if` statement (terniary) notation.
* Square roots can be displayed using `sqrt`.
* Prime characters can be displayed using `^prime`.
* If text gets to lengthy to fit on one line, you can add `\\` to force a line break anywhere in a line. This can help your calculations fit within the page's print margins.
* `ipycalc` assists you with printing your notebooks. It has a built in `nbconvert` template called `ipycalc` that works just like the `webpdf` template, except it fixes the the bad margins in the `webpdf` template, and avoids page breaks right after headers. Any cells tagged with `hide_cell` will not be rendered. Any cells tagged with `hide_input` will only show the output upon printing. You can select it from the file menu via "File -> Save and Export Notebook As... -> Ipycalc"

IPycalc is still in development. There could be bugs, so be cautious and validate the answers it gives you. A special thanks to @connorferster for his project `handcalcs` which inspired this project. A link to `handcalcs` is here: https://github.com/connorferster/handcalcs.
