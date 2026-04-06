"""Decorated AST printer with type annotations."""

from src.parser.ast import (
    ProgramNode, FunctionDeclNode, VarDeclNode, StructDeclNode,
    BlockNode, IfStmtNode, WhileStmtNode, ForStmtNode, ReturnStmtNode,
    AssignmentNode, BinaryExprNode, UnaryExprNode, CallNode,
    IdentifierNode, LiteralNode, ExprStmtNode
)


class DecoratedASTPrinter:
    """Prints AST with type annotations."""

    def __init__(self):
        self.indent = 0

    def _indent_str(self) -> str:
        return "  " * self.indent

    def print(self, node, has_type=True) -> str:
        """Print decorated AST node."""
        if isinstance(node, ProgramNode):
            return self._print_program(node)
        elif isinstance(node, FunctionDeclNode):
            return self._print_function(node)
        elif isinstance(node, VarDeclNode):
            return self._print_var(node)
        elif isinstance(node, BlockNode):
            return self._print_block(node)
        elif isinstance(node, IfStmtNode):
            return self._print_if(node)
        elif isinstance(node, WhileStmtNode):
            return self._print_while(node)
        elif isinstance(node, ForStmtNode):
            return self._print_for(node)
        elif isinstance(node, ReturnStmtNode):
            return self._print_return(node)
        elif isinstance(node, AssignmentNode):
            return self._print_assignment(node)
        elif isinstance(node, BinaryExprNode):
            return self._print_binary(node)
        elif isinstance(node, UnaryExprNode):
            return self._print_unary(node)
        elif isinstance(node, CallNode):
            return self._print_call(node)
        elif isinstance(node, IdentifierNode):
            return self._print_identifier(node)
        elif isinstance(node, LiteralNode):
            return self._print_literal(node)
        elif isinstance(node, ExprStmtNode):
            return self._print_expr_stmt(node)
        return f"{node}"

    def _print_program(self, node: ProgramNode) -> str:
        result = f"Program [line {node.line}:{node.column}]\n"
        self.indent += 1
        for decl in node.declarations:
            result += f"{self._indent_str()}{self.print(decl)}\n"
        self.indent -= 1
        return result.rstrip()

    def _print_function(self, node: FunctionDeclNode) -> str:
        type_info = ""
        if hasattr(node, 'semantic_type') and node.semantic_type:
            type_info = f" -> {node.semantic_type}"

        result = f"FunctionDecl: {node.name}{type_info} [line {node.line}:{node.column}]"

        if node.parameters:
            result += f"\n{self._indent_str()}  Parameters:"
            self.indent += 2
            for param in node.parameters:
                param_type = ""
                if hasattr(param, 'semantic_type') and param.semantic_type:
                    param_type = f": {param.semantic_type}"
                result += f"\n{self._indent_str()}- {param.name}{param_type}"
            self.indent -= 2

        result += f"\n{self._indent_str()}  Body:"
        self.indent += 2
        result += f"\n{self._indent_str()}{self.print(node.body)}"
        self.indent -= 2

        return result

    def _print_var(self, node: VarDeclNode) -> str:
        type_info = ""
        if hasattr(node, 'semantic_type') and node.semantic_type:
            type_info = f": {node.semantic_type}"

        result = f"VarDecl: {node.name}{type_info} [line {node.line}:{node.column}]"

        if node.initializer:
            self.indent += 1
            result += f"\n{self._indent_str()}= {self.print(node.initializer)}"
            self.indent -= 1

        return result

    def _print_block(self, node: BlockNode) -> str:
        result = f"Block [line {node.line}:{node.column}]"
        if node.statements:
            self.indent += 1
            for stmt in node.statements:
                result += f"\n{self._indent_str()}{self.print(stmt)}"
            self.indent -= 1
        return result

    def _print_if(self, node: IfStmtNode) -> str:
        result = f"IfStmt [line {node.line}:{node.column}]"
        self.indent += 1
        result += f"\n{self._indent_str()}Condition: {self.print(node.condition)}"
        result += f"\n{self._indent_str()}Then: {self.print(node.then_branch)}"
        if node.else_branch:
            result += f"\n{self._indent_str()}Else: {self.print(node.else_branch)}"
        self.indent -= 1
        return result

    def _print_while(self, node: WhileStmtNode) -> str:
        result = f"WhileStmt [line {node.line}:{node.column}]"
        self.indent += 1
        result += f"\n{self._indent_str()}Condition: {self.print(node.condition)}"
        result += f"\n{self._indent_str()}Body: {self.print(node.body)}"
        self.indent -= 1
        return result

    def _print_for(self, node: ForStmtNode) -> str:
        result = f"ForStmt [line {node.line}:{node.column}]"
        self.indent += 1
        if node.initializer:
            result += f"\n{self._indent_str()}Init: {self.print(node.initializer)}"
        if node.condition:
            result += f"\n{self._indent_str()}Cond: {self.print(node.condition)}"
        if node.increment:
            result += f"\n{self._indent_str()}Incr: {self.print(node.increment)}"
        result += f"\n{self._indent_str()}Body: {self.print(node.body)}"
        self.indent -= 1
        return result

    def _print_return(self, node: ReturnStmtNode) -> str:
        type_info = ""
        if hasattr(node, 'semantic_type') and node.semantic_type:
            type_info = f" [{node.semantic_type}]"

        result = f"ReturnStmt{type_info} [line {node.line}:{node.column}]"
        if node.value:
            self.indent += 1
            result += f"\n{self._indent_str()}{self.print(node.value)}"
            self.indent -= 1
        return result

    def _print_assignment(self, node: AssignmentNode) -> str:
        type_info = ""
        if hasattr(node, 'semantic_type') and node.semantic_type:
            type_info = f" [{node.semantic_type}]"

        result = f"Assignment{type_info} [line {node.line}:{node.column}]"
        self.indent += 1
        result += f"\n{self._indent_str()}Left: {self.print(node.left)}"
        result += f"\n{self._indent_str()}Right: {self.print(node.right)}"
        self.indent -= 1
        return result

    def _print_binary(self, node: BinaryExprNode) -> str:
        type_info = ""
        if hasattr(node, 'semantic_type') and node.semantic_type:
            type_info = f" [{node.semantic_type}]"

        return f"BinaryOp: {node.operator}{type_info} [line {node.line}:{node.column}]"

    def _print_unary(self, node: UnaryExprNode) -> str:
        type_info = ""
        if hasattr(node, 'semantic_type') and node.semantic_type:
            type_info = f" [{node.semantic_type}]"

        return f"UnaryOp: {node.operator}{type_info} [line {node.line}:{node.column}]"

    def _print_call(self, node: CallNode) -> str:
        type_info = ""
        if hasattr(node, 'semantic_type') and node.semantic_type:
            type_info = f" -> {node.semantic_type}"

        result = f"Call: {node.callee}{type_info} [line {node.line}:{node.column}]"
        if node.arguments:
            self.indent += 1
            for arg in node.arguments:
                result += f"\n{self._indent_str()}Arg: {self.print(arg)}"
            self.indent -= 1
        return result

    def _print_identifier(self, node: IdentifierNode) -> str:
        type_info = ""
        if hasattr(node, 'semantic_type') and node.semantic_type:
            type_info = f": {node.semantic_type}"

        return f"Identifier: {node.name}{type_info} [line {node.line}:{node.column}]"

    def _print_literal(self, node: LiteralNode) -> str:
        type_info = ""
        if hasattr(node, 'semantic_type') and node.semantic_type:
            type_info = f" [{node.semantic_type}]"

        return f"Literal: {node.value}{type_info} [line {node.line}:{node.column}]"

    def _print_expr_stmt(self, node: ExprStmtNode) -> str:
        return f"ExprStmt [line {node.line}:{node.column}]\n{self._indent_str()}  {self.print(node.expression)}"