import re
from typing import Optional, List, Tuple
from .token import Token, TokenType
from .errors import ErrorHandler


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.errors = ErrorHandler()

        # Keywords mapping
        self.keywords = {
            'if': TokenType.KW_IF,
            'else': TokenType.KW_ELSE,
            'while': TokenType.KW_WHILE,
            'for': TokenType.KW_FOR,
            'int': TokenType.KW_INT,
            'float': TokenType.KW_FLOAT,
            'bool': TokenType.KW_BOOL,
            'return': TokenType.KW_RETURN,
            'true': TokenType.KW_TRUE,
            'false': TokenType.KW_FALSE,
            'void': TokenType.KW_VOID,
            'struct': TokenType.KW_STRUCT,
            'fn': TokenType.KW_FN
        }

    def scan_tokens(self) -> List[Token]:
        """Scan all tokens from the source"""
        while not self.is_at_end():
            self.start = self.current
            self._scan_token()

        # Вычисляем правильные строку и колонку для END_OF_FILE
        # Проверяем, заканчивается ли файл переносом строки
        if self.source.endswith('\n'):
            line = self.source.count('\n')  # Последняя строка уже учтена
            # Находим последний перенос строки (не включая последний символ)
            last_newline = self.source.rfind('\n', 0, len(self.source) - 1)
            if last_newline == -1:
                column = len(self.source)
            else:
                column = len(self.source) - last_newline
        else:
            last_newline = self.source.rfind('\n')
            if last_newline == -1:
                column = len(self.source) + 1
                line = 1
            else:
                column = len(self.source) - last_newline
                line = self.source.count('\n') + 1

        self.tokens.append(Token(TokenType.END_OF_FILE, "", line, column))
        return self.tokens

    def _scan_token(self):
        """Scan a single token"""
        c = self._advance()

        if c == '\n':
            self.line += 1
            self.column = 1
        elif c in ' \t\r':
            pass  # Ignore whitespace
        elif c == '/':
            if self._peek() == '/':
                self._single_line_comment()
            elif self._peek() == '*':
                self._multi_line_comment()
            else:
                self._add_token(TokenType.SLASH)
        elif c == '+':
            self._add_token(TokenType.PLUS)
        elif c == '-':
            self._add_token(TokenType.MINUS)
        elif c == '*':
            self._add_token(TokenType.STAR)
        elif c == '%':
            self._add_token(TokenType.MOD)
        elif c == '=':
            if self._match('='):
                self._add_token(TokenType.EQ)
            else:
                self._add_token(TokenType.ASSIGN)
        elif c == '!':
            if self._match('='):
                self._add_token(TokenType.NEQ)
            else:
                self._error("Unexpected character '!'")
        elif c == '<':
            if self._match('='):
                self._add_token(TokenType.LTE)
            else:
                self._add_token(TokenType.LT)
        elif c == '>':
            if self._match('='):
                self._add_token(TokenType.GTE)
            else:
                self._add_token(TokenType.GT)
        elif c == '&':
            if self._match('&'):
                self._add_token(TokenType.AND)
            else:
                self._error("Expected '&&'")
        elif c == '|':
            if self._match('|'):
                self._add_token(TokenType.OR)
            else:
                self._error("Expected '||'")
        elif c == '(':
            self._add_token(TokenType.LPAREN)
        elif c == ')':
            self._add_token(TokenType.RPAREN)
        elif c == '{':
            self._add_token(TokenType.LBRACE)
        elif c == '}':
            self._add_token(TokenType.RBRACE)
        elif c == '[':
            self._add_token(TokenType.LBRACKET)
        elif c == ']':
            self._add_token(TokenType.RBRACKET)
        elif c == ';':
            self._add_token(TokenType.SEMICOLON)
        elif c == ',':
            self._add_token(TokenType.COMMA)
        elif c == '"':
            self._string()
        elif c.isdigit() or (c == '.' and self._peek().isdigit()):
            self._number(c)
        elif c.isalpha() or c == '_':
            self._identifier()
        else:
            self._error(f"Unexpected character '{c}'")

    def _identifier(self):
        """Handle identifiers and keywords"""
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)

        if token_type == TokenType.KW_TRUE:
            self._add_token(token_type, True)
        elif token_type == TokenType.KW_FALSE:
            self._add_token(token_type, False)
        else:
            self._add_token(token_type)

    def _number(self, first_char: str):
        """Handle numeric literals"""
        is_float = False

        if first_char == '.':
            is_float = True
            while self._peek().isdigit():
                self._advance()
        else:
            while self._peek().isdigit():
                self._advance()

            if self._peek() == '.' and self._peek_next().isdigit():
                is_float = True
                self._advance()  # Consume the '.'
                while self._peek().isdigit():
                    self._advance()

        number_str = self.source[self.start:self.current]

        if is_float:
            try:
                value = float(number_str)
                self._add_token(TokenType.FLOAT_LITERAL, value)
            except ValueError:
                self._error(f"Invalid float literal: {number_str}")
        else:
            try:
                value = int(number_str)
                if value < -2 ** 31 or value > 2 ** 31 - 1:
                    self._error(f"Integer literal out of range: {number_str}")
                self._add_token(TokenType.INT_LITERAL, value)
            except ValueError:
                self._error(f"Invalid integer literal: {number_str}")

    def _string(self):
        """Handle string literals"""
        while self._peek() != '"' and not self.is_at_end():
            if self._peek() == '\n':
                self.line += 1
                self.column = 1
            self._advance()

        if self.is_at_end():
            self._error("Unterminated string")
            return

        self._advance()  # Consume closing "
        value = self.source[self.start + 1:self.current - 1]
        self._add_token(TokenType.STRING_LITERAL, value)

    def _single_line_comment(self):
        """Handle single-line comments"""
        while self._peek() != '\n' and not self.is_at_end():
            self._advance()
        # Don't add token, just consume

    def _multi_line_comment(self):
        """Handle multi-line comments"""
        nesting_level = 1

        while nesting_level > 0 and not self.is_at_end():
            if self._peek() == '*' and self._peek_next() == '/':
                self._advance()  # Consume '*'
                self._advance()  # Consume '/'
                nesting_level -= 1
            elif self._peek() == '/' and self._peek_next() == '*':
                self._advance()  # Consume '/'
                self._advance()  # Consume '*'
                nesting_level += 1
            else:
                if self._peek() == '\n':
                    self.line += 1
                    self.column = 1
                self._advance()

        if nesting_level > 0:
            self._error("Unterminated multi-line comment")

    def _add_token(self, token_type: TokenType, literal_value=None):
        """Add a token to the list"""
        text = self.source[self.start:self.current]

        # Вычисляем номер колонки (начинается с 1)
        last_newline = self.source.rfind('\n', 0, self.start)
        if last_newline == -1:
            column = self.start + 1  # +1 потому что колонки с 1
        else:
            column = self.start - last_newline

        self.tokens.append(Token(
            type=token_type,
            lexeme=text,
            line=self.line,
            column=column,
            literal_value=literal_value
        ))

    def _advance(self) -> str:
        """Advance to next character and return current"""
        self.current += 1
        self.column += 1
        return self.source[self.current - 1]

    def _peek(self) -> str:
        """Look at current character without advancing"""
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def _peek_next(self) -> str:
        """Look at next character without advancing"""
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def _match(self, expected: str) -> bool:
        """Match expected character and advance if matches"""
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        self.column += 1
        return True

    def _error(self, message: str):
        """Report an error"""
        # Get the current line for context
        line_start = self.source.rfind('\n', 0, self.start) + 1
        line_end = self.source.find('\n', self.start)
        if line_end == -1:
            line_end = len(self.source)
        source_line = self.source[line_start:line_end]

        self.errors.report_error(message, self.line, self.column, source_line)
        self._add_token(TokenType.UNKNOWN)

    def is_at_end(self) -> bool:
        """Check if we've reached the end of source"""
        return self.current >= len(self.source)

    def get_tokens(self) -> List[Token]:
        """Get all scanned tokens"""
        return self.tokens

    def has_errors(self) -> bool:
        """Check if any errors occurred"""
        return self.errors.has_errors()

    def print_errors(self):
        """Print all errors"""
        for error in self.errors.errors:
            print(error)