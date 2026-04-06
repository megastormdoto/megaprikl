"""Type system for semantic analysis."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from enum import Enum


class BaseType(Enum):
    """Base types for the language."""
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    VOID = "void"
    STRING = "string"


@dataclass
class Type:
    """Type representation."""
    kind: Union[BaseType, str]
    is_struct: bool = False
    fields: Optional[Dict[str, 'Type']] = None
    is_array: bool = False
    array_size: Optional[int] = None
    element_type: Optional['Type'] = None

    def __str__(self) -> str:
        if self.is_struct:
            return f"struct {self.kind}"
        elif self.is_array:
            return f"array[{self.array_size}] of {self.element_type}"
        return self.kind.value if isinstance(self.kind, BaseType) else str(self.kind)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Type):
            return False

        if not self.is_struct and not other.is_struct:
            return self.kind == other.kind

        if self.is_struct and other.is_struct:
            return self.kind == other.kind

        return False

    def size_bytes(self) -> int:
        """Return size in bytes for memory layout."""
        if self.kind == BaseType.INT:
            return 4
        elif self.kind == BaseType.FLOAT:
            return 4
        elif self.kind == BaseType.BOOL:
            return 1
        elif self.kind == BaseType.VOID:
            return 0
        elif self.is_struct and self.fields:
            total = 0
            for field_type in self.fields.values():
                total += field_type.size_bytes()
            return total
        elif self.is_array:
            return self.array_size * self.element_type.size_bytes()
        return 0


class TypeSystem:
    """Type operations and compatibility checking."""

    @staticmethod
    def is_compatible(target: Type, source: Type) -> bool:
        """Check if source type can be assigned to target type.
        Allows implicit widening: int -> float.
        """
        # Exact match
        if target == source:
            return True

        # Implicit widening: int to float
        if (target.kind == BaseType.FLOAT and source.kind == BaseType.INT):
            return True

        # Struct types: must be same struct name
        if target.is_struct and source.is_struct:
            return target.kind == source.kind

        return False

    @staticmethod
    def can_convert(source: Type, target: Type) -> bool:
        """Check if source can be converted to target."""
        # Exact match
        if source == target:
            return True

        # int -> float (widening)
        if source.kind == BaseType.INT and target.kind == BaseType.FLOAT:
            return True

        # Any type can be used as bool (for conditions)
        if target.kind == BaseType.BOOL:
            return True

        return False

    @staticmethod
    def binary_operator_result_type(op: str, left: Type, right: Type) -> Optional[Type]:
        """Determine result type of binary operation."""
        # Arithmetic operators: + - * / %
        if op in ['+', '-', '*', '/', '%']:
            # int + int = int
            if left.kind == BaseType.INT and right.kind == BaseType.INT:
                return Type(BaseType.INT)

            # float + anything = float (if both are numeric)
            if (left.kind in [BaseType.INT, BaseType.FLOAT] and
                    right.kind in [BaseType.INT, BaseType.FLOAT]):
                return Type(BaseType.FLOAT)

            return None

        # Comparison operators: == != < <= > >=
        elif op in ['==', '!=', '<', '<=', '>', '>=']:
            if TypeSystem.is_compatible(left, right) or TypeSystem.is_compatible(right, left):
                return Type(BaseType.BOOL)
            return None

        # Logical operators: && ||
        elif op in ['&&', '||']:
            if left.kind == BaseType.BOOL and right.kind == BaseType.BOOL:
                return Type(BaseType.BOOL)
            return None

        return None