# ipycalc
Simple Engineering Calculations in Python

This project is similar to 'handcalcs' by Conner Ferster, but with a slightly different flavor that I found useful for my calculations as a structural engineer. While it is similar, it was built from scratch rather than by forking `handcalcs`, so the code behaves very differently. A few key differences are:

*Use `%%calc` as the first line of a cell to indicate that you want to run `ipycalc` on the contents of a cell.
*US units are built in via `Pint`. Metric units are not yet supported.
*`ipycalc` does not show intermediate substitutions in the calculations.
*`ipycalc` provides control over the precision of the output line by line.
*`ipycalc` offers a placeholder for calculation descriptions (before the calculation) as well as references (after the calculation).

The basic calculation format is:

Variable Description: `variable_name` = `python_expression` -> `result_decimal_places`*`result_unit` # Reference Text

Here are a few useful things to keep in mind when using `ipycalc`:

*Subscripts can be added by using the `_` character to indicate the start of a subscript.
*To stack fractions place the numerator and denominater in parenthesis: (num)/(denom) = $\frac{num}{denom}$.
*The reference text is optional. I use it to give equation references or code references.
*`If` statements and `else` statements are available using python's inline `if` statement notation.