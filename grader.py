import ast
from style_detector import detect_level

def calculate_score(code, analysis_results=None):
    """
    Grading Logic:
    - Correctness: Based on syntax and execution (Layer 2)
    - Efficiency: Based on complexity and nesting (Layer 1)
    - Readability: Based on naming, comments, and structure
    """
    
    # Default metric scores
    scores = {
        "correctness": 100,
        "efficiency": 100,
        "readability": 100,
        "total": 0,
        "complexity_label": "O(N)"
    }

    if not code.strip():
        return {k: 0 if isinstance(v, int) else "N/A" for k, v in scores.items()}

    # --- 1. CORRECTNESS SCORE ---
    try:
        compile(code, '<string>', 'exec')
    except Exception:
        scores["correctness"] = 30  # Major penalty for syntax errors

    # --- 2. EFFICIENCY SCORE (Big O Logic) ---
    if analysis_results:
        nesting = analysis_results.get("max_nesting", 0)
        loops = analysis_results.get("loops", 0)
        
        # Penalty for deep nesting (O(N^2) or higher indicators)
        if nesting > 2:
            scores["efficiency"] -= 20
            scores["complexity_label"] = "O(N²)"
        if nesting > 4:
            scores["efficiency"] -= 30
            scores["complexity_label"] = "O(N³)"
        if loops > 3:
            scores["efficiency"] -= 10

    # --- 3. READABILITY SCORE ---
    # Check for Docstrings
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # Agar syntax galat hai, toh analysis bypass karein aur low score dein
        return {
            "correctness": 0,
            "efficiency": 0,
            "readability": 0,
            "total": 0,
            "error": "Syntax Error: Please check your code structure."
        }
    has_docstring = any(isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) for n in tree.body)
    if not has_docstring:
        scores["readability"] -= 15
        
    # Check for Comments
    if "#" not in code:
        scores["readability"] -= 15
        
    # Check for Variable Naming (Basic check for generic names)
    generic_names = ['temp', 'data', 'val', 'x', 'y', 'a', 'b']
    found_generics = sum(1 for name in generic_names if name in code.lower())
    if found_generics > 3:
        scores["readability"] -= 10

    # --- 4. FINAL CALCULATION (Weighted Average) ---
    # Correctness is most important (50%), then Efficiency (30%), then Readability (20%)
    weighted_total = (
        (scores["correctness"] * 0.5) + 
        (scores["efficiency"] * 0.3) + 
        (scores["readability"] * 0.2)
    )
    
    scores["total"] = int(weighted_total)
    
    return scores

# grader.py

def get_final_verdict(grades, style_data=None):
    total = grades.get('total', 0)
    
    # Logic based on Score (Traffic Signal)
    if total >= 80:
        # GREEN: Excellent/Advance
        v_name = "ELITE" 
        v_color = "#00FF41" # Matrix Green
        v_desc = "Safe to Deploy: Highly Optimized & Proper."
    elif total >= 50:
        # YELLOW/ORANGE: Intermediate/Medium
        v_name = "MODEST"
        v_color = "#FF9800" # Warning Orange
        v_desc = "Caution: Functional but needs refactoring."
    else:
        # RED: Critical/Poor
        v_name = "CRITICAL"
        v_color = "#FF3333" # Danger Red
        v_desc = "Unsafe: Major logical or structural errors."

    return v_name, v_color, v_desc