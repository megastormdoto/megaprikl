from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LexicalError:
    message: str
    line: int
    column: int
    source_line: str

    def __str__(self):
        return f"Lexical error at {self.line}:{self.column}: {self.message}\n{self.source_line}"


class ErrorHandler:
    def __init__(self):
        self.errors: List[LexicalError] = []

    def report_error(self, message: str, line: int, column: int, source_line: str = ""):
        error = LexicalError(message, line, column, source_line)
        self.errors.append(error)
        print(f"Error: {error}")  # Immediate feedback

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def clear(self):
        self.errors.clear()