# src/parser/parser.py
from typing import List, Optional, Any
import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.token import Token, TokenType
from src.parser.ast import *


class ParseError(Exception):
    """Исключение для ошибок парсинга"""
    pass


class Parser:
    """Основной класс парсера"""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.errors = []

    # === Вспомогательные методы ===

    def peek(self) -> Token:
        """Возвращает текущий токен без продвижения"""
        if self.current >= len(self.tokens):
            return Token(TokenType.END_OF_FILE, "", -1, -1)
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Возвращает предыдущий токен"""
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        """Проверяет, достигнут ли конец токенов"""
        return self.peek().type == TokenType.END_OF_FILE

    def check(self, token_type: TokenType) -> bool:
        """Проверяет тип текущего токена"""
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        """Переходит к следующему токену и возвращает предыдущий"""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def match(self, *types: TokenType) -> bool:
        """Проверяет, совпадает ли текущий токен с одним из переданных типов"""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        """Потребляет токен ожидаемого типа или сохраняет ошибку"""
        if self.check(token_type):
            return self.advance()

        # Сохраняем ошибку
        current_token = self.peek()
        error_msg = f"Строка {current_token.line}, колонка {current_token.column}: {message}"
        self.errors.append(error_msg)

        # Возвращаем текущий токен (для продолжения работы)
        return current_token

    def synchronize(self):
        """Восстановление после ошибки"""
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            # Ключевые слова, с которых могут начинаться новые конструкции
            if self.peek().type in [
                TokenType.KW_FN, TokenType.KW_STRUCT, TokenType.KW_IF,
                TokenType.KW_WHILE, TokenType.KW_FOR, TokenType.KW_RETURN,
                TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_VOID
            ]:
                return

            self.advance()

    # === Основные методы парсинга ===

    def parse(self) -> Optional[ProgramNode]:
        """Главный метод парсинга"""
        try:
            return self.parse_program()
        except ParseError as e:
            self.errors.append(str(e))
            return None

    def parse_program(self) -> ProgramNode:
        """Program ::= { Declaration }"""
        declarations = []

        # Запоминаем позицию первого токена
        if not self.is_at_end():
            line = self.peek().line
            column = self.peek().column
        else:
            line, column = 0, 0

        # Парсим все объявления до конца файла
        while not self.is_at_end():
            decl = self.parse_declaration()
            if decl:
                declarations.append(decl)

        return ProgramNode(declarations, line, column)

    def parse_declaration(self) -> Optional[ASTNode]:
        """Declaration ::= FunctionDecl | StructDecl | VarDecl"""
        try:
            if self.match(TokenType.KW_FN):
                return self.parse_function_decl()
            elif self.match(TokenType.KW_STRUCT):
                return self.parse_struct_decl()
            elif self.check(TokenType.KW_INT) or self.check(TokenType.KW_FLOAT) or \
                    self.check(TokenType.KW_BOOL) or self.check(TokenType.KW_VOID):
                return self.parse_var_decl()
            else:
                # Если не объявление, возможно это оператор
                return self.parse_statement()
        except ParseError as e:
            self.errors.append(str(e))
            self.synchronize()
            return None

    def parse_function_decl(self) -> FunctionDeclNode:
        """FunctionDecl ::= "fn" Identifier "(" [Parameters] ")" ["->" Type] Block"""
        line = self.previous().line
        column = self.previous().column

        # Имя функции
        name_token = self.consume(TokenType.IDENTIFIER, "Ожидается имя функции")
        name = name_token.lexeme

        # Параметры
        self.consume(TokenType.LPAREN, "Ожидается '(' после имени функции")
        parameters = self.parse_parameters()
        self.consume(TokenType.RPAREN, "Ожидается ')' после параметров")

        # Возвращаемый тип (опционально)
        return_type = "void"
        if self.match(TokenType.KW_VOID):  # Просто void без стрелки
            return_type = "void"
        elif self.match(TokenType.KW_INT) or self.match(TokenType.KW_FLOAT) or \
                self.match(TokenType.KW_BOOL):
            return_type = self.previous().lexeme

        # Тело функции
        body = self.parse_block()

        return FunctionDeclNode(name, return_type, parameters, body, line, column)

    def parse_parameters(self) -> List[ParameterNode]:
        """Parameters ::= Parameter { "," Parameter }"""
        parameters = []

        # Если нет параметров
        if self.check(TokenType.RPAREN):
            return parameters

        # Первый параметр
        param = self.parse_parameter()
        parameters.append(param)

        # Остальные параметры
        while self.match(TokenType.COMMA):
            param = self.parse_parameter()
            parameters.append(param)

        return parameters

    def parse_parameter(self) -> ParameterNode:
        """Parameter ::= Type Identifier"""
        line = self.peek().line
        column = self.peek().column

        # Тип параметра
        if self.match(TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_VOID):
            param_type = self.previous().lexeme
        else:
            param_type = self.consume(TokenType.IDENTIFIER, "Ожидается тип параметра").lexeme

        # Имя параметра
        name_token = self.consume(TokenType.IDENTIFIER, "Ожидается имя параметра")
        name = name_token.lexeme

        return ParameterNode(name, param_type, line, column)

    def parse_struct_decl(self) -> StructDeclNode:
        """StructDecl ::= "struct" Identifier "{" { VarDecl } "}"""
        line = self.previous().line
        column = self.previous().column

        # Имя структуры
        name_token = self.consume(TokenType.IDENTIFIER, "Ожидается имя структуры")
        name = name_token.lexeme

        # Открывающая скобка
        self.consume(TokenType.LBRACE, "Ожидается '{' после имени структуры")

        # Поля структуры
        fields = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            field = self.parse_var_decl()
            if field:
                fields.append(field)

        # Закрывающая скобка
        self.consume(TokenType.RBRACE, "Ожидается '}' после полей структуры")

        return StructDeclNode(name, fields, line, column)

    def parse_var_decl(self) -> Optional[VarDeclNode]:
        """VarDecl ::= Type Identifier [ "=" Expression ] ";" """
        line = self.peek().line
        column = self.peek().column

        # Тип переменной
        if self.match(TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_VOID):
            var_type = self.previous().lexeme
        else:
            var_type = self.consume(TokenType.IDENTIFIER, "Ожидается тип переменной").lexeme

        # Имя переменной
        name_token = self.consume(TokenType.IDENTIFIER, "Ожидается имя переменной")
        name = name_token.lexeme

        # Начальное значение (опционально)
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.parse_expression()

        # Точка с запятой
        self.consume(TokenType.SEMICOLON, "Ожидается ';' после объявления переменной")

        return VarDeclNode(var_type, name, initializer, line, column)

    # === Парсинг выражений (с приоритетами) ===

    def parse_expression(self) -> ASTNode:
        """Expression ::= Assignment"""
        return self.parse_assignment()

    def parse_assignment(self) -> ASTNode:
        """Assignment ::= LogicalOr { ("=" | "+=" | "-=" | "*=" | "/=") Assignment }"""
        line = self.peek().line
        column = self.peek().column

        expr = self.parse_logical_or()

        # Проверяем операторы присваивания
        if self.match(TokenType.ASSIGN):
            operator = self.previous().lexeme
            value = self.parse_assignment()

            if isinstance(expr, IdentifierNode):
                return AssignmentNode(expr.name, operator, value, line, column)
            else:
                self.errors.append(
                    f"Строка {line}, колонка {column}: Левая часть присваивания должна быть идентификатором")
                return expr

        return expr

    def parse_logical_or(self) -> ASTNode:
        """LogicalOr ::= LogicalAnd { "||" LogicalAnd }"""
        line = self.peek().line
        column = self.peek().column

        expr = self.parse_logical_and()

        while self.match(TokenType.OR):
            operator = self.previous().lexeme
            right = self.parse_logical_and()
            expr = BinaryExprNode(expr, operator, right, line, column)
            line = self.peek().line
            column = self.peek().column

        return expr

    def parse_logical_and(self) -> ASTNode:
        """LogicalAnd ::= Equality { "&&" Equality }"""
        line = self.peek().line
        column = self.peek().column

        expr = self.parse_equality()

        while self.match(TokenType.AND):
            operator = self.previous().lexeme
            right = self.parse_equality()
            expr = BinaryExprNode(expr, operator, right, line, column)
            line = self.peek().line
            column = self.peek().column

        return expr

    def parse_equality(self) -> ASTNode:
        """Equality ::= Relational { ("==" | "!=") Relational }"""
        line = self.peek().line
        column = self.peek().column

        expr = self.parse_relational()

        while self.match(TokenType.EQ, TokenType.NEQ):
            operator = self.previous().lexeme
            right = self.parse_relational()
            expr = BinaryExprNode(expr, operator, right, line, column)
            line = self.peek().line
            column = self.peek().column

        return expr

    def parse_relational(self) -> ASTNode:
        """Relational ::= Additive { ("<" | "<=" | ">" | ">=") Additive }"""
        line = self.peek().line
        column = self.peek().column

        expr = self.parse_additive()

        while self.match(TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE):
            operator = self.previous().lexeme
            right = self.parse_additive()
            expr = BinaryExprNode(expr, operator, right, line, column)
            line = self.peek().line
            column = self.peek().column

        return expr

    def parse_additive(self) -> ASTNode:
        """Additive ::= Multiplicative { ("+" | "-") Multiplicative }"""
        line = self.peek().line
        column = self.peek().column

        expr = self.parse_multiplicative()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().lexeme
            right = self.parse_multiplicative()
            expr = BinaryExprNode(expr, operator, right, line, column)
            line = self.peek().line
            column = self.peek().column

        return expr

    def parse_multiplicative(self) -> ASTNode:
        """Multiplicative ::= Unary { ("*" | "/" | "%") Unary }"""
        line = self.peek().line
        column = self.peek().column

        expr = self.parse_unary()

        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.MOD):
            operator = self.previous().lexeme
            right = self.parse_unary()
            expr = BinaryExprNode(expr, operator, right, line, column)
            line = self.peek().line
            column = self.peek().column

        return expr

    def parse_unary(self) -> ASTNode:
        """Unary ::= ("-" | "!") Unary | Primary"""
        line = self.peek().line
        column = self.peek().column

        if self.match(TokenType.MINUS):
            operator = self.previous().lexeme
            expr = self.parse_unary()
            return UnaryExprNode(operator, expr, line, column)

        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        """Primary ::= Literal | Identifier | "(" Expression ")" | Call"""
        line = self.peek().line
        column = self.peek().column

        if self.match(TokenType.INT_LITERAL):
            # Числовой литерал
            value = self.previous().literal_value
            return LiteralNode(value, "int", line, column)

        if self.match(TokenType.FLOAT_LITERAL):
            value = self.previous().literal_value
            return LiteralNode(value, "float", line, column)

        if self.match(TokenType.STRING_LITERAL):
            # Строковый литерал
            value = self.previous().literal_value
            return LiteralNode(value, "string", line, column)

        if self.match(TokenType.KW_TRUE):
            return LiteralNode(True, "bool", line, column)

        if self.match(TokenType.KW_FALSE):
            return LiteralNode(False, "bool", line, column)

        if self.match(TokenType.IDENTIFIER):
            name = self.previous().lexeme

            # Проверяем, не вызов ли это функции
            if self.match(TokenType.LPAREN):
                return self.parse_call(name, line, column)

            return IdentifierNode(name, line, column)

        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Ожидается ')' после выражения")
            return expr

        # Если ничего не подошло - ошибка
        self.consume(TokenType.END_OF_FILE, f"Ожидалось выражение, получено {self.peek().lexeme}")
        return LiteralNode(0, "int", line, column)

    def parse_call(self, callee: str, line: int, column: int) -> CallNode:
        """Call ::= "(" [ Arguments ] ")" """
        arguments = []

        # Если нет аргументов
        if not self.check(TokenType.RPAREN):
            # Первый аргумент
            arguments.append(self.parse_expression())

            # Остальные аргументы
            while self.match(TokenType.COMMA):
                arguments.append(self.parse_expression())

        self.consume(TokenType.RPAREN, "Ожидается ')' после аргументов")

        return CallNode(callee, arguments, line, column)

    # === Парсинг операторов ===

    def parse_statement(self) -> Optional[ASTNode]:
        """Statement ::= Block | IfStmt | WhileStmt | ForStmt | ReturnStmt | ExprStmt | VarDecl"""

        if self.check(TokenType.LBRACE):
            return self.parse_block()
        elif self.match(TokenType.KW_IF):
            return self.parse_if_statement()
        elif self.match(TokenType.KW_WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.KW_FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.KW_RETURN):
            return self.parse_return_statement()
        elif self.check(TokenType.KW_INT) or self.check(TokenType.KW_FLOAT) or \
                self.check(TokenType.KW_BOOL) or self.check(TokenType.KW_VOID):
            return self.parse_var_decl()
        else:
            return self.parse_expression_statement()

    def parse_block(self) -> BlockNode:
        """Block ::= "{" { Statement } "}" """
        line = self.peek().line
        column = self.peek().column

        self.consume(TokenType.LBRACE, "Ожидается '{' в начале блока")

        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        self.consume(TokenType.RBRACE, "Ожидается '}' в конце блока")

        return BlockNode(statements, line, column)

    def parse_if_statement(self) -> IfStmtNode:
        """IfStmt ::= "if" "(" Expression ")" Statement [ "else" Statement ]"""
        line = self.previous().line
        column = self.previous().column

        self.consume(TokenType.LPAREN, "Ожидается '(' после 'if'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Ожидается ')' после условия")

        then_branch = self.parse_statement()

        else_branch = None
        if self.match(TokenType.KW_ELSE):
            else_branch = self.parse_statement()

        return IfStmtNode(condition, then_branch, else_branch, line, column)

    def parse_while_statement(self) -> WhileStmtNode:
        """WhileStmt ::= "while" "(" Expression ")" Statement"""
        line = self.previous().line
        column = self.previous().column

        self.consume(TokenType.LPAREN, "Ожидается '(' после 'while'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Ожидается ')' после условия")

        body = self.parse_statement()

        return WhileStmtNode(condition, body, line, column)

    def parse_for_statement(self) -> ForStmtNode:
        """ForStmt ::= "for" "(" [ ExprStmt ] ";" [ Expression ] ";" [ Expression ] ")" Statement"""
        line = self.previous().line
        column = self.previous().column

        self.consume(TokenType.LPAREN, "Ожидается '(' после 'for'")

        # Инициализация
        init = None
        if not self.check(TokenType.SEMICOLON):
            init = self.parse_expression_statement()
        else:
            self.consume(TokenType.SEMICOLON, "Ожидается ';'")

        # Условие
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Ожидается ';' после условия")

        # Обновление
        update = None
        if not self.check(TokenType.RPAREN):
            update = self.parse_expression()

        self.consume(TokenType.RPAREN, "Ожидается ')' после заголовка for")

        # Тело цикла
        body = self.parse_statement()

        return ForStmtNode(init, condition, update, body, line, column)

    def parse_return_statement(self) -> ReturnStmtNode:
        """ReturnStmt ::= "return" [ Expression ] ";" """
        line = self.previous().line
        column = self.previous().column

        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Ожидается ';' после return")

        return ReturnStmtNode(value, line, column)

    def parse_expression_statement(self) -> ExprStmtNode:
        """ExprStmt ::= Expression ";" """
        line = self.peek().line
        column = self.peek().column

        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Ожидается ';' после выражения")

        return ExprStmtNode(expr, line, column)