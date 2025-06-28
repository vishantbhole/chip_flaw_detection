import subprocess
import json
import re

def run_ollama(prompt):
    try:
        # Ensure prompt is a string
        prompt = str(prompt)
        # Enforce JSON output
        prompt = prompt + "\nReturn the response as a JSON array, e.g., [{'flaw': 'description', 'location': 'where', 'fix': 'solution', 'confidence': 80}]."
        process = subprocess.run(
            ["ollama", "run", "mistral:7b-instruct-q4_0"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=600
        )
        return process.stdout.strip()
    except Exception as e:
        error_msg = f"Error in Ollama: {str(e)}\nStderr: {process.stderr if 'process' in locals() else 'No process output'}"
        with open("llm_error.txt", "w") as f:
            f.write(error_msg)
        return error_msg

def rule_based_check(code):
    flaws = []
    if "always @(posedge clk)" in code.lower() and "reset" not in code.lower():
        flaws.append({
            "flaw": "Missing reset signal",
            "location": "Clocked block",
            "fix": "Add asynchronous reset",
            "confidence": 90
        })
    if "output reg" in code.lower() and not re.search(r"\w+\s*<=\s*0", code, re.IGNORECASE):
        flaws.append({
            "flaw": "Uninitialized output register",
            "location": "Output declaration",
            "fix": "Initialize register to 0",
            "confidence": 85
        })
    return flaws

def analyze_flaws(input_file):
    try:
        with open(input_file) as f:
            input_data = json.load(f)
    except Exception as e:
        error_msg = f"Error reading {input_file}: {str(e)}"
        with open("llm_error.txt", "w") as f:
            f.write(error_msg)
        return {"error": error_msg}

    rule_flaws = rule_based_check(input_data["verilog"])
    llm_output = run_ollama(input_data["prompt"])
    with open("llm_output.txt", "w") as f:
        f.write(f"LLM Output: {llm_output}\n")
    try:
        llm_flaws = json.loads(llm_output) if llm_output.startswith("[") else []
    except:
        llm_flaws = [{"flaw": "LLM output error", "location": "N/A", "fix": "Check prompt", "confidence": 50, "raw_output": llm_output}]

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