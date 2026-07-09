import re
from collections import Counter

from models.log_entry import LogEntry

DEFAULT_PATTERNS = {
    "Error": r"\berror\b",
    "Denied": r"\bdenied\b",
    "Failed": r"\bfailed\b|authentication failure",
    "Warning": r"\bwarning\b",
}


class LogAnalyzer:
    def __init__(self):
        self.lines = []
        self.entries = []
        self.stats = {}
        self.source_file = None

    def load_file(self, path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            self.lines = f.readlines()
        self.source_file = path

        if not self.lines:
            raise ValueError("Файл порожній — немає рядків для аналізу.")

    def analyze(self, patterns=None):
        if not self.lines:
            raise ValueError("Спочатку викличте load_file().")

        patterns = patterns or DEFAULT_PATTERNS
        compiled = {name: re.compile(pat, re.IGNORECASE) for name, pat in patterns.items()}

        self.entries = []
        for idx, line in enumerate(self.lines, start=1):
            for level, regex in compiled.items():
                if regex.search(line):
                    self.entries.append(
                        LogEntry(
                            line_number=idx,
                            level=level,
                            message=line.strip(),
                            raw_line=line,
                        )
                    )
                    break

        self.stats = dict(Counter(e.level for e in self.entries))

    def get_statistics(self):
        return self.stats

    def get_entries(self):
        return self.entries

    def to_report_dict(self):
        return {
            "source_file": self.source_file,
            "statistics": self.stats,
            "entries": [e.to_dict() for e in self.entries],
        }