"""Symbol table implementation for semantic analysis."""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# Импорт типов из type_system
from src.semantic.type_system import Type, BaseType


class SymbolKind(Enum):
    """SYM-3: Types of symbols."""
    VARIABLE = "variable"
    FUNCTION = "function"
    PARAMETER = "parameter"
    STRUCT = "struct"
    FIELD = "field"


@dataclass
class Symbol:
    """SYM-3: Symbol information for each identifier."""
    name: str
    kind: SymbolKind
    type: Type
    line: int
    column: int

    # Optional fields for functions
    parameters: Optional[List[Type]] = None
    return_type: Optional[Type] = None

    # Optional fields for structs
    fields: Optional[Dict[str, Type]] = None

    # For future code generation
    stack_offset: Optional[int] = None
    size_bytes: Optional[int] = None


class SymbolTable:
    """SYM-1: Hierarchical symbol table with scope management."""

    def __init__(self):
        """SYM-1: Constructor creates global scope."""
        self.scopes: List[Dict[str, Symbol]] = [{}]
        self.current_scope_index = 0

    def enter_scope(self) -> None:
        """SYM-1: Push new nested scope."""
        self.scopes.append({})
        self.current_scope_index += 1

    def exit_scope(self) -> None:
        """SYM-1: Pop current scope."""
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope_index -= 1

    def insert(self, name: str, symbol: Symbol) -> bool:
        """SYM-1: Insert symbol into current scope.
        Returns True if successful, False if duplicate.
        """
        current_scope = self.scopes[-1]
        if name in current_scope:
            return False
        current_scope[name] = symbol
        return True

    def lookup(self, name: str) -> Optional[Symbol]:
        """SYM-1: Search from current to outer scopes."""
        for i in range(len(self.scopes) - 1, -1, -1):
            if name in self.scopes[i]:
                return self.scopes[i][name]
        return None

    def lookup_local(self, name: str) -> Optional[Symbol]:
        """SYM-1: Search only current scope."""
        return self.scopes[-1].get(name)

    def get_current_scope_depth(self) -> int:
        """SYM-2: Return current nesting depth."""
        return len(self.scopes) - 1

    def dump(self) -> str:
        """Produce readable symbol table dump."""
        result = []
        for i, scope in enumerate(self.scopes):
            scope_name = "Global (scope 0)" if i == 0 else f"Scope {i}"
            result.append(f"\n{scope_name}:")
            if not scope:
                result.append("  (empty)")
            for name, sym in scope.items():
                type_str = str(sym.type) if sym.type else "unknown"
                result.append(f"  - {name}: {sym.kind.value} -> {type_str} (line {sym.line})")
                if sym.kind == SymbolKind.FUNCTION and sym.parameters:
                    params = ", ".join(str(p) for p in sym.parameters)
                    result.append(f"      parameters: ({params})")
                    result.append(f"      returns: {sym.return_type}")
                elif sym.kind == SymbolKind.STRUCT and sym.fields:
                    for fname, ftype in sym.fields.items():
                        result.append(f"      field {fname}: {ftype}")
        return "\n".join(result)