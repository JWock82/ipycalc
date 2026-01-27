import os
import re

from math import pi, sqrt, sin, cos, asin, acos, atan, tan, sinh, cosh, tanh, log, log10

from IPython.core.magic import (register_cell_magic, needs_local_scope)
from IPython.display import display, Latex, HTML, Markdown

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

    # Provide the IPython console with access to the `funit` method
    local_ns['funit'] = funit

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
    
    # Format the variable to be Python friendly
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
    
    # Add the variable and its value to this module's global namespace
    exec('global ' + variable + '; ' + variable + '=' + value)

    # Add the variable and its value to the IPython console's namespace
    local_ns[variable] = eval(value)
    
    # Add the equals sign between the variable and equation
    latex_variable = latex_variable + '='

    # Format the reference
    reference = reference.strip()
    # Escape ampersand symbols for latex table formatting
    reference = reference.replace('&', r'\&')

    # Return the line formatted in all its glory
    latex_text = linebreaks(description, 'text') + '&' + linebreaks(latex_variable + latex_equation + latex_value, 'math') + '&' + linebreaks(reference, 'text') + '\\\\ \n'

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
        
        text = text.replace('(' + num + ')/(' + denom + ')', '\\dfrac{' + num + '}{' + denom + '}')

    # Correct any remaining instances of `\\dfrac{a}{b}^{c}` to be `\\dfrac{a}{b^c}`
    pattern = r"\\dfrac\{(.*?)\}\{(.*?)\}\^\{(.*?)\}"
    repl = r"\\dfrac{\1}{\2^{{\3}}}"
    text = re.sub(pattern, repl, text)
    
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
    
    # Normally in Latex a simple \\ will create a linebreak. However, MathJax in Jupyter applies the line break across the entire row of a table array, rather than just across the individual cell. To work around this, we'll use another table array within the table cell to contain the linebreak to just the cell.

    # Note that \\ becomes \\\\ when formatted as a string in Python since \ is considered an escape character in Python.

    # Format text with linebreaks
    if format == 'text':
        text = text.replace('\\\\', '}}} \\\\ {\\small{\\textsf{')
        # return '\\begin{array}{@{}l@{}} {\\small{\\textsf{' + text + '}}} \\end{array}'
        return '\\begin{array}{l} {\\small{\\textsf{' + text + '}}} \\end{array}'  # This version of the line above is KaTeX friendly
    
    # Math equations having linebreaks should have an indentation at the new line for clarity reading the equation
    else:
        text = text.replace('\\\\', '}} \\\\ \\hspace{2em} {\\small{')
        # return '\\begin{array}{@{}l@{}} {\\small{' + text + '}} \\end{array}'
        return '\\begin{array}{l} {\\small{' + text + '}} \\end{array}'  # This version of the line above is KaTeX friendly
