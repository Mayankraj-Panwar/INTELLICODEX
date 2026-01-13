import ast
import re

class StructuralAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {
            "loops": 0,
            "functions": 0,
            "max_nesting": 0,
            "complexity": 1, 
            "dead_code": 0,
            "long_functions": [],
            "issues": [],
            "big_o": "O(1)" 
        }
        self.current_depth = 0

    def visit_FunctionDef(self, node):
        self.stats["functions"] += 1
        length = node.end_lineno - node.lineno
        if length > 25:
            self.stats["long_functions"].append(node.name)
            self.stats["issues"].append(f"Function '{node.name}' is too long ({length} lines).")
        self.generic_visit(node)

    def visit_If(self, node):
        self.stats["complexity"] += 1
        self.increment_nesting(node)

    def visit_For(self, node):
        self.stats["loops"] += 1
        self.stats["complexity"] += 1
        # Anti-pattern check: range(len())
        if isinstance(node.iter, ast.Call):
            if isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                if node.iter.args and isinstance(node.iter.args[0], ast.Call):
                    if isinstance(node.iter.args[0].func, ast.Name) and node.iter.args[0].func.id == 'len':
                        self.stats["issues"].append("Anti-pattern: Use 'enumerate()' instead of 'range(len())'.")
        self.increment_nesting(node)

    def visit_While(self, node):
        self.stats["loops"] += 1
        self.stats["complexity"] += 1
        self.increment_nesting(node)

    def increment_nesting(self, node):
        self.current_depth += 1
        if self.current_depth > self.stats["max_nesting"]:
            self.stats["max_nesting"] = self.current_depth
        self.generic_visit(node)
        self.current_depth -= 1

def analyze_logic(code):
    try:
        tree = ast.parse(code)
        
        # 1. Big O Estimation Logic
        loops = 0
        nested_loops = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                loops += 1
                for child in ast.iter_child_nodes(node):
                    if any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(child)):
                        nested_loops += 1

        if nested_loops > 0: big_o = "O(n²)"
        elif loops > 0: big_o = "O(n)"
        else: big_o = "O(1)"

        # 2. Run the Structural Analyzer
        analyzer = StructuralAnalyzer()
        analyzer.visit(tree)
        analyzer.stats["big_o"] = big_o 

        # 3. Dead Code Detection
        lines = code.splitlines()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(("return", "continue", "break")):
                if i + 1 < len(lines) and lines[i+1].strip():
                    current_indent = len(line) - len(line.lstrip())
                    next_indent = len(lines[i+1]) - len(lines[i+1].lstrip())
                    if current_indent == next_indent:
                        analyzer.stats["dead_code"] += 1
                        analyzer.stats["issues"].append(f"Potential dead code detected near line {i+2}.")

        # 4. Neural Origin Detection (AI vs Human)
        ai_score = 0
        origin_reasons = []
        if re.search(r'""".*?"""', code, re.DOTALL):
            ai_score += 30
            origin_reasons.append("Professional Docstring usage detected")
        if "result =" in code or "data =" in code:
            ai_score += 15
            origin_reasons.append("Standardized variable naming")
        if analyzer.stats["functions"] > 0 and len(lines) / analyzer.stats["functions"] < 15:
            ai_score += 25
            origin_reasons.append("High modularity (AI Pattern)")

        analyzer.stats["ai_probability"] = min(ai_score, 95)
        analyzer.stats["human_probability"] = 100 - analyzer.stats["ai_probability"]
        analyzer.stats["origin_reasons"] = origin_reasons

        # 5. Final Health & Labels
        health = 100
        health -= (analyzer.stats["max_nesting"] * 5)
        health -= (len(analyzer.stats["long_functions"]) * 10)
        health -= (analyzer.stats["dead_code"] * 15)
        analyzer.stats["health"] = max(0, min(100, health))
        
        comp = analyzer.stats["complexity"]
        if comp < 5: analyzer.stats["complexity_label"] = "Low"
        elif comp < 10: analyzer.stats["complexity_label"] = "Moderate"
        else: analyzer.stats["complexity_label"] = "High"

        return analyzer.stats 

    except SyntaxError as e:
        return {"error": f"Syntax Error at line {e.lineno}: {e.msg}", "health": 0}
    except Exception as e:
        return {"error": str(e), "health": 0}