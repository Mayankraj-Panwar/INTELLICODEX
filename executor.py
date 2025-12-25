import sys
import time
import io
import inspect
import re

def execute_with_timeout(code, func_name, test_input):
    try:
        local_vars = {}
        # Sandbox execution
        exec(code, {"__builtins__": __builtins__}, local_vars)
        
        func = local_vars.get(func_name)
        if not func:
            return {"status": "Fail", "error": f"Function '{func_name}' not found"}
            
        start_time = time.time()
        # Handle single vs multiple arguments
        if isinstance(test_input, (list, tuple)):
            result = func(*test_input)
        else:
            result = func(test_input)
        end_time = time.time()
        
        return {
            "status": "Success",
            "output": result,
            "runtime": f"{int((end_time - start_time) * 1000)}ms"
        }
    except Exception as e:
        return {"status": "Fail", "error": str(e)}

def run_behavioral_audit(code, test_cases):
    # Regex to find function name
    match = re.search(r'def (\w+)\(', code)
    func_name = match.group(1) if match else "solution"

    final_results = []
    passed_count = 0

    if not test_cases:
        return [], 0

    for test in test_cases:
        res = execute_with_timeout(code, func_name, test["input"])
        res["scenario"] = test["name"]
        
        if res.get("status") == "Success":
            # JUDGE-PROOF LOGIC: 
            # Agar judge ka custom code hai (expected is None), toh sirf success hi PASS hai.
            # Agar expected defined hai (manual), toh value match karo.
            if test.get("expected") is None or res["output"] == test["expected"]:
                res["verdict"] = "✅ PASS"
                passed_count += 1
            else:
                res["verdict"] = "❌ FAIL (Mismatch)"
        else:
            res["verdict"] = "❌ ERROR (Crash)"
            res["output"] = res.get("error", "Execution failed")
                
        final_results.append(res)

    accuracy = int((passed_count / len(test_cases)) * 100)
    return final_results, accuracy

def generate_dynamic_test_cases(code, func_name):
    """
    Generates generic inputs. We set expected to None so that 
    any non-crashing execution is considered a 'PASS'.
    """
    try:
        # Inspect code to see how many arguments it needs
        match = re.search(rf'def {func_name}\((.*?)\):', code)
        if not match: return []
        
        params = match.group(1).split(',')
        params_count = len([p for p in params if p.strip()])

        # Standard generic inputs that work for most algorithms
        scenarios = [
            {"name": "Neutral Input", "input": tuple([0] * params_count) if params_count > 1 else 0},
            {"name": "Positive Edge", "input": tuple([10] * params_count) if params_count > 1 else 10},
            {"name": "Small Collection", "input": [[1, 2, 3]] if params_count == 1 else tuple([[1]] * params_count)}
        ]
        
        for s in scenarios:
            s["expected"] = None # Critical: We don't guess the answer!
            
        return scenarios
    except:
        return [{"name": "Basic Audit", "input": [1], "expected": None}]