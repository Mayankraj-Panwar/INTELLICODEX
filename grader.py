import ast

def calculate_score(code, analysis, behavior_accuracy=0):
    """
    Final Neural Grading Logic.
    Bridges AST analysis and behavioral results for the HUD.
    """
    # 1. Initialize Metric Scores
    scores = {
        "correctness": 100, "efficiency": 100, "readability": 100,
        "behavior": behavior_accuracy, "total": 0, "complexity": "O(N)"
    }

    if not code.strip():
        return {"accuracy": 0, "v_str": "EMPTY", "v_desc": "No code detected.", "behavior": []}

    # 2. Correctness (Syntax Check)
    try:
        compile(code, '<string>', 'exec')
    except Exception:
        scores["correctness"] = 20 

    # 3. Efficiency & Big O Analysis (Elite vs Modest Logic)
    nesting = analysis.get("max_nesting", 0)
    has_hashmap = "{" in code or "dict(" in code

    # ELITE Logic: 1 Loop (Nesting Level 2) + Hashmap = Elite O(N). 
    # Nested loops (Nesting Level 3+) = Modest O(N²).
    if has_hashmap and nesting <= 2:
        scores["efficiency"] = 100
        scores["complexity"] = "O(N) [Elite]"
    elif nesting > 2:
        scores["efficiency"] -= 35
        scores["complexity"] = "O(N²)"
    
    # 4. Readability
    try:
        tree = ast.parse(code)
        has_docstring = any(isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) for n in tree.body)
        if not has_docstring: scores["readability"] -= 20
    except:
        has_docstring = False

    # 5. Final Calculation (Weighted Average)
    total = (scores["correctness"] * 0.40) + (scores["efficiency"] * 0.30) + \
            (scores["readability"] * 0.15) + (scores["behavior"] * 0.15)
    
    total_int = int(total)
    
    # 6. Verdict Mapping
    if total_int >= 85:
        v_name, v_desc = "ELITE", "Highly Optimized: Architecture is evergreen."
    elif total_int >= 55:
        v_name, v_desc = "MODEST", "Caution: Functional but contains structural debt."
    else:
        v_name, v_desc = "CRITICAL", "Unsafe: Major logical or structural flaws."

    return {
        "accuracy": total_int,
        "v_str": v_name,
        "v_desc": v_desc,
        "complexity": scores["complexity"],
        "suggs": get_suggestions(analysis, has_docstring),
        "behavior": [{"input": "Neural Trace", "verdict": "✅ PASS" if behavior_accuracy > 50 else "❌ FAIL"}],
        "origin": {"health": scores["readability"], "node_counts": analysis.get('node_counts', {})}
    }

def get_final_verdict(grades, theme_overrides=None):
    """
    Standardized Verdict Mapper for IntelliCodex HUD.
    Maps results to the 'November Palette' theme.
    """
    # 1. Define the Architectural Theme Map
    THEME = {
        "ELITE": {"color": "#2ECC71", "icon": "🏆"},    # Emerald Green
        "MODEST": {"color": "#F1C40F", "icon": "⚠️"},   # Golden Yellow
        "STABLE": {"color": "#3F778C", "icon": "✅"},   # Lake Summit Blue
        "CRITICAL": {"color": "#E74C3C", "icon": "🚨"}, # Alizarin Red
        "EMPTY": {"color": "#95A5A6", "icon": "❓"}      # Concrete Gray
    }

    # 2. Extract Data from the Grade Dictionary
    v_str = grades.get("v_str", "STABLE").upper()
    v_desc = grades.get("v_desc", "System analysis complete.")

    # 3. Apply Theme (Fall back to STABLE if key is missing)
    status_theme = THEME.get(v_str, THEME["STABLE"])

    # 4. Apply theme overrides if provided
    if theme_overrides and "level_color" in theme_overrides:
        status_theme["color"] = theme_overrides["level_color"]

    return v_str, status_theme["color"], v_desc

def get_suggestions(analysis, has_docstring):
    """Generates the Roadmap suggestions."""
    suggs = []
    if analysis.get("max_nesting", 0) > 2:
        suggs.append("⚠️ **Structural Debt:** Logic is nested too deeply. Use 'Guard Clauses' to flatten the flow.")
    if not has_docstring:
        suggs.append("📝 **Documentation Gap:** Add a docstring to explain the 'Why' of this function.")
    return suggs if suggs else ["✨ Architecture is optimal. Code is Elite."]