# MedLog-Sentinel

**MedLog-Sentinel** is a lightweight command-line diagnostic utility designed for Application Support Engineers and Site Reliability teams managing Hospital Information Management Systems (HIMS) and Laboratory Information Systems (LIS). 

It parses structured server logs, identifies subsystem bottlenecks, flags SLA latency breaches, and automatically generates structured Root Cause Analysis (RCA) incident summaries in Markdown or JSON format.

## Key Features
- **Zero External Dependencies:** Built entirely with Python's standard library (`re`, `dataclasses`, `argparse`, `collections`) for immediate deployment in restricted clinical server environments.
- **Latency & SLA Auditing:** Configurable millisecond thresholds to detect database connection pool exhaustion and external gateway timeouts.
- **Subsystem Hotspot Detection:** Aggregates `ERROR` and `CRITICAL` events by service module (e.g., `EMR-API`, `LAB-LIS`, `DB-POOL`).
- **Automated RCA Reporting:** Exports clean Markdown tables and diagnostic summaries ready to be pasted into incident tickets.

## Project Structure
```text
medlog-sentinel/
├── src/
│   ├── parser.py      # Regex-based log line tokenizer and data models
│   ├── analyzer.py    # Latency aggregation and anomaly detection engine
│   └── reporter.py    # Markdown and JSON report formatters
├── sample_logs/
│   └── simrs_server.log
└── main.py            # CLI entry point