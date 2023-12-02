import os

from math import pi, sqrt, sin, cos, asin, acos, atan, tan, sinh, cosh, tanh

from IPython.core.magic import (register_cell_magic, needs_local_scope)
from IPython.display import display, Latex, HTML

# Use pint for units
import pint
directory = os.path.dirname(__file__)
ureg = pint.UnitRegistry(directory + '\\ipycalc_en.txt')  # Creates the units registry
ureg.default_system = 'US'  # US Customary unit system
ureg.default_format = '~P'  # Shorthand units w/ pretty formatting
ureg.define('plf = pound_force / foot')
ureg.define('klf = kip / foot')
ureg.define('psf = pound_force / foot**2')
ureg.define('pcf = pound_force / foot**3')
ureg.define('ksi = kip / inch**2')
ureg.define('ksf = kip / foot**2')
ureg.define('lbm = pound')

# Create shortcuts to the unit registry's units in this module's namespace
inch = ureg.inch
ft = ureg.foot
feet = ureg.foot
mi = ureg.mile
ozf = ureg.force_pound/16
lbf = ureg.force_pound
lbm = ureg.pound
kip = ureg.kip
ton = ureg.ton
tonf = ureg.force_ton
plf = ureg.plf
klf = ureg.klf
psi = ureg.force_pound/ureg.inch**2
psf = ureg.psf
ksi = ureg.kip/ureg.inch**2
ksf = ureg.kip/ureg.foot**2
pcf = ureg.force_pound/ureg.foot**3
kcf = ureg.kip/ureg.foot**3
lbin = ureg.force_pound*ureg.inch
lbft = ureg.force_pound*ureg.foot
kipin = ureg.kip*ureg.inch
kipft = ureg.kip*ureg.foot
kin = ureg.kip*ureg.inch
kft = ureg.kip*ureg.foot
mph = ureg.mile/ureg.hour
deg = ureg.degree
rad = ureg.radian
sec = ureg.second
hr = ureg.hour

# Add some useful metric units
mm = ureg.millimeter
cm = ureg.centimeter
m = ureg.meter
km = ureg.kilometer
N = ureg.newton
kN = ureg.kilonewton
ton = ureg.metric_ton
tonnef = ureg.force_metric_ton
Pa = ureg.pascal
kPa = ureg.kilopascal
MPa = ureg.megapascal
GPa = ureg.gigapascal

unit_list = ['inch', 'feet', 'ft', 'mi', 'ozf', 'lbf', 'lbm', 'kip', 'plf', 'klf', 'psi', 'psf', 
             'ksi', 'ksf', 'pcf', 'kcf', 'lbin', 'lbft', 'kipin', 'kipft', 'kin', 'kft', 'mph',
             'sec', 'hr', 'deg', 'rad', 'mm', 'cm', 'm', 'km', 'N', 'kN', 'Pa', 'kPa', 'MPa', 'GPa']

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
    
    # Start the output text
    text = '\\begin{array}{lpwidth{0.25\\linewidth} lpwidth{0.5\\linewidth} lpwidth{0.25\\linewidth}}\n'

    # Process each code line
    for ln in code_lines:
        text += process_line(ln, local_ns)

    # Display the cell's results
    text += '\\end{array}'

    # IPython will try to center the output in the output cell since it's a table. Rendering to
    # HTML first will cause IPython to treat it as left-justified HTML. $ tags are needed to tell
    # HTML that this is Latex.
    display(HTML('$' + text + '$'))
    
    # Alternatively, for center-justified tables bypassing HTML, use the next line instead.
    # display(Latex(text))

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
    local_ns['ozf'] = ureg.force_pound/16
    local_ns['lbf'] = ureg.force_pound
    local_ns['lbm'] = ureg.pound
    local_ns['kip'] = ureg.kip
    local_ns['k']= ureg.kip
    local_ns['ton'] = ureg.ton
    local_ns['tonf'] = ureg.force_ton
    local_ns['plf'] = ureg.plf
    local_ns['klf'] = ureg.klf
    local_ns['psi'] = ureg.force_pound/ureg.inch**2
    local_ns['psf'] = psf
    local_ns['ksi'] = ureg.kip/ureg.inch**2
    local_ns['ksf'] = ureg.kip/ureg.foot**2
    local_ns['pcf'] = ureg.force_pound/ureg.foot**3
    local_ns['kcf'] = ureg.kip/ureg.foot**3
    local_ns['lbin'] = ureg.force_pound*ureg.inch
    local_ns['lbft'] = ureg.force_pound*ureg.foot
    local_ns['kipin'] = ureg.kip*ureg.inch
    local_ns['kipft'] = ureg.kip*ureg.foot
    local_ns['kin'] = ureg.kip*ureg.inch
    local_ns['kft'] = ureg.kip*ureg.foot
    local_ns['mph'] = ureg.mile/ureg.hour
    local_ns['sec'] = ureg.second
    local_ns['hr'] = ureg.hour
    local_ns['deg'] = ureg.degree
    local_ns['rad'] = ureg.radian
    
    # Add some useful metric units
    local_ns['mm'] = ureg.millimeter
    local_ns['cm'] = ureg.centimeter
    local_ns['m'] = ureg.meter
    local_ns['km'] = ureg.kilometer
    local_ns['N'] = ureg.newton
    local_ns['kN'] = ureg.kilonewton
    local_ns['kg'] = ureg.kilogram
    local_ns['Pa'] = ureg.pascal
    local_ns['kPa'] = ureg.kilopascal
    local_ns['MPa'] = ureg.megapascal
    local_ns['GPa'] = ureg.gigapascal
    local_ns['tonne'] = ureg.metric_ton
    local_ns['tonnef'] = ureg.force_metric_ton

    # Provide the IPython console with access to the `funit` method
    local_ns['funit'] = funit

#%%
def process_line(calc_line, local_ns):

    # Ampersand symbols will mess with latex table formatting unless they have a `\` in front of
    # them
    calc_line = calc_line.replace('&', '\&')

    # Break up the line into components: `description`, `variable`, `equation`, `value` and `reference`
    if '#' in calc_line:
        description, reference = calc_line.split('#', 1)
    else:
        description, reference = calc_line, ''
    
    if ':' in calc_line:
        description, variable = description.split(':', 1)
    else:
        description, variable = '', description
    
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

    # Remove leading and trailing whitespace from all the components except the equation. The
    # equation is a Python expression that may need the spaces.
    description = description.strip()
    variable = variable.strip()
    value_format = value_format.strip()

    # Format the equation to be Python friendly
    equation = equation.replace('^prime', '_prime')
    equation = equation.replace('^', '**')

    # Resolve prime symbols in the variable before we compare it to the equation, which has already
    # had them resolved
    variable = variable.replace('^prime', '_prime')

    # Make a latex copy of the equation and variable before we switch out square root symbols
    latex_variable = python_to_latex(variable)
    latex_equation = python_to_latex(equation)

    # `Pint` prefers exponents to the 1/2 power instead of square roots
    equation = alt_sqrt(equation)

    # Handle manually inserted line breaks placed in the line by the user
    description = description.replace('\\\\', '} \\\\ \\textsf{')
    equation = equation.replace('\\\\', '')
    reference = reference.replace('\\\\', '} \\\\ \\textsf{')
    
    # Turn off pretty printing momentarily while we prepare a Python expression for the value
    ureg.default_format = '~'

    # Determine the requested unit format
    if '*' in value_format:
        # Both precision and units were requested
        precision, unit = value_format.split('*', 1)
        precision = int(precision)
    elif value_format != '':
        # Precision was requested without units
        precision, unit = value_format, None
        precision = int(precision)
    else:
        # No precision and no units were requested
        precision = None
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

    # Sometimes the user may want to display a value without an equation
    if equation == '':

        if unit != None:
            value = str((eval(variable).to(unit)).magnitude) + '*' + unit
        elif precision != None:
            # Unitless values require special consideration. Pint leaves values in terms of the
            # units used to calculate them. That means 60 ft / 12 in = 5 ft/in instead of 60.
            # As a workaround we'll convert that quantity to some units that cancel each other out.
            # In cases where there are no units (a pure float) we'll need to tag on some units
            # to make the `to` function available. These units should also cancel each other out.
            value = str((eval(variable)*inch/inch).to(inch/inch))
        else:
            value = str(eval(variable))

    else:

        if unit != None:
            value = str((eval(equation).to(unit)).magnitude) + '*' + unit
        elif precision != None:
            # Unitless values require special consideration. Pint leaves values in terms of the
            # units used to calculate them. That means 60 ft / 12 in = 5 ft/in instead of 60.
            # As a workaround we'll convert that quantity to some units that cancel each other out.
            # In cases where there are no units (a pure float) we'll need to tag on some units
            # to make the `to` function available. These units should also cancel each other out.
            value = str((eval(equation)*inch/inch).to(inch/inch))
        else:
            value = str(eval(equation))
    
    # 'in' is a keyword in Python. Remove it from the expression we just created and replace it with 'inch'
    value = value.replace('inch', '@@@@')  # Used to prevent 'inchch' after the next line runs
    value = value.replace('in', 'inch')
    value = value.replace('@@@@', 'inch')
    value = value.strip()
    
    # In the case of dimensionless units due to units canceling out, there will be an extra '*' at
    # the end of the value we need to eliminate
    if value[-1] == '*':
        value = value[0:-1]
    
    # Turn pretty printing back on
    ureg.default_format = '~P'
    
    # Format the description
    if description != '':
        description = description + ': '
    
    # Format the variable to be Python friendly
    variable = variable.replace('(', '')
    variable = variable.replace(')', '')
    variable = variable.replace(',', '')  # Allowing commas in variable names would get messy
    variable = variable.replace(' ', '')

    # Create a Latex version of the value
    latex_value = ''
    if value_format != '' or equation == '':

        if unit != None:
            latex_value = '=' + funit(eval(value), precision)
        elif precision != None:
            latex_value = '=' + funit((eval(value)*inch/inch).to(inch/inch), precision)
        else:
            latex_value = str(eval(value))

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

    # Return the line formatted in all its glory
    latex_text =  '\\small{\\textsf{' + description + '}} & ' + '\\small{' + latex_variable + latex_equation + latex_value + '} & \\small{\\textsf{' + reference + '}} \\\\\n'
    
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
    
    # Change spaces we want to keep to the '@' symbol temporarily
    text = text.replace(' if ', '@if@')
    text = text.replace(' else ', '@else@')

    # Add any prime symbols back in
    text = text.replace('_prime', '^{\\prime}')

    # Switch out Python's exponent symbols for Latex's
    text = text.replace('**', '^')

    # Add brackets to superscripts and subscripts if they are missing
    text = sscript_curly('^', text)
    text = sscript_curly('_', text)

    # Adjust inequality symbols
    text = text.replace('<=', ' \\le ')
    text = text.replace('>=', ' \\ge ')
    text = text.replace('!=', ' \\neq ')

    # Process 'if' statements first, since they require spaces
    if '@if@' in text:
        text = process_if(text, level=1, type='if')

    # Remove spaces from the raw text
    text = text.replace(' ', '')

    # Define a list of greek symbols
    greek = (['alpha', 'eta', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'omega', 'Alpha', 'Eta', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega'])
    
    # Clean up any greek symbols
    for symbol in greek:
        if symbol in text:
            text = text.replace(symbol, '\\' + symbol + ' ')
    
    # Fix any errors caused by `eta` being similar to other symbols
    text = text.replace('b\\eta', '\\beta')
    text = text.replace('th\\eta', '\\theta')
    text = text.replace('z\\eta', '\\zeta')
    
    # Take care of any lower case greek psi characters. This is necessary because 'psi' is also a unit
    text = text.replace('grpsi', '\\psi')

    #

    # Convert common functions to latex
    text = text.replace('sin', '\\sin')
    text = text.replace('cos', '\\cos')
    text = text.replace('tan', '\\tan')
    text = text.replace('a\\sin', '\\arcsin')
    text = text.replace('a\\cos', '\\arccos')
    text = text.replace('a\\tan', '\\arctan')
    text = text.replace('arc\\sin', '\\arcsin')
    text = text.replace('arc\\cos', '\\arccos')
    text = text.replace('arc\\tan', '\\arctan')
    text = text.replace('min', '\\min')
    text = text.replace('max', '\\max')

    # Adjust a few more special characters to be Latex friendly
    text = text.replace('*', ' \\cdot{}')
    text = text.replace('sqrt', '\\sqrt')

    # Change any parentheses to brackets for `sqrt`, `^`, and `_`
    text = curly_brackets('sqrt', text)
    text = curly_brackets('^', text)
    text = curly_brackets('_', text)

    # Format fractions
    text = frac(text)

    # Change out normal parentheses for auto-sizing parentheses
    text = text.replace('(', '\\left(')
    text = text.replace(')', '\\right)')

    # Convert '@' symbols back to spaces
    text = text.replace('@', ' ')

    # Remove the multiplicate dot in front of any units
    text = text.replace('\\cdot{}inch', ' \\ in')
    for unit in unit_list:
        text = text.replace('\\cdot{}' + unit, ' \\ ' + unit)

    # Return the Latex text
    return text

def process_if(text, level, type):
    
    # Note: 'if' statements nested in the first return value are not supported yet. 'If' statements
    # nested after the first 'else' are supported.

    # Split the line into 'if' and 'else' portions
    if 'else' in text:
        if_text, else_text = text.split('else', 1)
    else:
        if_text, else_text = text, ''
    
    # Split the 'if' portion into the condition and value
    value, condition = if_text.split('if', 1)

    # Check if the 'if' is an really an 'if' or if it's an 'elif'
    if type == 'if':
        # Add an 'if' line
        latex_text = value + '\\textsf{@if@}' + condition + '\\\\'
    elif type == 'elif':
        # Add an 'else if' line
        latex_text = '\\hspace{1cm}'  + '\\textsf{else@}' + value + '\\textsf{@if@}' + condition + '\\\\'

    # Check for an 'else' condition without an 'if' in it
    if '@if@' not in else_text:
        # Add the 'else' text
        latex_text += '\\hspace{1cm}' + '\\textsf{else@}' + else_text + '\\\\'
    
    # Evaluate 'if' statements nested in the 'else' statement
    elif else_text != '':

        # Remove any whitespace at the ends of the else text
        else_text = else_text.strip()

        # Remove parentheses at the ends of the else text
        if else_text[0] == '(': else_text = else_text[1:]
        if else_text[-1] == ')': else_text = else_text[0:-1]

        # Use recursion to evaluate the nested 'if' statement
        latex_text += process_if(else_text, level=2, type='elif')
    
    if level == 1:
        latex_text += '\\hspace{0.5cm}'

    return latex_text

#%%
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
            while j < len(text) and text[j] not in ['+', '-', '*', '/', '=', '>', '<', '!', ',', '@']:

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

    # Step through each character in the value
    for i, char in enumerate(latex_value):

        # Find the first non-numeric non-decimal character
        if not latex_value[i].isnumeric() and latex_value[i] !='.':

            # Add a space between the value and the units
            latex_value = latex_value[0:i] + ' \\ ' + latex_value[i:len(latex_value)]

            # The round function tags on a .0 after it rounds floats. It doesn't do it to integers. Correct this.
            if precision == 0:
                latex_value = latex_value.replace('.0', '')                

            # Return the formatted value
            return latex_value

            # Exit the loop
            break
    
    # If no non-numeric characters were found we're dealing with a unitless value
    return latex_value

#%%
# @register_line_magic
# @needs_local_scope
# def print_calc(line, local_ns):

#     line = line.strip()

#     if line == '':
#         dir = local_ns['_dh'][0] + '\\ipycalc_Notebook.pdf'
#     else:
#         dir = line

#     exec('!jupyter nbconvert \'' + dir + '\' --to=ipycalc')
