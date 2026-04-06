"""Error handling for semantic analysis."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SemanticError:
    """ERR-2: Структурированная ошибка с позицией в коде."""
    line: int
    column: int
    message: str
    category: str  # Тип ошибки (undeclared, type_mismatch, и т.д.)
    details: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None

    def __str__(self) -> str:
        """Форматирует ошибку для вывода пользователю."""
        result = f"semantic error: {self.message}\n"
        result += f"  --> line {self.line}, column {self.column}\n"
        if self.expected or self.actual:
            result += f"  = expected: {self.expected}\n"
            result += f"  = found: {self.actual}\n"
        if self.details:
            result += f"  = note: {self.details}\n"
        return result


class ErrorCollector:
    """ERR-3: Собирает ошибки и продолжает анализ."""

    def __init__(self):
        self.errors: List[SemanticError] = []

    def add(self, line: int, column: int, message: str, category: str,
            details: Optional[str] = None) -> None:
        """Добавляет новую ошибку."""
        error = SemanticError(
            line=line,
            column=column,
            message=message,
            category=category,
            details=details
        )
        self.errors.append(error)

    def add_type_mismatch(self, line: int, column: int, message: str,
                          expected: str, actual: str) -> None:
        """Удобный метод для ошибок несоответствия типов."""
        error = SemanticError(
            line=line,
            column=column,
            message=message,
            category="type_mismatch",
            expected=expected,
            actual=actual
        )
        self.errors.append(error)

    def add_undeclared(self, line: int, column: int, name: str) -> None:
        """Удобный метод для ошибок необъявленных переменных."""
        error = SemanticError(
            line=line,
            column=column,
            message=f"undeclared identifier '{name}'",
            category="undeclared",
            details=f"variable '{name}' was not declared in this scope"
        )
        self.errors.append(error)

    def has_errors(self) -> bool:
        """Проверяет, есть ли ошибки."""
        return len(self.errors) > 0

    def get_count(self) -> int:
        """Возвращает количество ошибок."""
        return len(self.errors)

    def clear(self) -> None:
        """Очищает список ошибок."""
        self.errors.clear()