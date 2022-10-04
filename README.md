# ipycalc
Simple Engineering Calculations in Python

Turn the contents of a Jupyter cell into a formatted calculation by following the steps below:

1. Install `ipycalc` using `pip install ipycalc`
2. Use `import ipycalc` to bring `ipycalc` into your notebook's namespace.
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
* To stack fractions place the numerator and denominater in parenthesis: (num)/(denom) yields $\dfrac{num}{denom}$.
* `If` statements and `else` statements are available using python's inline `if` statement notation.
* Square roots can be displayed using `sqrt`.
* Prime characters can be displayed using `^prime`.
* US units are built in via `Pint`. Metric units are not yet supported.

IPycalc is still in its infancy. I'm sure there are bugs, so be cautious and use your head. A special thanks to @connorferster for `handcalcs` which inspired this project: https://github.com/connorferster/handcalcs
