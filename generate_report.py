import json
from jinja2 import Template

def generate_report(json_report):
    with open(json_report) as f:
        data = json.load(f)

    template = Template("""
# Flaw Detection Report

## Design
- **File**: {{ design_file | truncate(100) }}
- **Metrics**:
  - Clock: {{ metrics.clock_frequency }}
  - Power: {{ metrics.power_estimate }}
  - Gates: {{ metrics.gate_count }}

## Flaws

### Rule-Based
{% if rule_flaws %}
{% for flaw in rule_flaws %}
- **Flaw**: {{ flaw.flaw }}
  - **Location**: {{ flaw.location }}
  - **Fix**: {{ flaw.fix }}
  - **Confidence**: {{ flaw.confidence }}%
{% endfor %}
{% else %}
- None
{% endif %}

### LLM Analysis
{% if llm_flaws %}
{% for flaw in llm_flaws %}
- **Flaw**: {{ flaw.flaw }}
  - **Location**: {{ flaw.location }}
  - **Fix**: {{ flaw.fix }}
  - **Confidence**: {{ flaw.confidence }}%
{% endfor %}
{% else %}
- None
{% endif %}
    """)

    report = template.render(
        design_file=data["design_file"],
        metrics=data["metrics"],
        rule_flaws=data["rule_flaws"],
        llm_flaws=data["llm_flaws"]
    )
    with open("flaw_report.md", "w") as f:
        f.write(report)
    return report

if __name__ == "__main__":
    generate_report("flaw_report.json")