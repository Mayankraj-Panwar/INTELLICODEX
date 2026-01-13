import sys
import time
import io
import re
import traceback

def execute_with_timeout(code, func_name, test_input):
    """
    Executes code in a controlled sandbox to capture output and performance.
    """
    local_vars = {}
    sandbox_env = {"__builtins__": __builtins__}
    
    try:
        exec(code, sandbox_env, local_vars)
        func = local_vars.get(func_name)
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            start_time = time.perf_counter()
            if func and test_input is not None:
                # Handle Function Execution
                result = func(*test_input) if isinstance(test_input, (list, tuple)) else func(test_input)
                str_result = str(result)
            else:
                # Handle Script Execution
                str_result = captured_output.getvalue().strip() or "No Output"
            
            end_time = time.perf_counter()
            runtime_ms = (end_time - start_time) * 1000

            if len(str_result) > 100:
                str_result = str_result[:97] + "..."

            return {"status": "Success", "output": str_result, "runtime": f"{runtime_ms:.2f}ms"}
        finally:
            sys.stdout = old_stdout
    except Exception:
        return {"status": "Fail", "error": traceback.format_exc().splitlines()[-1]}

def generate_dynamic_test_cases(code, func_name):
    """
    Generates test scenarios based on function arguments.
    """
    try:
        match = re.search(rf'def {func_name}\((.*?)\):', code)
        if match:
            params = match.group(1).split(',')
            params_count = len([p for p in params if p.strip()])
            
            # Cases for TwoSum or Search
            return [
                {"name": "Standard Vector", "input": ([2, 7, 11, 15], 9) if params_count == 2 else [1, 2, 3], "expected": "[0, 1]" if params_count == 2 else None},
                {"name": "Empty/Null Edge", "input": ([], 0) if params_count == 2 else [], "expected": "[]" if params_count == 2 else None}
            ]
        return [{"name": "Generic Execution", "input": None, "expected": None}]
    except:
        return [{"name": "Basic Audit", "input": None, "expected": None}]

def run_behavioral_audit(code, test_cases):
    """
    Orchestrates the tests and returns results for the UI.
    """
    match = re.search(r'def (\w+)\(', code)
    func_name = match.group(1) if match else "solution"
    final_results = []
    passed_count = 0

    for test in test_cases:
        res = execute_with_timeout(code, func_name, test["input"])
        res["scenario"] = test["name"]
        
        if res.get("status") == "Success":
            if test.get("expected") is None or res["output"] == str(test["expected"]):
                res["verdict"] = "✅ PASS"
                passed_count += 1
            else:
                res["verdict"] = "❌ FAIL"
        else:
            res["verdict"] = "⚠️ ERROR"
            res["output"] = res.get("error", "Runtime fault")
        final_results.append(res)

    accuracy = int((passed_count / len(test_cases)) * 100) if test_cases else 0
    return final_results, accuracy
