import ast
import re

def detect_level(code, analysis_results):
    """
    LAYER 3 — STYLE & ORIGIN INTELLIGENCE
    Returns: level_name, level_label, level_color, origin_stats
    """
    
    # --- 1. COMPLEXITY LEVEL DETECTION ---
    complexity_score = 0
    complexity_score += analysis_results.get('loops', 0) * 15
    complexity_score += analysis_results.get('max_nesting', 0) * 20
    complexity_score += analysis_results.get('functions', 0) * 10
    
    if 'class ' in code: complexity_score += 40
    if 'import ' in code: complexity_score += 5
    
    # Categorize Level
    if complexity_score <= 40:
        level_name, level_label, level_color = "Beginner", "Easy", "#4CAF50" # Green
    elif complexity_score <= 85:
        level_name, level_label, level_color = "Intermediate", "Medium", "#FF9800" # Orange
    else:
        level_name, level_label, level_color = "Advanced", "Hard", "#F44336" # Red


    # --- 2. AI VS HUMAN ORIGIN DETECTION (Layer 3 Logic) ---
    ai_signals = 0
    total_checks = 6
    
    # Signal 1: Variable Uniformity (AI loves these names)
    ai_vars = ['result', 'temp', 'data', 'val', 'output', 'items', 'element']
    found_ai_vars = sum(1 for var in ai_vars if var in code.lower())
    if found_ai_vars >= 3: ai_signals += 1
    
    # Signal 2: Comment Density (AI over-comments every block)
    lines = code.splitlines()
    comment_lines = len([l for l in lines if l.strip().startswith('#')])
    code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
    if code_lines > 0 and (comment_lines / code_lines) > 0.4:
        ai_signals += 1 # Too many comments
        
    # Signal 3: No Debugging Prints (Humans leave print() everywhere)
    if 'print(' not in code:
        ai_signals += 1
        
    # Signal 4: Over-clean Formatting (Humans usually have inconsistent spacing)
    # Simple check: Is there a space after every comma and around operators?
    if re.search(r',\S', code) is None and re.search(r'[+\-*/]=\S', code) is None:
         ai_signals += 1

    # Signal 5: Docstring presence (AI almost always includes them)
    if '"""' in code or "'''" in code:
        ai_signals += 1
        
    # Signal 6: Generic Structure (Common AI templates)
    if 'if __name__ == "__main__":' in code:
        ai_signals += 0.5 # Humans use this too, but AI uses it 100% of the time

    # Calculate Probability
    ai_probability = int((ai_signals / total_checks) * 100)
    human_probability = 100 - ai_probability
    
    # Storing in analysis_results for UI access
    analysis_results['ai_probability'] = ai_probability
    analysis_results['human_probability'] = human_probability
    
    # Determine Reason
    reasons = []
    if found_ai_vars >= 3: reasons.append("Template-based variable naming")
    if comment_lines / max(1, code_lines) > 0.4: reasons.append("Excessive comment density")
    if 'print(' not in code: reasons.append("Zero debugging traces detected")
    
    analysis_results['origin_reasons'] = reasons if reasons else ["Natural coding flow detected"]

    return level_name, level_label, level_color