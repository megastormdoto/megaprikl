from typing import List, Optional, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.token import Token, TokenType
from src.parser.ast import *


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.errors = []

    def peek(self) -> Token:
        if self.current >= len(self.tokens):
            return Token(TokenType.END_OF_FILE, "", -1, -1)
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.END_OF_FILE

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        current_token = self.peek()
        self.errors.append(f"Строка {current_token.line}, колонка {current_token.column}: {message}")
        return current_token

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in [TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL,
                                    TokenType.KW_VOID, TokenType.KW_STRUCT, TokenType.KW_IF,
                                    TokenType.KW_WHILE, TokenType.KW_FOR, TokenType.KW_RETURN,
                                    TokenType.KW_FN]:
                return
            self.advance()

    def parse(self) -> Optional[ProgramNode]:
        try:
            return self.parse_program()
        except ParseError as e:
            self.errors.append(str(e))
            return None

    def parse_program(self) -> ProgramNode:
        declarations = []
        line, column = 0, 0
        if not self.is_at_end():
            line = self.peek().line
            column = self.peek().column

        while not self.is_at_end():
            decl = self.parse_declaration()
            if decl:
                declarations.append(decl)

        return ProgramNode(declarations, line, column)

    def parse_declaration(self) -> Optional[ASTNode]:
        try:
            # extern declaration
            if self.check(TokenType.IDENTIFIER) and self.peek().lexeme == "extern":
                self.advance()
                return self.parse_extern_decl()

            # function declaration
            if self._is_function_declaration():
                return self.parse_function_decl()

            if self.check(TokenType.KW_STRUCT):
                return self.parse_struct_decl()

            # variable declaration
            if self.check(TokenType.KW_INT) or self.check(TokenType.KW_FLOAT) or \
                    self.check(TokenType.KW_BOOL) or self.check(TokenType.KW_VOID) or \
                    self.check(TokenType.IDENTIFIER):
                return self.parse_var_decl()

            return self.parse_statement()

        except ParseError as e:
            self.errors.append(str(e))
            self.synchronize()
            return None

    def _is_function_declaration(self) -> bool:
        """Check if current position is a function declaration."""
        pos = self.current

        # Support 'fn' keyword
        if self.check(TokenType.KW_FN):
            self.current = pos
            return True

        # Standard C syntax: type identifier '('
        if not (self.check(TokenType.KW_INT) or self.check(TokenType.KW_FLOAT) or
                self.check(TokenType.KW_BOOL) or self.check(TokenType.KW_VOID) or
                self.check(TokenType.IDENTIFIER)):
            return False
        self.advance()

        if not self.check(TokenType.IDENTIFIER):
            self.current = pos
            return False
        self.advance()

        is_func = self.check(TokenType.LPAREN)
        self.current = pos
        return is_func

    def parse_extern_decl(self) -> FunctionDeclNode:
        line = self.previous().line
        column = self.previous().column

        if self.match(TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_VOID):
            return_type = self.previous().lexeme
        else:
            return_type = self.consume(TokenType.IDENTIFIER, "Expected return type").lexeme

        name_token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.lexeme

        self.consume(TokenType.LPAREN, "Expected '('")
        parameters = self.parse_parameters()
        self.consume(TokenType.RPAREN, "Expected ')'")
        self.consume(TokenType.SEMICOLON, "Expected ';'")

        return FunctionDeclNode(name, return_type, parameters, None, line, column, is_extern=True)

    def parse_function_decl(self) -> FunctionDeclNode:
        line = self.peek().line
        column = self.peek().column

        # Support 'fn' keyword syntax
        if self.match(TokenType.KW_FN):
            name_token = self.consume(TokenType.IDENTIFIER, "Expected function name")
            name = name_token.lexeme
            self.consume(TokenType.LPAREN, "Expected '(' after function name")
            parameters = self.parse_parameters()
            self.consume(TokenType.RPAREN, "Expected ')' after parameters")

            return_type = "void"
            if self.match(TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_VOID):
                return_type = self.previous().lexeme

            body = self.parse_block()
            return FunctionDeclNode(name, return_type, parameters, body, line, column, is_extern=False)

        # Standard C syntax
        if self.match(TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_VOID):
            return_type = self.previous().lexeme
        else:
            return_type = self.consume(TokenType.IDENTIFIER, "Expected return type").lexeme

        name_token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.lexeme

        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        parameters = self.parse_parameters()
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")

        body = self.parse_block()
        return FunctionDeclNode(name, return_type, parameters, body, line, column, is_extern=False)

    def parse_parameters(self) -> List[ParameterNode]:
        parameters = []
        if self.check(TokenType.RPAREN):
            return parameters

        param = self.parse_parameter()
        parameters.append(param)

        while self.match(TokenType.COMMA):
            param = self.parse_parameter()
            parameters.append(param)

        return parameters

    def parse_parameter(self) -> ParameterNode:
        line = self.peek().line
        column = self.peek().column

        if self.match(TokenType.ELLIPSIS):
            return ParameterNode("...", "variadic", line, column)

        # Support both C-style (int a) and Go-style (a int)

        # Try C-style first: type then name
        if self.match(TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_VOID):
            param_type = self.previous().lexeme
            name_token = self.consume(TokenType.IDENTIFIER, "Expected parameter name")
            name = name_token.lexeme
            return ParameterNode(name=name, param_type=param_type, line=line, column=column)

        # Go-style: name then type
        name_token = self.consume(TokenType.IDENTIFIER, "Expected parameter name")
        name = name_token.lexeme

        if self.match(TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_VOID):
            param_type = self.previous().lexeme
        else:
            param_type = self.consume(TokenType.IDENTIFIER, "Expected parameter type").lexeme

        return ParameterNode(name=name, param_type=param_type, line=line, column=column)

    def parse_struct_decl(self) -> StructDeclNode:
        line = self.previous().line
        column = self.previous().column

        name_token = self.consume(TokenType.IDENTIFIER, "Expected struct name")
        name = name_token.lexeme

        self.consume(TokenType.LBRACE, "Expected '{' after struct name")
        fields = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            field = self.parse_var_decl()
            if field:
                fields.append(field)
        self.consume(TokenType.RBRACE, "Expected '}' after struct fields")
        return StructDeclNode(name, fields, line, column)

    def parse_var_decl(self) -> Optional[ASTNode]:
        line = self.peek().line
        column = self.peek().column

        if self.match(TokenType.KW_INT, TokenType.KW_FLOAT, TokenType.KW_BOOL, TokenType.KW_VOID):
            var_type = self.previous().lexeme
        else:
            var_type = self.consume(TokenType.IDENTIFIER, "Expected variable type").lexeme

        name_token = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.lexeme

        # array
        if self.match(TokenType.LBRACKET):
            size_expr = self.parse_expression()
            self.consume(TokenType.RBRACKET, "Expected ']'")
            initializer = None
            if self.match(TokenType.ASSIGN):
                if self.match(TokenType.LBRACE):
                    values = []
                    if not self.check(TokenType.RBRACE):
                        values.append(self.parse_expression())
                        while self.match(TokenType.COMMA):
                            values.append(self.parse_expression())
                    self.consume(TokenType.RBRACE, "Expected '}'")
                    initializer = values
                else:
                    initializer = self.parse_expression()
            self.consume(TokenType.SEMICOLON, "Expected ';' after array declaration")
            return ArrayDeclNode(var_type, name, size_expr, line, column, initializer)

        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return VarDeclNode(var_type, name, line, column, initializer)

    def parse_expression(self) -> ASTNode:
        return self.parse_assignment()

    def parse_assignment(self) -> ASTNode:
        line = self.peek().line
        column = self.peek().column
        expr = self.parse_logical_or()

        if self.match(TokenType.ASSIGN):
            operator = self.previous().lexeme
            value = self.parse_assignment()
            if isinstance(expr, IdentifierNode):
                return AssignmentNode(expr.name, operator, value, line, column)
            else:
                self.errors.append(f"Line {line}, column {column}: Left side must be identifier")
                return expr
        return expr

    def parse_logical_or(self) -> ASTNode:
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
        line = self.peek().line
        column = self.peek().column

        if self.match(TokenType.MINUS):
            operator = self.previous().lexeme
            expr = self.parse_unary()
            return UnaryExprNode(operator, expr, line, column)

        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        line = self.peek().line
        column = self.peek().column

        if self.match(TokenType.INT_LITERAL):
            return LiteralNode(self.previous().literal_value, "int", line, column)
        if self.match(TokenType.FLOAT_LITERAL):
            return LiteralNode(self.previous().literal_value, "float", line, column)
        if self.match(TokenType.STRING_LITERAL):
            return LiteralNode(self.previous().literal_value, "string", line, column)
        if self.match(TokenType.KW_TRUE):
            return LiteralNode(True, "bool", line, column)
        if self.match(TokenType.KW_FALSE):
            return LiteralNode(False, "bool", line, column)

        if self.match(TokenType.IDENTIFIER):
            name = self.previous().lexeme
            if self.match(TokenType.LPAREN):
                return self.parse_call(name, line, column)
            if self.match(TokenType.LBRACKET):
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET, "Expected ']'")
                return ArrayAccessNode(name, index, line, column)
            return IdentifierNode(name, line, column)

        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        return LiteralNode(0, "int", line, column)

    def parse_call(self, callee: str, line: int, column: int) -> CallNode:
        arguments = []
        if not self.check(TokenType.RPAREN):
            arguments.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.parse_expression())
        self.consume(TokenType.RPAREN, "Expected ')' after arguments")
        return CallNode(callee, arguments, line, column)

    def parse_statement(self) -> Optional[ASTNode]:
        if self.check(TokenType.LBRACE):
            return self.parse_block()
        if self.match(TokenType.KW_IF):
            return self.parse_if_statement()
        if self.match(TokenType.KW_WHILE):
            return self.parse_while_statement()
        if self.match(TokenType.KW_FOR):
            return self.parse_for_statement()
        if self.match(TokenType.KW_RETURN):
            return self.parse_return_statement()
        if self.check(TokenType.KW_INT) or self.check(TokenType.KW_FLOAT) or \
                self.check(TokenType.KW_BOOL) or self.check(TokenType.KW_VOID):
            return self.parse_var_decl()
        return self.parse_expression_statement()

    def parse_block(self) -> BlockNode:
        line = self.peek().line
        column = self.peek().column
        self.consume(TokenType.LBRACE, "Expected '{'")
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.consume(TokenType.RBRACE, "Expected '}'")
        return BlockNode(statements, line, column)

    def parse_if_statement(self) -> IfStmtNode:
        line = self.previous().line
        column = self.previous().column
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        then_branch = self.parse_statement()
        else_branch = None
        if self.match(TokenType.KW_ELSE):
            else_branch = self.parse_statement()
        return IfStmtNode(condition, then_branch, line, column, else_branch)

    def parse_while_statement(self) -> WhileStmtNode:
        line = self.previous().line
        column = self.previous().column
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        body = self.parse_statement()
        return WhileStmtNode(condition, body, line, column)

    def parse_for_statement(self) -> ForStmtNode:
        line = self.previous().line
        column = self.previous().column
        self.consume(TokenType.LPAREN, "Expected '(' after 'for'")
        init = None
        if not self.check(TokenType.SEMICOLON):
            init = self.parse_expression_statement()
        else:
            self.consume(TokenType.SEMICOLON, "Expected ';'")
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after condition")
        update = None
        if not self.check(TokenType.RPAREN):
            update = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after for header")
        body = self.parse_statement()
        return ForStmtNode(init, condition, update, body, line, column)

    def parse_return_statement(self) -> ReturnStmtNode:
        line = self.previous().line
        column = self.previous().column
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after return")
        return ReturnStmtNode(line, column, value)

    def parse_expression_statement(self) -> ExprStmtNode:
        line = self.peek().line
        column = self.peek().column
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return ExprStmtNode(expr, line, column)