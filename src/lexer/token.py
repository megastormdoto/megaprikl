from enum import Enum, auto
from dataclasses import dataclass
from typing import Union, Optional


class TokenType(Enum):
    # Keywords
    KW_IF = auto()
    KW_ELSE = auto()
    KW_WHILE = auto()
    KW_FOR = auto()
    KW_INT = auto()
    KW_FLOAT = auto()
    KW_BOOL = auto()
    KW_RETURN = auto()
    KW_TRUE = auto()
    KW_FALSE = auto()
    KW_VOID = auto()
    KW_STRUCT = auto()
    KW_FN = auto()

    # Literals
    IDENTIFIER = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOL_LITERAL = auto()

    # Operators
    PLUS = auto()  # +
    MINUS = auto()  # -
    STAR = auto()  # *
    SLASH = auto()  # /
    MOD = auto()  # %
    ASSIGN = auto()  # =
    EQ = auto()  # ==
    NEQ = auto()  # !=
    LT = auto()  # <
    LTE = auto()  # <=
    GT = auto()  # >
    GTE = auto()  # >=
    AND = auto()  # &&
    OR = auto()  # ||

    # Delimiters
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    SEMICOLON = auto()  # ;
    COMMA = auto()  # ,

    # Special
    END_OF_FILE = auto()
    UNKNOWN = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
    literal_value: Optional[Union[int, float, str, bool]] = None

    def __str__(self):
        if self.literal_value is not None:
            return f"{self.line}:{self.column} {self.type.name} \"{self.lexeme}\" {self.literal_value}"
        return f"{self.line}:{self.column} {self.type.name} \"{self.lexeme}\""