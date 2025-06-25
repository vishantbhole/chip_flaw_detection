import subprocess
import json
import re

def run_ollama(prompt):
    try:
        process = subprocess.run(
            ["ollama", "run", "mistral:7b-instruct-q4_0"],
            input=prompt.encode(),
            capture_output=True,
            text=True,
            timeout=600
        )
        return process.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def rule_based_check(code):
    flaws = []
    # Check for missing reset in clocked blocks
    if "always @(posedge clk)" in code.lower() and "reset" not in code.lower():
        flaws.append({
            "flaw": "Missing reset signal",
            "location": "Clocked block",
            "fix": "Add asynchronous reset",
            "confidence": 90
        })
    # Check for uninitialized registers
    if "output reg" in code.lower() and not re.search(r"\w+\s*<=\s*0", code, re.IGNORECASE):
        flaws.append({
            "flaw": "Uninitialized output register",
            "location": "Output declaration",
            "fix": "Initialize register to 0",
            "confidence": 85
        })
    return flaws

def analyze_flaws(input_file):
    with open(input_file) as f:
        input_data = json.load(f)

    rule_flaws = rule_based_check(input_data["verilog"])
    llm_output = run_ollama(input_data["prompt"])
    try:
        llm_flaws = json.loads(llm_output) if llm_output.startswith("[") else []
    except:
        llm_flaws = [{"flaw": "LLM output error", "location": "N/A", "fix": "Check prompt", "confidence": 50}]

    report = {
        "design_file": input_data["verilog"][:100] + "..." if len(input_data["verilog"]) > 100 else input_data["verilog"],
        "metrics": input_data["metrics"],
        "rule_flaws": rule_flaws,
        "llm_flaws": llm_flaws
    }
    with open("flaw_report.json", "w") as f:
        json.dump(report, f, indent=2)
    return report

if __name__ == "__main__":
    analyze_flaws("input.json")