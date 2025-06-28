from pyverilog.vparser.parser import parse
import json
import os

def parse_verilog(file_path):
    try:
        ast, directives = parse([file_path])
        with open(file_path, 'r') as f:
            code = f.read()
        return code
    except Exception as e:
        return f"Error parsing {file_path}: {str(e)}"

def prepare_input(verilog_file, metrics_file=None):
    verilog_code = parse_verilog(verilog_file)
    metrics = json.load(open(metrics_file)) if metrics_file and os.path.exists(metrics_file) else {
        "clock_frequency": "Unknown",
        "power_estimate": "Unknown",
        "gate_count": "Unknown"
    }

    input_data = {
        "verilog": verilog_code,
        "metrics": metrics,
        "prompt": (
            "Analyze this Verilog code and metrics for hardware flaws (timing, logic, power, security). "
            "Focus on timing violations, especially if the clock frequency is too high for the gate count (e.g., 1 GHz for 5000 gates may be unrealistic). "
            "For each flaw, provide a description, location, suggested fix (e.g., reduce clock frequency or optimize critical path), and confidence (0-100%). "
            "Return the result as a JSON array, e.g., [{'flaw': 'description', 'location': 'where', 'fix': 'solution', 'confidence': 80}]. "
            "If no flaws, return []. "
            f"Code:\n{verilog_code}\nMetrics:\n{json.dumps(metrics, indent=2)}"
        )
    }
    with open("input.json", "w") as f:
        json.dump(input_data, f, indent=2)
    return input_data

if __name__ == "__main__":
    import sys
    verilog_file = sys.argv[1] if len(sys.argv) > 1 else "dataset/design.v"
    metrics_file = sys.argv[2] if len(sys.argv) > 2 else None
    prepare_input(verilog_file, metrics_file)