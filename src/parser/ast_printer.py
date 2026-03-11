# src/parser/ast_printer.py
from src.parser.ast import *


class ASTPrinter:
    """Класс для красивого вывода AST"""

    def __init__(self):
        self.indent_level = 0

    def indent(self):
        """Возвращает отступ"""
        return "  " * self.indent_level

    def print(self, node: ASTNode) -> str:
        """Главный метод печати"""
        if node is None:
            return "None"

        if node.node_type == NodeType.PROGRAM:
            return self.print_program(node)
        elif node.node_type == NodeType.FUNCTION_DECL:
            return self.print_function_decl(node)
        elif node.node_type == NodeType.VAR_DECL:
            return self.print_var_decl(node)
        elif node.node_type == NodeType.STRUCT_DECL:
            return self.print_struct_decl(node)
        elif node.node_type == NodeType.PARAM:
            return self.print_param(node)
        elif node.node_type == NodeType.BLOCK:
            return self.print_block(node)
        elif node.node_type == NodeType.IF_STMT:
            return self.print_if_stmt(node)
        elif node.node_type == NodeType.WHILE_STMT:
            return self.print_while_stmt(node)
        elif node.node_type == NodeType.FOR_STMT:
            return self.print_for_stmt(node)
        elif node.node_type == NodeType.RETURN_STMT:
            return self.print_return_stmt(node)
        elif node.node_type == NodeType.EXPR_STMT:
            return self.print_expr_stmt(node)
        elif node.node_type == NodeType.BINARY_EXPR:
            return self.print_binary_expr(node)
        elif node.node_type == NodeType.UNARY_EXPR:
            return self.print_unary_expr(node)
        elif node.node_type == NodeType.LITERAL:
            return self.print_literal(node)
        elif node.node_type == NodeType.IDENTIFIER:
            return self.print_identifier(node)
        elif node.node_type == NodeType.CALL:
            return self.print_call(node)
        elif node.node_type == NodeType.ASSIGNMENT:
            return self.print_assignment(node)
        else:
            return f"{self.indent()}Unknown node: {node.node_type}\n"

    def print_program(self, node: ProgramNode) -> str:
        result = f"{self.indent()}Program [{node.line}:{node.column}]:\n"
        self.indent_level += 1
        for decl in node.declarations:
            result += self.print(decl)
        self.indent_level -= 1
        return result

    def print_function_decl(self, node: FunctionDeclNode) -> str:
        result = f"{self.indent()}FunctionDecl: {node.name} -> {node.return_type} [{node.line}:{node.column}]\n"
        self.indent_level += 1
        result += f"{self.indent()}Parameters:\n"
        self.indent_level += 1
        for param in node.parameters:
            result += self.print(param)
        self.indent_level -= 1
        result += f"{self.indent()}Body:\n"
        self.indent_level += 1
        result += self.print(node.body)
        self.indent_level -= 2
        return result

    def print_var_decl(self, node: VarDeclNode) -> str:
        result = f"{self.indent()}VarDecl: {node.var_type} {node.name}"
        if node.initializer:
            result += f" = ..."
        result += f" [{node.line}:{node.column}]\n"
        if node.initializer:
            self.indent_level += 1
            result += self.print(node.initializer)
            self.indent_level -= 1
        return result

    def print_struct_decl(self, node: StructDeclNode) -> str:
        result = f"{self.indent()}StructDecl: {node.name} [{node.line}:{node.column}]\n"
        self.indent_level += 1
        result += f"{self.indent()}Fields:\n"
        self.indent_level += 1
        for field in node.fields:
            result += self.print(field)
        self.indent_level -= 2
        return result

    def print_param(self, node: ParameterNode) -> str:
        return f"{self.indent()}Param: {node.param_type} {node.name} [{node.line}:{node.column}]\n"

    def print_block(self, node: BlockNode) -> str:
        result = f"{self.indent()}Block [{node.line}:{node.column}]:\n"
        self.indent_level += 1
        for stmt in node.statements:
            result += self.print(stmt)
        self.indent_level -= 1
        return result

    def print_if_stmt(self, node: IfStmtNode) -> str:
        result = f"{self.indent()}IfStmt [{node.line}:{node.column}]:\n"
        self.indent_level += 1
        result += f"{self.indent()}Condition:\n"
        self.indent_level += 1
        result += self.print(node.condition)
        self.indent_level -= 1
        result += f"{self.indent()}Then:\n"
        self.indent_level += 1
        result += self.print(node.then_branch)
        self.indent_level -= 1
        if node.else_branch:
            result += f"{self.indent()}Else:\n"
            self.indent_level += 1
            result += self.print(node.else_branch)
            self.indent_level -= 1
        self.indent_level -= 1
        return result

    def print_while_stmt(self, node: WhileStmtNode) -> str:
        result = f"{self.indent()}WhileStmt [{node.line}:{node.column}]:\n"
        self.indent_level += 1
        result += f"{self.indent()}Condition:\n"
        self.indent_level += 1
        result += self.print(node.condition)
        self.indent_level -= 1
        result += f"{self.indent()}Body:\n"
        self.indent_level += 1
        result += self.print(node.body)
        self.indent_level -= 2
        return result

    def print_for_stmt(self, node: ForStmtNode) -> str:
        result = f"{self.indent()}ForStmt [{node.line}:{node.column}]:\n"
        self.indent_level += 1
        if node.init:
            result += f"{self.indent()}Init:\n"
            self.indent_level += 1
            result += self.print(node.init)
            self.indent_level -= 1
        if node.condition:
            result += f"{self.indent()}Condition:\n"
            self.indent_level += 1
            result += self.print(node.condition)
            self.indent_level -= 1
        if node.update:
            result += f"{self.indent()}Update:\n"
            self.indent_level += 1
            result += self.print(node.update)
            self.indent_level -= 1
        result += f"{self.indent()}Body:\n"
        self.indent_level += 1
        result += self.print(node.body)
        self.indent_level -= 2
        return result

    def print_return_stmt(self, node: ReturnStmtNode) -> str:
        result = f"{self.indent()}Return"
        if node.value:
            result += f" [{node.line}:{node.column}]:\n"
            self.indent_level += 1
            result += self.print(node.value)
            self.indent_level -= 1
        else:
            result += f" void [{node.line}:{node.column}]\n"
        return result

    def print_expr_stmt(self, node: ExprStmtNode) -> str:
        result = f"{self.indent()}ExprStmt [{node.line}:{node.column}]:\n"
        self.indent_level += 1
        result += self.print(node.expression)
        self.indent_level -= 1
        return result

    def print_binary_expr(self, node: BinaryExprNode) -> str:
        result = f"{self.indent()}Binary: {node.operator} [{node.line}:{node.column}]\n"
        self.indent_level += 1
        result += f"{self.indent()}Left:\n"
        self.indent_level += 1
        result += self.print(node.left)
        self.indent_level -= 1
        result += f"{self.indent()}Right:\n"
        self.indent_level += 1
        result += self.print(node.right)
        self.indent_level -= 2
        return result

    def print_unary_expr(self, node: UnaryExprNode) -> str:
        result = f"{self.indent()}Unary: {node.operator} [{node.line}:{node.column}]\n"
        self.indent_level += 1
        result += self.print(node.operand)
        self.indent_level -= 1
        return result

    def print_literal(self, node: LiteralNode) -> str:
        return f"{self.indent()}Literal: {node.value} ({node.literal_type}) [{node.line}:{node.column}]\n"

    def print_identifier(self, node: IdentifierNode) -> str:
        return f"{self.indent()}Identifier: {node.name} [{node.line}:{node.column}]\n"

    def print_call(self, node: CallNode) -> str:
        result = f"{self.indent()}Call: {node.callee} [{node.line}:{node.column}]\n"
        self.indent_level += 1
        result += f"{self.indent()}Arguments:\n"
        self.indent_level += 1
        for arg in node.arguments:
            result += self.print(arg)
        self.indent_level -= 2
        return result

    def print_assignment(self, node: AssignmentNode) -> str:
        result = f"{self.indent()}Assignment: {node.target} {node.operator} [{node.line}:{node.column}]\n"
        self.indent_level += 1
        result += self.print(node.value)
        self.indent_level -= 1
        return result