from collections import Counter
from typing import List, Dict, Any
from src.parser import LogEntry

class LogAnalyzer:
    def __init__(self, entries: List[LogEntry], latency_threshold_ms: int = 1500):
        self.entries = entries
        self.latency_threshold_ms = latency_threshold_ms

    def run_diagnostics(self) -> Dict[str, Any]:
        total_logs = len(self.entries)
        if total_logs == 0:
            return {"status": "empty", "total_logs": 0}

        level_counts = Counter(e.level for e in self.entries)
        service_errors = Counter(
            e.service for e in self.entries if e.level in ("ERROR", "CRITICAL")
        )
        
        high_latency_events = [
            e for e in self.entries if e.latency_ms >= self.latency_threshold_ms
        ]
        
        avg_latency = sum(e.latency_ms for e in self.entries) / total_logs
        max_latency_entry = max(self.entries, key=lambda e: e.latency_ms)

        return {
            "total_logs": total_logs,
            "time_range": {
                "start": self.entries[0].timestamp.isoformat(),
                "end": self.entries[-1].timestamp.isoformat(),
            },
            "level_distribution": dict(level_counts),
            "failing_services": dict(service_errors.most_common()),
            "latency_metrics": {
                "average_ms": round(avg_latency, 2),
                "max_ms": max_latency_entry.latency_ms,
                "max_service": max_latency_entry.service,
                "threshold_breaches": len(high_latency_events),
            },
            "critical_events": [
                {
                    "time": e.timestamp.strftime("%H:%M:%S"),
                    "level": e.level,
                    "service": e.service,
                    "message": e.message,
                    "latency_ms": e.latency_ms,
                }
                for e in self.entries
                if e.level in ("ERROR", "CRITICAL") or e.latency_ms >= self.latency_threshold_ms
            ],
        }