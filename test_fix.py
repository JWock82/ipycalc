import sys
sys.path.insert(0, r'c:\Users\craig\Documents\Python\ipycalc')

# Force reload
if 'ipycalc' in sys.modules:
    del sys.modules['ipycalc']
if 'ipycalc.calc' in sys.modules:
    del sys.modules['ipycalc.calc']

from ipycalc.calc import python_to_latex

# Test case: D_c**2 in a fraction context  
test_input = "pi*(((D_c + 2*t_w)**2)/(4) - (D_c**2)/(4))"
result = python_to_latex(test_input)
print("Input:", test_input)
print("Output:", result)
print()

# Check if the problematic pattern appears
if "D_{c^{{2}}}" in result:
    print("❌ PROBLEM: Found D_{c^{{2}}} - exponent nested in subscript!")
elif "{D_{c}}^{2}" in result:
    print("✓ GOOD: Found {D_{c}}^{2} - properly wrapped!")
elif "D_{c}^{2}" in result:
    print("⚠ OK: Found D_{c}^{2} - flat but acceptable")
else:
    print("? Pattern not found, full output:")
    print(result)
