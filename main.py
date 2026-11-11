import argparse
import sys
from pathlib import Path
from src.parser import LogParser
from src.analyzer import LogAnalyzer
from src.reporter import IncidentReporter

def main():
    parser = argparse.ArgumentParser(
        description="MedLog-Sentinel: Automated Log Analyzer & RCA Generator for Healthcare Systems."
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Path to the application log file to analyze."
    )
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=1500,
        help="Latency threshold in milliseconds to flag SLA breaches (default: 1500ms)."
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format for the diagnostic report (default: markdown)."
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional file path to save the generated report."
    )

    args = parser.parse_args()
    log_path = Path(args.file)

    if not log_path.exists():
        print(f"Error: Log file not found at '{log_path}'", file=sys.stderr)
        sys.exit(1)

    entries = LogParser.parse_file(str(log_path))
    analyzer = LogAnalyzer(entries, latency_threshold_ms=args.threshold)
    diagnostics = analyzer.run_diagnostics()

    if args.format == "json":
        report_content = IncidentReporter.to_json(diagnostics)
    else:
        report_content = IncidentReporter.to_markdown(diagnostics)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(report_content, encoding="utf-8")
        print(f"[+] Diagnostic report successfully saved to {out_path}")
    else:
        print(report_content)

if __name__ == "__main__":
    main()