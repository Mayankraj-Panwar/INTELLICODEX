import ast
import re

def get_suggestions(code):
    """
    Analyzes code patterns to provide actionable improvement suggestions.
    """
    suggestions = []
    
    try:
        tree = ast.parse(code)
    except Exception:
        return ["⚠️ System cannot provide suggestions on code with Syntax Errors."]

    # 1. AST-Based Check: range(len()) -> Suggest enumerate()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == 'range':
                if node.args and isinstance(node.args[0], ast.Call):
                    if isinstance(node.args[0].func, ast.Name) and node.args[0].func.id == 'len':
                        suggestions.append("Consider using `enumerate()` instead of `range(len())` for cleaner iteration.")

    # 2. Manual Counter Logic
    if " += 1" in code and ("for " in code or "while " in code):
        suggestions.append("Detected manual counter. The Pythonic way is to use `enumerate()` or `zip()`.")

    # 3. Performance: List Comprehensions
    if ".append(" in code and "for " in code:
        suggestions.append("Simple loops with `.append()` can be converted to **List Comprehensions** for faster execution.")

    # 4. Modularity: Global Variables
    if "global " in code:
        suggestions.append("Avoid using `global` variables. Try passing variables as function arguments to improve modularity.")

    # 5. Resource Management: File Handling
    if "open(" in code and "with " not in code:
        suggestions.append("Always use the `with open(...)` statement for file operations to ensure proper resource management.")

    # 6. Algorithmic Efficiency: Membership Checks
    if " in " in code and ("[" in code or "(" in code) and "{" not in code:
        suggestions.append("For frequent membership checks, a `set()` is $O(1)$ compared to $O(n)$ for a list.")

    # 7. Professionalism: Documentation
    if "def " in code and '"""' not in code and "'''" not in code:
        suggestions.append("Add **Docstrings** (`\"\"\" ... \"\"\"`) to your functions to make them 'Production-Ready'.")

    # 8. Clean Code: Type Hinting
    if not suggestions:
        suggestions.append("🔥 Code looks very professional! Consider adding Type Hinting (e.g., `a: int`) for extra clarity.")

    # Return unique suggestions (limited to 4 for UI cleanliness)
    return list(set(suggestions))[:4]
    