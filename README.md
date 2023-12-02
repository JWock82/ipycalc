# ipycalc
Simple Engineering Calculations in Python

Turn the contents of a Jupyter cell into a formatted calculation by following the steps below:

1. Install `ipycalc` using `pip install ipycalc`
2. Use `from ipycalc import calc` to bring `ipycalc` into your notebook's namespace.
3. Use `%%calc` as the first line of a cell to indicate that you want to run `ipycalc` on the contents of a cell.

The basic calculation syntax is:

Variable Description: `variable_name` = `python_expression` -> `result_decimal_places`*`result_unit` # Reference Text

Key components of the `ipycalc` syntax are:

* `:` (required) The description must come before this character.
* `=` (optional) Used to assign a python expression to a variable name. Omit this if you simply want to reprint a previously defined variable.
* `->` (optional) Separates the python expression from the results formatting rules.
* `*` (optional) Indicate the number of decimals you want to see in the result to the left of the `*`, and the units you want to see in the result to the right.
* `#` (optional) Indicates reference text to the side of the calculation - handy for equation references or code references.

Here are a few useful things to keep in mind when using `ipycalc`:

* Subscripts can be added by using the `_` character to indicate the start of a subscript.
* To stack fractions place the numerator and denominater in parentheses: (num)/(denom) yields $\dfrac{num}{denom}$.
* `If` statements and `else` statements are available using python's inline `if` statement notation.
* Square roots can be displayed using `sqrt`.
* Prime characters can be displayed using `^prime`.
* If a line gets too long for printing, you can add a line break to the description, equation, or reference by inserting `\\`.
* `ipycalc` assists you with printing your notebooks. It has a built in `nbconvert` template called `ipycalc` that works just like the `webpdf` template, except it fixes the the bad margins in the `webpdf` template, and avoids page breaks right after headers. Any cells tagged with `hide_cell` will not be rendered. Any cells tagged with `hide_input` will only show the output upon printing. You can select it from the file menu via "File -> Save and Export Notebook As... -> Ipycalc"

IPycalc is still in its infancy. I'm sure there are bugs, so be cautious and use your head. A special thanks to @connorferster for `handcalcs` which inspired this project: https://github.com/connorferster/handcalcs
