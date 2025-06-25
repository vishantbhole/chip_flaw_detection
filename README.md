# Chip Flaw Detection

A lightweight tool to detect hardware flaws (timing, logic, power, security) in small chip designs (<10,000 gates) during the design phase, using a locally hosted **Mistral 7B** LLM and rule-based checks. Developed by **Vishant Bhole** on a 2017 MacBook (i7, 16 GB RAM, macOS 13.7.5), this process minimizes manufacturing costs and security risks by identifying issues early.

## Features
- Detects flaws in Verilog designs using Python 3.10, Pyverilog, and Icarus Verilog.
- Integrates Mistral 7B for advanced LLM-based analysis.
- Generates human-readable Markdown reports.
- Validates findings with Verilator (optional).
- Local execution ensures data privacy.

## Prerequisites
### Hardware
- Intel i7, 16 GB RAM, macOS 13.7.5 (or similar).
- ~15 GB free storage (~4.5 GB for Mistral 7B, ~5-10 GB for tools).

### Software
- Homebrew
- Python 3.10.18
- Ollama 0.9.2
- Pyverilog
- Icarus Verilog
- Verilator (optional)
- Python packages: `pandas`, `jinja2`

## Installation
1. **Set Up Environment**:
   ```bash
   brew update
   brew install python@3.10 ollama icarus-verilog verilator
   /usr/local/bin/python3.10 -m pip install pyverilog pandas jinja2
   ```

2. **Pull Mistral 7B**:
   ```bash
   ollama serve &
   ollama pull mistral:7b-instruct-q4_0
   ```

3. **Clone Repository**:
   ```bash
   git clone https://github.com/<your-username>/chip-flaw-detection.git
   cd chip-flaw-detection
   ```

## Project Structure
```
chip-flaw-detection/
├── preprocess.py
├── analyze_flaws.py
├── generate_report.py
├── dataset/
│   ├── design.v
│   ├── metrics.json
│   ├── flaws.json
├── README.md
```

## Usage
1. **Preprocess Verilog**:
   ```bash
   /usr/local/bin/python3.10 preprocess.py dataset/design.v dataset/metrics.json
   ```

2. **Analyze Flaws**:
   ```bash
   /usr/local/bin/python3.10 analyze_flaws.py
   ```

3. **Generate Report**:
   ```bash
   /usr/local/bin/python3.10 generate_report.py
   open flaw_report.md
   ```

4. **Validate**:
   ```bash
   verilator --lint-only dataset/design.v
   ```

## Example Output
`flaw_report.md`:
```markdown
# Flaw Detection Report

## Design
- **File**: module counter(input clk, input reset, output reg [3:0] out); always @(posedge clk or posedge rese...
- **Metrics**:
  - Clock: 100 MHz
  - Power: 50 mW
  - Gates: 5000

## Flaws

### Rule-Based
- None

### LLM Analysis
- None
```

## Troubleshooting
- **LLM Issues**:
  ```bash
  ollama list
  cat llm_output.txt
  ollama pull mistral:7b-instruct-q4_0
  ```
- **Parsing Errors**:
  ```bash
  cat dataset/design.v
  /usr/local/bin/python3.10 -m pip install --no-cache-dir pyverilog==1.3.0
  ```
- **Memory**: Close apps to free ~10 GB RAM.
- **Icarus Verilog**: `brew reinstall icarus-verilog`.

## Contributing
- Submit issues or pull requests to enhance rules, dataset, or LLM prompts.
- Expand `flaws.json` with new flaw examples.
- Contact Vishant Bhole for collaboration.

## License
MIT License. See `LICENSE` file for details.

## Acknowledgments
- Created by **Vishant Bhole**.
- Built with Mistral 7B, Pyverilog, and Ollama.
