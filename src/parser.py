import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    service: str
    message: str
    latency_ms: int
    raw_line: str

class LogParser:
    # Pola: 2026-11-10 08:01:12 [INFO] [AUTH-SVC] Message [120ms]
    LOG_PATTERN = re.compile(
        r"^(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s"
        r"\[(?P<level>[A-Z]+)\]\s"
        r"\[(?P<service>[A-Z0-9-]+)\]\s"
        r"(?P<message>.*?)\s"
        r"\[(?P<latency>\d+)ms\]$"
    )

    @classmethod
    def parse_line(cls, line: str) -> Optional[LogEntry]:
        match = cls.LOG_PATTERN.match(line.strip())
        if not match:
            return None
        
        data = match.groupdict()
        return LogEntry(
            timestamp=datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S"),
            level=data["level"],
            service=data["service"],
            message=data["message"],
            latency_ms=int(data["latency"]),
            raw_line=line.strip()
        )

    @classmethod
    def parse_file(cls, filepath: str) -> List[LogEntry]:
        entries = []
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    entry = cls.parse_line(line)
                    if entry:
                        entries.append(entry)
        return entries