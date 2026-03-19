import os
import re
import json

from math import pi, sqrt, sin, cos, asin, acos, atan, tan, sinh, cosh, tanh, log, log10

from IPython.core.magic import (register_cell_magic, needs_local_scope)
from IPython.display import display, Latex, HTML, Markdown
from IPython import get_ipython

# Use pint for units
import pint
directory = os.path.dirname(__file__)
ureg = pint.UnitRegistry(directory + '\\ipycalc_en.txt')  # Creates the units registry
ureg.default_system = 'US'  # US Customary unit system
ureg.formatter.default_format = '~P'  # Shorthand units w/ pretty formatting

# Enable automatic handling of offset units (temperatures)
ureg.autoconvert_offset_to_baseunit = True

# Create shortcuts to the unit registry's units in this module's namespace
inch = ureg.inch
ft = ureg.foot
feet = ureg.foot
mi = ureg.mile
ozf = ureg.ozf
lbf = ureg.lbf
lbm = ureg.lbm
kip = ureg.kip
ton = ureg.ton
tonf = ureg.tonf
plf = ureg.plf
klf = ureg.klf
psi = ureg.psi
psf = ureg.psf
ksi = ureg.ksi
ksf = ureg.ksf
pcf = ureg.pcf
kcf = ureg.kcf
lbin = ureg.lbin
lbft = ureg.lbft
kipin = ureg.kipin
kipft = ureg.kipft
kin = ureg.kin
kft = ureg.kft
mph = ureg.mph
rpm = ureg.rpm
Hz = ureg.hertz
deg = ureg.degree
rad = ureg.radian
sec = ureg.second
minute = ureg.minute
hr = ureg.hour
gal = ureg.gallon
degF = ureg.degF
degC = ureg.degC

# Add some useful metric units
g = ureg.gram
kg = ureg.kilogram
mm = ureg.millimeter
cm = ureg.centimeter
m = ureg.meter
km = ureg.kilometer
N = ureg.newton
kN = ureg.kilonewton
kgf = ureg.force_kilogram
tonne = ureg.tonne
tonnef = ureg.tonnef
Pa = ureg.pascal
kPa = ureg.kilopascal
MPa = ureg.megapascal
GPa = ureg.gigapascal
percent = ureg.percent
pct = ureg.pct

unit_list = ['inch', 'feet', 'ft', 'mi', 'ozf', 'lbf', 'lbm', 'kip', 'ton', 'tonf', 'plf', 'klf', 'psi', 'psf', 
             'ksi', 'ksf', 'pcf', 'kcf', 'lbin', 'lbft', 'kipin', 'kipft', 'kin', 'kft', 'mph',
             'rpm', 'Hz', 'deg', 'rad', 'sec', 'minute', 'hr', 'gal', 'degF', 'degC', 'mm', 'cm', 'm', 'km', 'N', 'kN', 'kgf', 'tonne', 'tonnef', 'Pa',
             'kPa', 'MPa', 'GPa', 'percent', 'pct']

#%%
@register_cell_magic
@needs_local_scope
def calc(line, cell, local_ns):

    # Sync variables in this module's namespace with IPython's namespace and vis-versa
    sync_namespaces(local_ns)

    # Split up each line of text in the cell
    code_lines = cell.split('\n', -1)

    # Purge blank lines
    for i, ln in enumerate(code_lines):
        if ln == '' or ln == '\n':
            code_lines.pop(i)

    # Arrays will be used to format the output in a tabular way for display in Jupyter
    # Start a parent array that will hold all the output.
    # text = '\\begin{array} {lpwidth{0.25\\linewidth} lpwidth{0.5\\linewidth} lpwidth{0.25\\linewidth}}\n'
    text = '\\begin{array}{l l l}\n'  # KaTeX friendly version of the line above

    # Process each code line
    for ln in code_lines:
        text += process_line(ln, local_ns)

    # Close of the parent array that contains all the lines
    text += '\\end{array}'

    # Display the cell's results
    display(Markdown('$' + text + '$'))

#%%
def sync_namespaces(local_ns):
    
    # Sync all of this module's global variables with IPython's latest variables.
    for var in local_ns.keys():
        if var[0] != '_':
            exec('global ' + var + '; ' + var + ' = local_ns[var]')

    # Create shortcuts to the unit registry's units in the IPython console's namespace
    local_ns['inch'] = ureg.inch
    local_ns['ft'] = ureg.foot
    local_ns['feet'] = ureg.foot
    local_ns['mi'] = ureg.mile
    local_ns['ozf'] = ureg.ozf
    local_ns['lbf'] = ureg.lbf
    local_ns['lbm'] = ureg.lbm
    local_ns['kip'] = ureg.kip
    local_ns['k'] = ureg.kip
    local_ns['ton'] = ureg.ton
    local_ns['tonf'] = ureg.tonf
    local_ns['plf'] = ureg.plf
    local_ns['klf'] = ureg.klf
    local_ns['psi'] = ureg.psi
    local_ns['psf'] = psf
    local_ns['ksi'] = ureg.ksi
    local_ns['ksf'] = ureg.ksf
    local_ns['pcf'] = ureg.pcf
    local_ns['kcf'] = ureg.kcf
    local_ns['lbin'] = ureg.lbin
    local_ns['lbft'] = ureg.lbft
    local_ns['kipin'] = ureg.kipin
    local_ns['kipft'] = ureg.kipft
    local_ns['kin'] = ureg.kin
    local_ns['kft'] = ureg.kft
    local_ns['mph'] = ureg.mph
    local_ns['rpm'] = ureg.rpm
    local_ns['Hz'] = ureg.hertz
    local_ns['sec'] = ureg.second
    local_ns['minute'] = ureg.minute
    local_ns['hr'] = ureg.hour
    local_ns['deg'] = ureg.degree
    local_ns['rad'] = ureg.radian
    local_ns['gal'] = ureg.gallon
    local_ns['degF'] = ureg.degF
    local_ns['degC'] = ureg.degC
    
    # Add some useful metric units
    local_ns['mm'] = ureg.millimeter
    local_ns['cm'] = ureg.centimeter
    local_ns['m'] = ureg.meter
    local_ns['km'] = ureg.kilometer
    local_ns['N'] = ureg.newton
    local_ns['kN'] = ureg.kilonewton
    local_ns['g'] = ureg.gram
    local_ns['kg'] = ureg.kilogram
    local_ns['Pa'] = ureg.pascal
    local_ns['kPa'] = ureg.kilopascal
    local_ns['MPa'] = ureg.megapascal
    local_ns['GPa'] = ureg.gigapascal
    local_ns['tonne'] = ureg.tonne
    local_ns['tonnef'] = ureg.tonnef
    local_ns['percent'] = ureg.percent
    local_ns['pct'] = ureg.pct

    # Provide the IPython console with access to save_vars and import_vars
    local_ns['save_vars'] = save_vars
    local_ns['import_vars'] = import_vars

#%%
def process_line(calc_line, local_ns):

    # Break up the line into components: `description`, `variable`, `equation`, `value` and `reference`
    # Split `reference` off from the rest of the line
    if '#' in calc_line:
        description, reference = calc_line.split('#', 1)
    else:
        description, reference = calc_line, ''
    
    # Split `description` off from the rest of the line
    if ':' in calc_line:
        description, variable = description.split(':', 1)
    else:
        description, variable = '', description
    
    # Split off `variable` from the rest of the line
    if '=' in variable:
        variable, equation = variable.split('=', 1)
    else:
        variable, equation = variable, ''

    if '->' in equation:
        equation, value_format = equation.split('->', 1)
    elif '->' in variable:
        variable, value_format = variable.split('->', 1)
    else:
        equation, value_format = equation, ''

    # Remove leading and trailing whitespace from all the components except the equation. The equation is a Python expression that may need the spaces.
    description = description.strip()
    variable = variable.strip()
    value_format = value_format.strip()

    # Determine if this is an expression-only line (no variable assignment).
    # This occurs when there's no '=' sign and the text is not a simple variable name.
    if equation == '':
        test_var = variable.replace('(', '').replace(')', '').replace('{', '').replace('}', '').replace(',', '').replace(' ', '').replace('lambda', 'lamb').replace('^prime', '_prime')
        is_expression_only = not test_var.isidentifier()
    else:
        is_expression_only = False

    # Format the equation to be Python friendly
    equation = equation.replace('^prime', '_prime')
    equation = equation.replace('^', '**')
    equation = equation.replace('lambda', 'lamb')
    
    # Convert percentage symbols to percent units
    # Match % symbols that follow numbers/variables (but not in strings)
    equation = re.sub(r'(\d+(?:\.\d+)?)\s*%', r'\1*percent', equation)

    # Resolve prime symbols in the variable before we compare it to the equation, which has already had them resolved
    variable = variable.replace('^prime', '_prime')

    # Make a latex copy of the equation and variable before we switch out square root symbols
    latex_variable = python_to_latex(variable)
    latex_equation = python_to_latex(equation)

    # `Pint` prefers exponents to the 1/2 power instead of square roots
    equation = alt_sqrt(equation)

    # Remove manually inserted line breaks from the equation
    equation = equation.replace('\\\\', '')
    
    # Turn off pretty printing momentarily while we prepare a Python expression for the value
    ureg.formatter.default_format = '~'

    # Determine the requested unit format
    if '*' in value_format:
        # Both precision and units were requested
        precision, unit = value_format.split('*', 1)
        precision = int(precision)
        is_string_format = False
    elif value_format.strip().lower() == 's':
        # String format requested
        precision, unit = None, None
        is_string_format = True
    elif value_format != '':
        # Precision was requested without units
        precision, unit = value_format, None
        precision = int(precision)
        is_string_format = False
    else:
        # No precision and no units were requested
        precision = None
        is_string_format = False
        if equation != '':
            # An equation has been provided
            if type(eval(equation)) == ureg.Quantity:
                # The evaluated equation carries units
                unit = str(eval(equation).units)
            else:
                # The equation is unitless after evaluation
                unit = None
        elif variable != '':
            # No equation has been provided. We are just displaying a variable
            if type(eval(variable)) == ureg.Quantity:
                # The variable carries units
                unit = str(eval(variable).units)
            else:
                # The variable does not carry units
                unit = None

    # Determine what expression to evaluate (equation or variable)
    expr_to_eval = equation if equation != '' else variable
    
    # Helper function to compute the value string
    def compute_value(expression, target_unit, target_precision):
        """Computes the value string for storage and later evaluation"""
        if target_unit != None:
            return str((eval(expression).to(target_unit)).magnitude) + '*' + target_unit
        elif target_precision != None:
            # Unitless values - convert to ensure proper cancellation:
            # Unitless values require special consideration. Pint leaves values in terms of the
            # units used to calculate them. That means 60 ft / 12 in = 5 ft/in instead of 60.
            # As a workaround we'll convert that quantity to some units that cancel each other out.
            # In cases where there are no units (a pure float) we'll need to tag on some units
            # to make the `to` function available. These units should also cancel each other out.
            return str((eval(expression)*inch/inch).to(inch/inch))
        else:
            eval_result = eval(expression)
            if isinstance(eval_result, str):
                return repr(eval_result)  # Use repr to get quoted string
            else:
                return str(eval_result)
    
    # Compute the value
    value = compute_value(expr_to_eval, unit, precision)
    
    # When pint returns unit strings, it uses abbreviated forms like 'in' instead of 'inch'
    # 'in' is a Python keyword, so we need to convert it back to 'inch' for eval()
    # Use regex to replace 'in' only when it appears as a standalone unit (word boundary)
    value = re.sub(r'\bin\b', 'inch', value)
    value = value.strip()
    
    # In the case of dimensionless units due to units canceling out, there will be an extra '*' at
    # the end of the value we need to eliminate
    if value[-1] == '*':
        value = value[0:-1]
    
    # Turn pretty printing back on
    ureg.formatter.default_format = '~P'
    
    # Format the description
    if description != '':
        # Escape ampersand symbols for latex table formatting
        description = description.replace('&', r'\&')
        description = description + ': '
    
    # Format the variable to be Python friendly (skip for expression-only lines)
    if not is_expression_only:
        variable = variable.replace('(', '')
        variable = variable.replace(')', '')
        variable = variable.replace('{', '')  # Remove curly braces for valid Python variable names
        variable = variable.replace('}', '')  # Remove curly braces for valid Python variable names
        variable = variable.replace(',', '')  # Remove commas for valid Python variable names
        variable = variable.replace(' ', '')
        variable = variable.replace('lambda', 'lamb')  # lambda is a reserved word in python

    # Create a Latex version of the value
    latex_value = ''
    if value_format != '' or equation == '':

        if is_string_format:
            # String format requested with 's'
            eval_val = eval(value)
            if isinstance(eval_val, str):
                latex_value = '=\\textsf{' + eval_val + '}'
            else:
                latex_value = '=' + str(eval_val)
        elif unit != None:
            latex_value = '=' + funit(eval(value), precision)
        elif precision != None:
            latex_value = '=' + funit((eval(value)*inch/inch).to(inch/inch), precision)
        else:
            eval_val = eval(value)
            if isinstance(eval_val, str):
                latex_value = '=\\textsf{' + eval_val + '}'
            else:
                latex_value = '=' + str(eval_val)

    # Known issue: The characters '.' and '-' will evaluate as not numeric below
    # # This next block allows values to be strings
    # if type(eval(equation)) != ureg.Quantity:
    #     if not value.isnumeric():
    #         value = '\'' + value + '\''
    
    # Add the variable and its value to this module's global namespace (skip for expression-only lines)
    if not is_expression_only:
        exec('global ' + variable + '; ' + variable + '=' + value)

        # Add the variable and its value to the IPython console's namespace
        local_ns[variable] = eval(value)
    
    # Add the equals sign between the variable and equation
    latex_variable = latex_variable + '='

    # Format the reference
    reference = reference.strip()
    # Escape ampersand symbols for latex table formatting
    reference = reference.replace('&', r'\&')

    # Return the line formatted in all its glory.
    # linebreaks() splits each column's text on "\\" linebreak markers and returns
    # a list of individually formatted lines. For example, if description has 2 lines
    # and reference has 1, we get desc=['line1','line2'], ref=['line1'].
    # We then emit one parent array row per index, filling in blanks for shorter columns.
    # This guarantees the first line of each column sits on the same row (top-aligned).

    # Get the list of formatted lines for the description column (left column)
    desc = linebreaks(description, 'text')
    # Get the list of formatted lines for the equation column (middle column)
    eq = linebreaks(latex_variable + latex_equation + latex_value, 'math')
    # Get the list of formatted lines for the reference column (right column)
    ref = linebreaks(reference, 'text')

    def compact_multiline_text_cell(raw_text):
        # Split on user-entered "\\" markers so each authored continuation line is preserved.
        # Example: "Line A\\Line B" -> ["Line A", "Line B"]
        text_lines = raw_text.split('\\\\')

        # Build each rendered line explicitly so blank lines can be handled safely.
        compact_lines = []
        for ln in text_lines:
            if ln:
                # Keep text columns in sans-serif to match existing description/reference styling.
                compact_lines.append('\\textsf{' + ln + '}')
            else:
                # Use a non-breaking placeholder so intentionally blank lines still occupy
                # vertical space in the nested array instead of collapsing.
                compact_lines.append('\\textsf{~}')

        # Render all continuation lines inside one nested array cell.
        # This avoids forcing continuation text onto additional parent rows, which is what
        # previously created large visual gaps when the equation column had tall content.
        #
        # `\\hspace{-0.5em}` and `\\hspace{-0.6em}` trim nested-array side padding so
        # multiline description/reference blocks visually align with single-line rows.
        return '{\\small{\\hspace{-0.5em}\\begin{array}{l}' + '\\\\'.join(compact_lines) + '\\end{array}\\hspace{-0.6em}}}'

    # If description spans multiple authored lines, collapse those lines into a single compact
    # cell entry. The compact cell still occupies row 1, so top-justification is preserved.
    if len(desc) > 1:
        desc = [compact_multiline_text_cell(description)]
    # Apply the same compact-cell rule to multiline references for consistent behavior.
    if len(ref) > 1:
        ref = [compact_multiline_text_cell(reference)]

    # Determine how many parent rows we need (driven by the column with the most lines)
    n = max(len(desc), len(eq), len(ref))
    # Initialize the output string that will hold all the rows for this calc line
    latex_text = ''
    # Loop through each row index
    for i in range(n):
        # Use the description line at this index, or blank if the column is shorter
        d = desc[i] if i < len(desc) else ''
        # Use the equation line at this index, or blank if the column is shorter
        e = eq[i] if i < len(eq) else ''
        # Use the reference line at this index, or blank if the column is shorter
        r = ref[i] if i < len(ref) else ''
        # Assemble the three cells into one parent array row separated by & delimiters
        latex_text += d + '&' + e + '&' + r + '\\\\ \n'

    # There will be a double equals sign if the equation is not being displayed
    latex_text = latex_text.replace('==', '=')
    
    # Uncomment the next line to view the raw latex output while debugging
    # print(latex_text)

    return latex_text

#%%
def python_to_latex(text):
    """Converts python equations to latex equations

    :param text: Python text to be converted to latex.
    :type text: str
    :return: Latex text
    :rtype: str
    """
    
    # Replace all quoted strings (both single and double quotes) with unquoted sans-serif versions
    # Protect spaces within strings by temporarily replacing them
    def replace_string(match):
        content = match.group(1).replace(' ', '~')
        return '\\textsf{' + content + '}'
    
    text = re.sub(r'"([^"]*)"', replace_string, text)
    # Handle single-quoted strings - replace spaces with placeholder
    text = re.sub(r"'([^']*)'", replace_string, text)
    
    # Change spaces we want to keep to the '~' symbol temporarily
    text = text.replace(' if ', '~if~')
    text = text.replace(' else ', '~else~')

    # Add any prime symbols back in
    text = text.replace('_prime', '^{\\prime}')

    # Switch out Python's exponent symbols for Latex's
    text = text.replace('**', '^')

    # Add brackets to superscripts and subscripts if they are missing
    text = sscript_curly('^', text)
    text = sscript_curly('_', text)
    
    # Wrap subscripted variables that are raised to a power to avoid ambiguity
    # Convert X_{sub}^{exp} to {X_{sub}}^{exp} so the exponent clearly applies to the whole variable
    text = re.sub(r'(\w+_\{[^}]+\})(\^\{[^}]+\})', r'{\1}\2', text)

    # Convert `lamb` back to `lambda` for latex
    text = text.replace('lamb', 'lambda')

    # Process 'if' statements first, since they require spaces
    if '~if~' in text:
        text = process_if(text, type='if')

    # Keep intentional spaces after commas
    text = text.replace(', ', ',\\~')

    # Convert logical operators to latex
    text = text.replace(' and ', '\\~and\\~')
    text = text.replace(' or ', '\\~or\\~')
    
    # Adjust inequality symbols
    text = text.replace('<=', '~\\le~')
    text = text.replace('>=', '~\\ge~')
    text = text.replace('!=', '~\\neq~')

    # Define a list of greek symbols
    greek = (['alpha', 'eta', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'omega', 'Alpha', 'Eta', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega'])
    
    # Clean up any greek symbols
    for symbol in greek:
        if symbol in text:
            text = text.replace(symbol, '\\' + symbol + '~')
    
    # Fix any errors caused by `eta` being similar to other symbols
    text = text.replace('b\\eta', '\\beta')
    text = text.replace('th\\eta', '\\theta')
    text = text.replace('z\\eta', '\\zeta')
    
    # Take care of any lower case greek psi characters. This is necessary because 'psi' is also a unit
    text = text.replace('grpsi', '\\psi')

    # Convert common functions to latex
    text = text.replace('sin(', '\\sin(')
    text = text.replace('cos(', '\\cos(')
    text = text.replace('tan(', '\\tan(')
    text = text.replace('a\\sin(', '\\arcsin(')
    text = text.replace('a\\cos(', '\\arccos(')
    text = text.replace('a\\tan(', '\\arctan(')
    text = text.replace('arc\\sin(', '\\arcsin(')
    text = text.replace('arc\\cos(', '\\arccos(')
    text = text.replace('arc\\tan(', '\\arctan(')
    text = text.replace('min(', '\\min(')
    text = text.replace('max(', '\\max(')
    text = text.replace('log(', 'ln(')
    text = text.replace('log10(', 'log10(')
    text = text.replace('sqrt(', '\\sqrt(')

    # Legacy code:
    # Adjust a few more special characters to be Latex friendly
    # text = text.replace('*', ' \\cdot{}')

    # Change any parentheses to brackets for `sqrt`, `^`, and `_`
    text = curly_brackets('sqrt', text)
    text = curly_brackets('^', text)
    text = curly_brackets('_', text)

    # Format fractions
    text = frac(text)

    # Change out normal parentheses for auto-sizing parentheses
    text = text.replace('(', '\\left(')
    text = text.replace(')', '\\right)')

    # Remove unwanted spaces from the raw text
    text = text.replace(' ', '')

    # Convert '~' symbols back to spaces
    text = text.replace('~', ' ')

    # Provide a space before any units
    text = text.replace('*inch', ' \\ in')
    
    # Handle percent specially - use % symbol instead of word
    text = text.replace('*percent', '\\%')
    text = text.replace('*pct', '\\%')
    for unit in unit_list:
        if unit not in ['percent', 'pct']:  # Skip percent as we already handled it
            text = text.replace('*' + unit, ' \\ ' + unit)

    # Replace multiplication symbols in front of numbers with a multiplication dot
    for i in range(10):
        text = text.replace('*' + str(i), '\\cdot{}' + str(i))
    
    # Convert remaining multiplication symbols to centered dots for better readability
    text = text.replace('*', '\\cdot{}')

    # Return the Latex text
    return text

def process_if(text, type):
    
    # Note: `if` statements nested in the first return value are not supported. `if` statements nested after the first 'else' are supported.

    # Split the line into `if` and `else` portions
    if 'else' in text:
        if_text, else_text = text.split('else', 1)
    else:
        if_text, else_text = text, ''
    
    # Check what type of statement this is: `if`, `elif`, or `else`
    if type == 'if':
        # Add an `if` line
        value, condition = if_text.split('if', 1)
        latex_text = value + '\\hspace{0.5em}\\textsf{~if~}' + condition + '\\\\'
    elif type == 'elif':
        # Add an `elsif` line
        value, condition = if_text.split('if', 1)
        latex_text = '\\textsf{else~}' + value + '\\hspace{0.5em}\\textsf{~if~}' + condition + '\\\\'
    elif type == 'else':
        value = if_text
        # Add the `else` line
        latex_text = '\\textsf{else~}' + value + '\\\\'

    # Repeat the process for any further conditionals found in the `else` portion of the statement
    if else_text != '':

        # Remove any whitespace at the ends of the else text
        else_text = else_text.strip()

        # Use recursion to evaluate the remaining conditional statements
        if '~if~' in else_text:
            latex_text += process_if(else_text, type='elif')
        else:
            latex_text += process_if(else_text, type='else')

    return latex_text

def curly_brackets(fname, text):

    while fname + '(' in text:
        
        lhs, rhs = text.split(fname + '(', 1)

        paren_count = 1
        term = ''
        for char in rhs:
            if char == ')':
                if paren_count == 1:
                    break
                else:
                    paren_count -= 1
            elif char == '(':
                paren_count += 1
            term += char
        
        text = text.replace(fname + '(' + term + ')', fname + '{' + term + '}')

    return text

def sscript_curly(symbol, text):
    """
    Places any terms immediately following the giving symbol in brackets. Useful for formatting
    superscripts and subscripts for Latex.
    """

    # Latex needs help seeing all the characters belonging to superscripts and subscripts
    term_list = []
    for i, char in enumerate(text):
        
        # Find any instances of `symbol` that have not already been formatted properly
        if char == symbol and text[i:i+2] != symbol + '(' and text[i:i+2] != symbol + '{':
            
            # Initialize the term after the symbol
            term = ''
            paren_count = 0

            # Add all the characters associated with this symbol
            j = i + 1
            while j < len(text) and text[j] not in ['+', '-', '*', '/', '=', '>', '<', '!', ',', '~', '^']:

                # Check for parentheses nested within the superscript or subscript
                if text[j] == '(':
                    # This parenthesis will need to be closed before we reach the end of the term
                    paren_count += 1
                elif text[j] == ')':
                    if paren_count == 0:
                        # All parentheses in the term are already closed, so this one does not
                        # belong to the term
                        break
                    else:
                        paren_count -= 1
                
                # Add the character to the term
                term += text[j]

                # Move to the next character
                j += 1
            
            # The search we just ran didn't stop at the strings below
            if '->' in term:
                term = term.split('->', 1)[0]
            
            term_list.append(term.strip())
    
    # Sort the list of terms from longest to shortest. This prevents errors when one term starts
    # with the same characters as those in a longer term
    term_list = sorted(term_list, key=len, reverse=True)

    # Replace all the discovered symbols with bracketed symbols
    for term in term_list:
        text = text.replace(symbol + term, symbol + '{' + term + '}')

    return text

#%%
def frac(text):
    """
    Formats fractions to have the numerator over the denominator when the terms are contained in
    parentheses.
    """
    # Make fractions Latex friendly
    # We must do this only after we've already adjusted functions and subscripts
    while ')/(' in text:
        
        lhs, rhs = text.split(')/(', 1)
        
        paren_count = 1
        num = ''
        for char in lhs[::-1]:
            if char == '(':
                if paren_count == 1:
                    break
                else:
                    paren_count -= 1
            elif char == ')':
                paren_count += 1
            num += char
        num = num[::-1]

        paren_count = 1
        denom = ''
        for char in rhs:
            if char == ')':
                if paren_count == 1:
                    break
                else:
                    paren_count -= 1
            elif char == '(':
                paren_count += 1
            denom += char
        
        # Check if the denominator's closing paren is immediately followed by an exponent.
        # In Python, (a)/(b)**x means a / (b**x), so the exponent belongs in the denominator.
        # But ((a)/(b))**x means (a/b)**x, which is handled correctly because the extra outer
        # paren prevents the exponent from appearing right after the denominator's closing paren.
        remaining = rhs[len(denom) + 1:]  # +1 to skip the closing ')'
        exp_str = ''
        if remaining.startswith('^{'):
            brace_count = 0
            for k, c in enumerate(remaining):
                if c == '{':
                    brace_count += 1
                elif c == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        exp_str = remaining[:k+1]  # e.g., '^{v_d}'
                        break

        if exp_str:
            text = text.replace('(' + num + ')/(' + denom + ')' + exp_str, '\\dfrac{' + num + '}{' + denom + exp_str + '}')
        else:
            text = text.replace('(' + num + ')/(' + denom + ')', '\\dfrac{' + num + '}{' + denom + '}')

    # Note: The following regex was disabled because it incorrectly moves exponents from
    # numerators into denominators. For example, ((D_c + 2*t_w)**2)/(4) should remain as
    # \dfrac{(D_c+2*t_w)^{2}}{4}, not \dfrac{(D_c+2*t_w)}{4^{2}}
    # Correct any remaining instances of `\\dfrac{a}{b}^{c}` to be `\\dfrac{a}{b^c}`
    # pattern = r"\\dfrac\{(.*?)\}\{(.*?)\}\^\{(.*?)\}"
    # repl = r"\\dfrac{\1}{\2^{{\3}}}"
    # text = re.sub(pattern, repl, text)
    
    return text

#%%
def alt_sqrt(text):
    """
    Makes square root terms `pint` friendly
    """

    while 'sqrt' in text:
        
        lhs, rhs = text.split('sqrt', 1)

        paren_count = 0
        term = ''
        for char in rhs:
            if char == ')':
                if paren_count == 1:
                    term += char
                    break
                else:
                    paren_count -= 1
            elif char == '(':
                paren_count += 1
            term += char
        
        text = text.replace('sqrt' + term, '(' + term + ')**0.5')

    return text

#%%
def funit(value, precision=None):

    # Round the value out to the appropriate precision
    if precision != None:
        latex_value = str(round(value, precision))
    else:
        latex_value = str(value)
    
    # Replace pct unit with % symbol early
    latex_value = latex_value.replace('pct', '%')

    # Step through each character in the value
    for i, char in enumerate(latex_value):

        # Find the first non-numeric non-decimal character, excluding the minus sign for negative numbers
        if not latex_value[i].isnumeric() and latex_value[i] !='.' and latex_value[i] !='-':

            # Add a space between the value and the units
            latex_value = latex_value[0:i] + ' \\ ' + latex_value[i:len(latex_value)]

            # The round function tags on a .0 after it rounds floats. It doesn't do it to integers. Correct this.
            if precision == 0:
                latex_value = latex_value.replace('.0', '')
            
            # Escape the % symbol for LaTeX
            latex_value = latex_value.replace('%', '\\%')

            # Return the formatted value
            return latex_value

            # Exit the loop
            break
    
    # If no non-numeric characters were found we're dealing with a unitless value
    return latex_value

def linebreaks(text, format='text'):
    
    # This function splits a cell's text on "\\\\" linebreak markers and returns a list
    # of formatted lines. Previously this wrapped lines in a nested \\begin{array} mini-table,
    # but KaTeX does not support [t] top-alignment on nested arrays. Instead, each line
    # is returned separately so the caller can emit them as individual parent array rows.
    # This ensures top-left alignment across all columns and works with both KaTeX and MathJax.

    # Split the text on "\\\\" (which is how the user writes linebreaks in their input)
    lines = text.split('\\\\')

    # Format text columns (description, reference) as sans-serif
    if format == 'text':
        # Wrap each non-empty line in \\small and \\textsf for consistent text formatting
        # Empty lines become empty strings (blank cells in that row)
        return ['{\\small{\\textsf{' + ln + '}}}' if ln else '' for ln in lines]
    
    # Format math columns (equation) with indentation on continuation lines
    else:
        result = []
        # Step through each line with its index
        for i, ln in enumerate(lines):
            # Empty lines become blank cells
            if not ln:
                result.append('')
            # The first line renders at normal position (no indent)
            elif i == 0:
                result.append('{\\small{' + ln + '}}')
            # Continuation lines get a 2em indent so it's clear they belong to the line above
            else:
                result.append('\\hspace{2em}{\\small{' + ln + '}}')
        # Return the list of formatted math lines
        return result

#%%
def _resolve_notebook_path(notebook_name):
    """
    Resolve a notebook filename against the current working directory.

    Users pass only a filename like "beam.ipynb". This keeps behavior
    deterministic and avoids brittle notebook path auto-detection.
    """
    if not isinstance(notebook_name, str) or notebook_name.strip() == '':
        raise ValueError('notebook_name must be a non-empty string like "beam.ipynb"')

    normalized_name = notebook_name.strip()
    if os.path.basename(normalized_name) != normalized_name:
        raise ValueError('Use filename only (no path), e.g. "beam.ipynb"')

    cwd = os.getcwd()
    notebook_path = os.path.abspath(os.path.join(cwd, normalized_name))
    return notebook_path, cwd

#%%
def _serialize_var(value):
    """
    Serialize a Python variable to a JSON-safe dict.
    
    Supported types:
    - int, float, str, bool, None → JSON native
    - pint.Quantity → {"__type__": "pint", "magnitude": float, "unit": str}
    - list, tuple → JSON array (tuple wrapped in {"__type__": "tuple", "items": [...]})
    - Anything else (functions, classes, numpy arrays) → returns None (will be skipped)
    
    Returns the serialized value, or None if it cannot be serialized.
    """
    # JSON native types
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    
    # pint.Quantity
    if isinstance(value, ureg.Quantity):
        return {
            "__type__": "pint",
            "magnitude": float(value.magnitude),
            "unit": str(value.units)
        }
    
    # Tuple: wrap in a tagged dict
    if isinstance(value, tuple):
        items = []
        for item in value:
            serialized = _serialize_var(item)
            if serialized is None and item is not None:
                return None  # Can't serialize tuple with non-serializable items
            items.append(serialized)
        return {
            "__type__": "tuple",
            "items": items
        }
    
    # List: recursively serialize items
    if isinstance(value, list):
        items = []
        for item in value:
            serialized = _serialize_var(item)
            if serialized is None and item is not None:
                return None  # Can't serialize list with non-serializable items
            items.append(serialized)
        return items
    
    # Everything else (functions, classes, numpy arrays, etc.) is not serializable
    return None

#%%
def _deserialize_var(data):
    """
    Deserialize a JSON dict back to a Python variable.
    
    Handles the reverse of _serialize_var, reconstructing pint.Quantity objects
    using the module's ureg unit registry.
    
    Returns the deserialized value.
    """
    # JSON native types or None
    if data is None or isinstance(data, (bool, int, float, str)):
        return data
    
    # Tagged pint.Quantity
    if isinstance(data, dict) and data.get("__type__") == "pint":
        magnitude = data["magnitude"]
        unit_str = data["unit"]
        return ureg.Quantity(magnitude, unit_str)
    
    # Tagged tuple
    if isinstance(data, dict) and data.get("__type__") == "tuple":
        items = []
        for item in data["items"]:
            items.append(_deserialize_var(item))
        return tuple(items)
    
    # Plain list: recursively deserialize items
    if isinstance(data, list):
        items = []
        for item in data:
            items.append(_deserialize_var(item))
        return items
    
    # Fallback: return as-is
    return data

#%%
def save_vars(notebook_name):
    """
    Save all user-defined variables to a sidecar JSON file.

    Variables are written to .ipycalc_vars/<stem>.json in the same directory
    as the notebook. Each call completely replaces any prior saved variables
    (no merging). The notebook file itself is never modified.

    notebook_name must be a filename in the current working directory.

    Skips:
    - Names starting with underscore
    - Unit shortcuts (from unit_list)
    - ipycalc internals (ureg, funit, save_vars, import_vars, etc.)
    - Non-data types (functions, classes, modules, types)
    """
    try:
        notebook_path, _ = _resolve_notebook_path(notebook_name)

        # Confirm the target notebook exists so typos don't create orphan sidecar files.
        if not os.path.exists(notebook_path):
            raise ValueError(f"Notebook not found: {notebook_path}")

        # Get the IPython user namespace
        ip = get_ipython()
        user_ns = ip.user_ns

        # Build the list of variables to skip
        skip_list = set(unit_list + [
            'ureg', 'funit', 'save_vars', 'import_vars',
            'In', 'Out', 'exit', 'quit', 'get_ipython',
            '_', '__', '___', '_i', '_ii', '_iii',
            '_oh', '_sh', '_dh', 'exit', 'quit'
        ])

        # Serialize each variable
        ipycalc_vars = {}
        for var_name, var_value in user_ns.items():
            # Skip if name starts with underscore
            if var_name.startswith('_'):
                continue
            
            # Skip if in skip list
            if var_name in skip_list:
                continue

            # Skip functions, classes, modules, types, etc.
            if callable(var_value) or hasattr(var_value, '__module__'):
                if not isinstance(var_value, (int, float, str, bool, type(None), ureg.Quantity)):
                    continue

            # Try to serialize the variable
            serialized = _serialize_var(var_value)
            if serialized is not None or var_value is None:
                ipycalc_vars[var_name] = serialized

        # Resolve sidecar path: .ipycalc_vars/<stem>.json
        notebook_dir = os.path.dirname(notebook_path)
        stem = os.path.splitext(os.path.basename(notebook_path))[0]
        vars_dir = os.path.join(notebook_dir, '.ipycalc_vars')
        os.makedirs(vars_dir, exist_ok=True)
        vars_path = os.path.join(vars_dir, stem + '.json')

        # Write variables to sidecar file (completely overwrite, no merging)
        with open(vars_path, 'w', encoding='utf-8') as f:
            json.dump(ipycalc_vars, f, indent=2)

        print(f"Saved {len(ipycalc_vars)} variable(s) to {vars_path}")

    except ValueError as e:
        print(f"Error saving variables: {str(e)}")
    except Exception as e:
        print(f"Error saving variables: {str(e)}")

#%%
def import_vars(notebook_name, *var_names):
    """
    Import variables from another notebook in the current working directory.
    
    Reads the sidecar file .ipycalc_vars/<stem>.json associated with the
    specified notebook and injects those variables into the current IPython
    namespace.
    
    Parameters:
    -----------
    notebook_name : str
        The filename of the notebook to import from (e.g., 'beam.ipynb').
        Must be in the current working directory.
    
    *var_names : str (optional)
        Variable names to import. If provided, only these variables are imported.
        If not provided, all saved variables are imported.
    
    Raises ValueError if the notebook is not found or has no saved variables.
    Prints warnings for any variables that already exist in the current namespace.
    """
    try:
        source_path, _ = _resolve_notebook_path(notebook_name)

        # Confirm source notebook exists before attempting sidecar import.
        if not os.path.exists(source_path):
            raise ValueError(f"Notebook not found: {source_path}")

        # Resolve sidecar path: .ipycalc_vars/<stem>.json
        notebook_dir = os.path.dirname(source_path)
        stem = os.path.splitext(os.path.basename(source_path))[0]
        vars_path = os.path.join(notebook_dir, '.ipycalc_vars', stem + '.json')

        if not os.path.exists(vars_path):
            raise ValueError(
                f"No saved variables found for {notebook_name} "
                f"(expected {vars_path})"
            )

        # Read the sidecar JSON
        with open(vars_path, 'r', encoding='utf-8') as f:
            ipycalc_vars = json.load(f)

        if not ipycalc_vars:
            raise ValueError(f"No saved variables found in {notebook_name}")
        
        # Get the IPython namespace
        ip = get_ipython()
        user_ns = ip.user_ns
        
        # Filter variables if var_names were specified
        if var_names:
            filtered_vars = {}
            for var_name in var_names:
                if var_name in ipycalc_vars:
                    filtered_vars[var_name] = ipycalc_vars[var_name]
                else:
                    print(f"Warning: Variable '{var_name}' not found in {notebook_name}")
            ipycalc_vars = filtered_vars
        
        # Deserialize and inject each variable
        imported_count = 0
        for var_name, var_data in ipycalc_vars.items():
            # Check if variable already exists and warn
            if var_name in user_ns:
                print(f"Warning: Variable '{var_name}' already exists. Overwriting.")
            
            # Deserialize the variable
            var_value = _deserialize_var(var_data)
            
            # Inject into IPython namespace
            user_ns[var_name] = var_value
            
            # Also add to module globals for consistency
            globals()[var_name] = var_value
            
            imported_count += 1
        
        print(f"Imported {imported_count} variable(s) from {notebook_name}")
        
    except ValueError as e:
        print(f"Error importing variables: {str(e)}")
    except Exception as e:
        print(f"Unexpected error importing variables: {str(e)}")
