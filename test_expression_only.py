"""Test that expression-only lines work without variable assignment."""
import sys
import importlib.util
sys.path.insert(0, r'c:\Users\craig\Documents\Python\ipycalc')

# Mock IPython environment so register_cell_magic doesn't fail
from unittest.mock import MagicMock
import builtins
builtins.get_ipython = MagicMock()

# Load calc.py directly, bypassing __init__.py which requires nbconvert
spec = importlib.util.spec_from_file_location("calc", r"c:\Users\craig\Documents\Python\ipycalc\ipycalc\calc.py")
calc_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc_module)
process_line = calc_module.process_line

# Simulate a local namespace with variables a and b defined
local_ns = {'a': 10, 'b': 5}
# Also inject into the calc module's global namespace (since process_line uses eval() in its own globals)
calc_module.a = 10
calc_module.b = 5

# Test 1: Expression-only line "a/b -> 2"
print("Test 1: Expression-only 'a/b -> 2'")
try:
    result = process_line("a/b -> 2", local_ns)
    print("  LaTeX output:", repr(result))
    assert 'a_over_b' not in local_ns, "Variable 'a_over_b' should NOT be assigned"
    assert 'a/b' not in local_ns, "Variable 'a/b' should NOT be assigned"
    print("  PASS: No variable assignment made")
except Exception as e:
    print(f"  FAIL: {e}")

# Test 2: Expression-only with description "Calc: a/b -> 2"
print("\nTest 2: Expression-only with description 'Calc: a/b -> 2'")
try:
    result = process_line("Calc: a/b -> 2", local_ns)
    print("  LaTeX output:", repr(result))
    print("  PASS")
except Exception as e:
    print(f"  FAIL: {e}")

# Test 3: Normal variable assignment still works "c = a/b"
print("\nTest 3: Normal assignment 'c = a/b'")
try:
    result = process_line("c = a/b", local_ns)
    print("  LaTeX output:", repr(result))
    assert 'c' in local_ns, "Variable 'c' should be assigned"
    print(f"  c = {local_ns['c']}")
    print("  PASS")
except Exception as e:
    print(f"  FAIL: {e}")

# Test 4: Simple variable display still works "a -> 2"
print("\nTest 4: Simple variable display 'a -> 2'")
try:
    result = process_line("a -> 2", local_ns)
    print("  LaTeX output:", repr(result))
    print("  PASS")
except Exception as e:
    print(f"  FAIL: {e}")

# Test 5: Expression with addition "a + b -> 2"
print("\nTest 5: Expression-only 'a + b -> 2'")
try:
    result = process_line("a + b -> 2", local_ns)
    print("  LaTeX output:", repr(result))
    assert 'a+b' not in local_ns, "No variable should be assigned"
    print("  PASS: No variable assignment made")
except Exception as e:
    print(f"  FAIL: {e}")

print("\nAll tests done.")
