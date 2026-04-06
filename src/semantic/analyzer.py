"""Semantic analyzer that traverses AST and validates all language rules."""

from typing import List, Optional
from src.parser.ast import (
    ProgramNode, FunctionDeclNode, VarDeclNode, StructDeclNode,
    BlockNode, IfStmtNode, WhileStmtNode, ForStmtNode, ReturnStmtNode,
    AssignmentNode, BinaryExprNode, UnaryExprNode, CallNode,
    IdentifierNode, LiteralNode, ExprStmtNode, ParameterNode,
    ASTNode
)
from src.semantic.symbol_table import SymbolTable, Symbol, SymbolKind
from src.semantic.type_system import Type, BaseType, TypeSystem
from src.semantic.errors import ErrorCollector


class SemanticAnalyzer:
    """SEM-1: Основной семантический анализатор."""

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = ErrorCollector()
        self.current_function: Optional[Symbol] = None
        self.in_loop = False
        self.decorated_ast = None

    def analyze(self, ast: ProgramNode) -> bool:
        """SEM-1: Запускает все семантические проверки."""
        self.decorated_ast = ast
        self.visit_program(ast)
        return len(self.errors.errors) == 0

    def get_errors(self):
        return self.errors.errors

    def get_symbol_table(self) -> SymbolTable:
        return self.symbol_table

    def get_decorated_ast(self) -> ProgramNode:
        return self.decorated_ast

    # ========== VISITOR METHODS ==========

    def visit_program(self, node: ProgramNode):
        """Обрабатывает всю программу."""
        # ПЕРВЫЙ ПРОХОД: собираем объявления
        for decl in node.declarations:
            if isinstance(decl, FunctionDeclNode):
                self._declare_function(decl)
            elif isinstance(decl, StructDeclNode):
                self._declare_struct(decl)

        # ВТОРОЙ ПРОХОД: анализируем тела
        for decl in node.declarations:
            if isinstance(decl, FunctionDeclNode):
                self.visit_function_decl(decl)
            elif isinstance(decl, VarDeclNode):
                self.visit_var_decl(decl)

    def _declare_function(self, node: FunctionDeclNode):
        """Объявляет функцию."""
        return_type = self._convert_type(node.return_type)

        param_types = []
        for param in node.parameters:
            param_types.append(self._convert_type(param.param_type))

        existing = self.symbol_table.lookup(node.name)
        if existing and existing.kind == SymbolKind.FUNCTION:
            self.errors.add(
                node.line, node.column,
                f"duplicate function: '{node.name}'",
                "duplicate_declaration"
            )
            return

        func_sym = Symbol(
            name=node.name,
            kind=SymbolKind.FUNCTION,
            type=return_type,
            line=node.line,
            column=node.column,
            parameters=param_types,
            return_type=return_type
        )
        self.symbol_table.insert(node.name, func_sym)

    def _declare_struct(self, node: StructDeclNode):
        """Объявляет структуру."""
        existing = self.symbol_table.lookup(node.name)
        if existing:
            self.errors.add(
                node.line, node.column,
                f"duplicate struct: '{node.name}'",
                "duplicate_declaration"
            )
            return

        fields = {}
        for field_name, field_type in node.fields.items():
            if field_name in fields:
                self.errors.add(
                    node.line, node.column,
                    f"duplicate field '{field_name}'",
                    "duplicate_declaration"
                )
            fields[field_name] = self._convert_type(field_type)

        struct_type = Type(kind=node.name, is_struct=True, fields=fields)
        struct_sym = Symbol(
            name=node.name,
            kind=SymbolKind.STRUCT,
            type=struct_type,
            line=node.line,
            column=node.column,
            fields=fields
        )
        self.symbol_table.insert(node.name, struct_sym)

    def _convert_type(self, type_name: str) -> Type:
        """Конвертирует строковый тип во внутренний."""
        if type_name == "int":
            return Type(BaseType.INT)
        elif type_name == "float":
            return Type(BaseType.FLOAT)
        elif type_name == "bool":
            return Type(BaseType.BOOL)
        elif type_name == "void":
            return Type(BaseType.VOID)
        elif type_name == "string":
            return Type(BaseType.STRING)
        else:
            # Возможно, это имя структуры
            return Type(kind=type_name, is_struct=True)

    def visit_function_decl(self, node: FunctionDeclNode):
        """Проверяет тело функции."""
        func_sym = self.symbol_table.lookup(node.name)
        if not func_sym:
            return

        self.symbol_table.enter_scope()
        self.current_function = func_sym

        for param in node.parameters:
            param_type = self._convert_type(param.param_type)
            param_sym = Symbol(
                name=param.name,
                kind=SymbolKind.PARAMETER,
                type=param_type,
                line=param.line,
                column=param.column
            )
            self.symbol_table.insert(param.name, param_sym)

        self.visit_block(node.body)
        self.symbol_table.exit_scope()
        self.current_function = None

    def visit_block(self, node: BlockNode):
        """Обрабатывает блок."""
        self.symbol_table.enter_scope()
        for stmt in node.statements:
            self.visit_statement(stmt)
        self.symbol_table.exit_scope()

    def visit_statement(self, node):
        """Обрабатывает операторы."""
        if isinstance(node, VarDeclNode):
            self.visit_var_decl(node)
        elif isinstance(node, AssignmentNode):
            self.visit_assignment(node)
        elif isinstance(node, IfStmtNode):
            self.visit_if(node)
        elif isinstance(node, WhileStmtNode):
            self.visit_while(node)
        elif isinstance(node, ForStmtNode):
            self.visit_for(node)
        elif isinstance(node, ReturnStmtNode):
            self.visit_return(node)
        elif isinstance(node, BlockNode):
            self.visit_block(node)
        elif isinstance(node, CallNode):
            self.visit_call(node)
        elif isinstance(node, ExprStmtNode):
            if node.expression:
                self.visit_expression(node.expression)

    def visit_var_decl(self, node: VarDeclNode):
        """Проверяет объявление переменной."""
        var_type = self._convert_type(node.var_type)

        if self.symbol_table.lookup_local(node.name):
            self.errors.add(
                node.line, node.column,
                f"duplicate variable: '{node.name}'",
                "duplicate_declaration"
            )
            return

        if node.initializer:
            init_type = self.visit_expression(node.initializer)
            if not TypeSystem.is_compatible(var_type, init_type):
                self.errors.add_type_mismatch(
                    node.line, node.column,
                    f"cannot initialize '{node.name}'",
                    expected=str(var_type),
                    actual=str(init_type)
                )

        var_sym = Symbol(
            name=node.name,
            kind=SymbolKind.VARIABLE,
            type=var_type,
            line=node.line,
            column=node.column
        )
        self.symbol_table.insert(node.name, var_sym)
        node.semantic_type = var_type
        node.symbol = var_sym

    def visit_assignment(self, node: AssignmentNode):
        """Проверяет присваивание."""
        if isinstance(node.left, IdentifierNode):
            var_sym = self.symbol_table.lookup(node.left.name)
            if not var_sym:
                self.errors.add_undeclared(node.left.line, node.left.column, node.left.name)
                return
            left_type = var_sym.type
            node.left.symbol = var_sym
        else:
            left_type = self.visit_expression(node.left)

        right_type = self.visit_expression(node.right)

        if not TypeSystem.is_compatible(left_type, right_type):
            self.errors.add_type_mismatch(
                node.line, node.column,
                "type mismatch in assignment",
                expected=str(left_type),
                actual=str(right_type)
            )

        node.semantic_type = left_type

    def visit_expression(self, node):
        """Определяет тип выражения."""
        if isinstance(node, LiteralNode):
            return self.visit_literal(node)
        elif isinstance(node, IdentifierNode):
            return self.visit_identifier(node)
        elif isinstance(node, BinaryExprNode):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryExprNode):
            return self.visit_unary_op(node)
        elif isinstance(node, CallNode):
            return self.visit_call(node)
        return Type(BaseType.VOID)

    def visit_literal(self, node: LiteralNode) -> Type:
        """Тип литерала."""
        if node.literal_type == "int":
            node.semantic_type = Type(BaseType.INT)
        elif node.literal_type == "float":
            node.semantic_type = Type(BaseType.FLOAT)
        elif node.literal_type == "bool":
            node.semantic_type = Type(BaseType.BOOL)
        elif node.literal_type == "string":
            node.semantic_type = Type(BaseType.STRING)
        else:
            node.semantic_type = Type(BaseType.VOID)
        return node.semantic_type

    def visit_identifier(self, node: IdentifierNode) -> Type:
        """Проверяет идентификатор."""
        sym = self.symbol_table.lookup(node.name)
        if not sym:
            self.errors.add_undeclared(node.line, node.column, node.name)
            node.semantic_type = Type(BaseType.VOID)
            return node.semantic_type

        node.symbol = sym
        node.semantic_type = sym.type
        return sym.type

    def visit_binary_op(self, node: BinaryExprNode) -> Type:
        """Проверяет бинарную операцию."""
        left_type = self.visit_expression(node.left)
        right_type = self.visit_expression(node.right)

        result_type = TypeSystem.binary_operator_result_type(
            node.operator, left_type, right_type
        )

        if result_type is None:
            self.errors.add_type_mismatch(
                node.line, node.column,
                f"operator '{node.operator}' cannot be applied",
                expected="compatible types",
                actual=f"{left_type} {node.operator} {right_type}"
            )
            result_type = Type(BaseType.VOID)

        node.semantic_type = result_type
        return result_type

    def visit_unary_op(self, node: UnaryExprNode) -> Type:
        """Проверяет унарную операцию."""
        operand_type = self.visit_expression(node.operand)

        result_type = TypeSystem.unary_operator_result_type(node.operator, operand_type)

        if result_type is None:
            self.errors.add_type_mismatch(
                node.line, node.column,
                f"operator '{node.operator}' cannot be applied to {operand_type}",
                expected="numeric or boolean",
                actual=str(operand_type)
            )
            result_type = Type(BaseType.VOID)

        node.semantic_type = result_type
        return result_type

    def visit_call(self, node: CallNode) -> Type:
        """Проверяет вызов функции. Использует node.callee вместо node.name."""
        func_name = node.callee

        func_sym = self.symbol_table.lookup(func_name)

        if not func_sym or func_sym.kind != SymbolKind.FUNCTION:
            self.errors.add(
                node.line, node.column,
                f"'{func_name}' is not a function",
                "undeclared"
            )
            node.semantic_type = Type(BaseType.VOID)
            return node.semantic_type

        expected_count = len(func_sym.parameters) if func_sym.parameters else 0
        actual_count = len(node.arguments)

        if expected_count != actual_count:
            self.errors.add(
                node.line, node.column,
                f"argument count mismatch for '{func_name}'",
                "argument_count_mismatch",
                details=f"expected {expected_count}, found {actual_count}"
            )

        for i, arg in enumerate(node.arguments):
            if i >= expected_count:
                break
            arg_type = self.visit_expression(arg)
            expected_type = func_sym.parameters[i]

            if not TypeSystem.is_compatible(expected_type, arg_type):
                self.errors.add_type_mismatch(
                    arg.line, arg.column,
                    f"argument {i + 1} of '{func_name}' has wrong type",
                    expected=str(expected_type),
                    actual=str(arg_type)
                )

        node.semantic_type = func_sym.return_type
        node.function_symbol = func_sym
        return func_sym.return_type

    def visit_if(self, node: IfStmtNode):
        """Проверяет if."""
        cond_type = self.visit_expression(node.condition)
        if cond_type.kind != BaseType.BOOL:
            self.errors.add_type_mismatch(
                node.condition.line, node.condition.column,
                "if condition must be boolean",
                expected="bool",
                actual=str(cond_type)
            )

        self.visit_statement(node.then_branch)
        if node.else_branch:
            self.visit_statement(node.else_branch)

    def visit_while(self, node: WhileStmtNode):
        """Проверяет while."""
        cond_type = self.visit_expression(node.condition)
        if cond_type.kind != BaseType.BOOL:
            self.errors.add_type_mismatch(
                node.condition.line, node.condition.column,
                "while condition must be boolean",
                expected="bool",
                actual=str(cond_type)
            )

        old_in_loop = self.in_loop
        self.in_loop = True
        self.visit_statement(node.body)
        self.in_loop = old_in_loop

    def visit_for(self, node: ForStmtNode):
        """Проверяет for."""
        if node.initializer:
            self.visit_statement(node.initializer)
        if node.condition:
            cond_type = self.visit_expression(node.condition)
            if cond_type.kind != BaseType.BOOL:
                self.errors.add_type_mismatch(
                    node.condition.line, node.condition.column,
                    "for condition must be boolean",
                    expected="bool",
                    actual=str(cond_type)
                )
        if node.increment:
            self.visit_expression(node.increment)

        old_in_loop = self.in_loop
        self.in_loop = True
        self.visit_statement(node.body)
        self.in_loop = old_in_loop

    def visit_return(self, node: ReturnStmtNode):
        """Проверяет return."""
        if not self.current_function:
            self.errors.add(
                node.line, node.column,
                "return outside function",
                "invalid_return"
            )
            return

        expected_type = self.current_function.return_type

        if node.value:
            actual_type = self.visit_expression(node.value)
            if not TypeSystem.is_compatible(expected_type, actual_type):
                self.errors.add_type_mismatch(
                    node.line, node.column,
                    f"return type mismatch in '{self.current_function.name}'",
                    expected=str(expected_type),
                    actual=str(actual_type)
                )
            node.semantic_type = actual_type
        else:
            if expected_type.kind != BaseType.VOID:
                self.errors.add(
                    node.line, node.column,
                    f"non-void function must return a value",
                    "invalid_return"
                )
            node.semantic_type = Type(BaseType.VOID)

    def print_symbol_table(self):
        """Выводит таблицу символов."""
        print(self.symbol_table.dump())

    def print_errors(self):
        """Выводит ошибки."""
        for error in self.errors.errors:
            print(error)