from dataclasses import dataclass


@dataclass
class LogEntry:
    line_number: int
    level: str
    message: str
    raw_line: str

    def to_dict(self) -> dict:
        return {
            "line": self.line_number,
            "level": self.level,
            "text": self.message,
        }