import ast

def get_suggestions(code):
    """
    Analyzes code patterns to provide actionable improvement suggestions.
    """
    suggestions = []
    
    try:
        tree = ast.parse(code)
    except Exception:
        return ["⚠️ System cannot provide suggestions on code with Syntax Errors."]

    # 1. Check for range(len()) -> Suggest enumerate()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == 'range':
                if node.args and isinstance(node.args[0], ast.Call):
                    if isinstance(node.args[0].func, ast.Name) and node.args[0].func.id == 'len':
                        suggestions.append("Consider using `enumerate()` instead of `range(len())` for cleaner iteration.")

    # 2. Check for Manual Counter in Loops
    # (If a loop has i += 1, suggest enumerate)
    if " += 1" in code and ("for " in code or "while " in code):
        suggestions.append("Detected manual counter. Pythonic way is to use `enumerate()` or `zip()`.")

    # 3. List Comprehension Suggestion
    if ".append(" in code and "for " in code:
        suggestions.append("Simple loops with `.append()` can be converted to **List Comprehensions** for faster execution.")

    # 4. Global Variable Usage
    if "global " in code:
        suggestions.append("Avoid using `global` variables. Try passing variables as function arguments to improve modularity.")

    # 5. File Handling
    if "open(" in code and "with " not in code:
        suggestions.append("Always use the `with open(...)` statement for file operations to ensure proper resource management.")

    # 6. Data Structure Optimization
    if " in " in code and ("[" in code or "(" in code) and "{" not in code:
        # Checking if searching in list/tuple instead of set
        suggestions.append("If you are performing frequent membership checks ('in' operator), using a `set()` is $O(1)$ compared to $O(N)$ for a list.")

    # 7. Built-in Function Suggestions
    if "sorted(" not in code and ".sort(" not in code and ("for" in code and "if" in code):
        if "min" in code or "max" in code:
            pass # already using built-ins
        else:
            suggestions.append("Check if Python's built-in functions like `map()`, `filter()`, or `any()` can replace your manual loop logic.")

    # 8. Documentation Check
    if "def " in code and '"""' not in code and "'''" not in code:
        suggestions.append("Add **Docstrings** to your functions. It makes the code 'Production-Ready' and easier to maintain.")

    # Default if code is already perfect
    if not suggestions:
        suggestions.append("🔥 Code looks very professional! Consider adding Type Hinting (e.g., `def func(a: int) -> str:`) for extra clarity.")

    return list(set(suggestions)) # Remove duplicates
    st.success("⚡ Audit Initiated!")
    