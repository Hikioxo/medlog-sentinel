import json
from typing import Dict, Any

class IncidentReporter:
    @staticmethod
    def to_markdown(diagnostics: Dict[str, Any]) -> str:
        if diagnostics.get("total_logs", 0) == 0:
            return "# Incident Report\nNo valid log entries found to analyze."

        metrics = diagnostics["latency_metrics"]
        levels = diagnostics["level_distribution"]
        failing = diagnostics["failing_services"]

        lines = [
            "# Automated System Diagnostic & RCA Summary",
            f"**Analysis Window:** `{diagnostics['time_range']['start']}` to `{diagnostics['time_range']['end']}`",
            f"**Total Events Processed:** {diagnostics['total_logs']}",
            "",
            "## 1. Severity Breakdown",
        ]

        for level, count in levels.items():
            lines.append(f"- **{level}:** {count} events")

        lines.extend([
            "",
            "## 2. Latency & Performance Metrics",
            f"- **Average Response Time:** {metrics['average_ms']} ms",
            f"- **Peak Latency:** {metrics['max_ms']} ms (Module: `{metrics['max_service']}`)",
            f"- **SLA Threshold Breaches:** {metrics['threshold_breaches']} events",
            "",
            "## 3. Impacted Subsystems (Error Hotspots)",
        ])

        if failing:
            for srv, err_count in failing.items():
                lines.append(f"- `{srv}`: {err_count} failure(s)")
        else:
            lines.append("- No critical subsystem failures detected.")

        lines.extend([
            "",
            "## 4. Anomaly Timeline (Errors & High Latency)",
            "| Time | Level | Module | Latency | Event Details |",
            "|------|-------|--------|---------|---------------|",
        ])

        for ev in diagnostics["critical_events"]:
            lines.append(
                f"| {ev['time']} | **{ev['level']}** | `{ev['service']}` | {ev['latency_ms']}ms | {ev['message']} |"
            )

        return "\n".join(lines)

    @staticmethod
    def to_json(diagnostics: Dict[str, Any]) -> str:
        return json.dumps(diagnostics, indent=2)