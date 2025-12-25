🧠 IntelliCodex

Rule-Based Intelligent Python Code Evaluation & Grading System


1️⃣ Introduction
In traditional coding evaluations, judges face multiple problems:
Manual code checking is time-consuming
Output-only checking ignores code quality
AI-based evaluators lack transparency
Plagiarism tools fail to detect AI-generated code
IntelliCodex solves these problems by providing a fully automated, rule-based, execution-driven evaluation system that assesses how the code works, how it is written, and how honestly it behaves during execution.
This system is not a black box. Every decision is explainable.


2️⃣ Problem Statement
Existing online judges and academic evaluators:
Only check final output
Ignore structure, efficiency, and runtime behavior
Cannot distinguish human vs AI-generated code
Provide misleading scores for non-working code


3️⃣ Proposed Solution

IntelliCodex introduces a multi-layer evaluation pipeline:

Layer	Purpose
Static Analysis	Understand code structure
Dynamic Execution	Run real test cases
Test Generator	Validate logic correctness
Grading Engine	Score fairly & honestly
Style Detector	Identify AI-generated patterns
Reporting	Provide judge-ready results


4️⃣ System Architecture (Explained)
User Code
   ↓
Abstract Syntax Tree (AST) Analysis
   ↓
Function Extraction
   ↓
Dynamic Test Case Generation
   ↓
Secure Runtime Execution
   ↓
Scoring & Penalty Engine
   ↓
Plagiarism & Style Detection
   ↓
Visualization + PDF Report

Each stage improves evaluation accuracy.


5️⃣ Module-Wise Explanation (Deep)

🔹 analyzer.py – Static Code Analyzer

Purpose:
Analyze source code without executing it.

Techniques Used:
Python AST (Abstract Syntax Tree)
Depth-first traversal
Metrics Extracted:
Number of loops
Function count
Maximum nesting depth
Why It Matters:
High nesting → poor readability
Excess loops → inefficiency
Used to estimate complexity & penalties

🔹 executor.py – Runtime Execution Engine
Purpose:
Safely execute user-submitted Python code.
Key Capabilities:
Isolated execution environment
Runtime error capture
Execution result validation
Judge Benefit:
Code that does not run cannot score high.

🔹 test_generator.py – Real Test Case Generator
Purpose:
Automatically generate and execute test cases per function.
How It Works:
Detects user-defined functions
Generates valid input combinations
Executes each function call
Records pass/fail status
Why This Is Important:
No hardcoded test cases
Works for unknown problems
Catches logical errors

🔹 grader.py – Honest Grading Engine

Scoring Distribution:
Component	Weight
Test Case Success	60%
Time Complexity	20%
Code Structure	10%
Penalties	Variable

Penalty Rules:
Runtime error → heavy deduction
Deep nesting → score reduction
Excessive loops → readability penalty
⚠️ Bad code = low score (always)

🔹 style_detector.py – AI / LLM Plagiarism Detector
Detects:
Over-polished formatting
Generic variable naming
Template-like logic
Common ChatGPT structures
Output:
Suspicion score (0–100)
Verdict (Low / Medium / High)
Human-readable reasons

🧠 This is style-based detection, not dataset matching.

🔹 suggestions.py – Code Improvement System
Provides actionable suggestions such as:
Reduce nesting
Improve naming
Optimize loops
Follow Python best practices
Helps students learn, not just score.

🔹 ui.py – Interactive Evaluation Dashboard
Built using:
Streamlit
Plotly
Displays:
Time complexity
Difficulty level
Score gauge
Radar performance chart
Test case results
Plagiarism verdict
PDF download option

🔹 report_gen.py – Automated PDF Report Generator
Creates a submission-ready report containing:
Code metrics
Execution results
Final score
Suggestions
Plagiarism analysis
Perfect for judges & faculty records.


6️⃣ Comparison With Existing Systems
Feature	                  IntelliCodex	Traditional Judge
Executes code	                ✅	            ❌
Analyzes structure	          ✅	            ❌
AI plagiarism detection     	✅		          ❌
Transparent scoring         	✅	           	❌
PDF reporting	                ✅		          ❌
ML dependency	                ❌		          ❌


7️⃣ Technologies Used
Python 3
AST Module
Streamlit
Plotly
FPDF
Rule-based heuristics


8️⃣ Why Rule-Based (No ML)?
✔ Fast
✔ Offline
✔ Explainable
✔ Judge-friendly
✔ No dataset dependency
✔ No hallucinated scores


9️⃣ Applications
Coding competitions
University practical exams
Hackathons
Online coding labs
Interview screening tools


🔟 Final Justification for Judges
IntelliCodex evaluates code like an expert human reviewer—
by executing it, testing it, analyzing it, and scoring it fairly.

This system cannot be cheated by formatting or fake outputs, making it ideal for academic and competitive use.


📌 Conclusion

IntelliCodex is not just a grader.
It is a complete intelligent code evaluation framework.
