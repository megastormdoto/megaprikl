# src/parser/ast.py
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Any


class NodeType(Enum):
    """Типы узлов AST"""
    PROGRAM = "program"
    FUNCTION_DECL = "function_decl"
    VAR_DECL = "var_decl"
    STRUCT_DECL = "struct_decl"
    PARAM = "param"
    BLOCK = "block"
    IF_STMT = "if_stmt"
    WHILE_STMT = "while_stmt"
    FOR_STMT = "for_stmt"
    RETURN_STMT = "return_stmt"
    EXPR_STMT = "expr_stmt"
    BINARY_EXPR = "binary_expr"
    UNARY_EXPR = "unary_expr"
    LITERAL = "literal"
    IDENTIFIER = "identifier"
    CALL = "call"
    ASSIGNMENT = "assignment"


@dataclass
class ASTNode:
    """Базовый класс для всех узлов AST"""
    node_type: NodeType
    line: int
    column: int

    def __str__(self):
        return f"{self.node_type.value} [{self.line}:{self.column}]"


@dataclass
class ProgramNode(ASTNode):
    """Корневой узел программы"""
    declarations: List[ASTNode] = field(default_factory=list)

    def __init__(self, declarations=None, line=0, column=0):
        super().__init__(NodeType.PROGRAM, line, column)
        self.declarations = declarations or []


@dataclass
class FunctionDeclNode(ASTNode):
    """Объявление функции"""
    name: str
    return_type: str
    parameters: List['ParameterNode']
    body: 'BlockNode'

    def __init__(self, name, return_type, parameters, body, line, column):
        super().__init__(NodeType.FUNCTION_DECL, line, column)
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.body = body


@dataclass
class ParameterNode(ASTNode):
    """Параметр функции"""
    name: str
    param_type: str

    def __init__(self, name, param_type, line, column):
        super().__init__(NodeType.PARAM, line, column)
        self.name = name
        self.param_type = param_type


@dataclass
class VarDeclNode(ASTNode):
    """Объявление переменной"""
    var_type: str
    name: str
    initializer: Optional[ASTNode] = None

    def __init__(self, var_type, name, initializer=None, line=0, column=0):
        super().__init__(NodeType.VAR_DECL, line, column)
        self.var_type = var_type
        self.name = name
        self.initializer = initializer


@dataclass
class StructDeclNode(ASTNode):
    """Объявление структуры"""
    name: str
    fields: List[VarDeclNode]

    def __init__(self, name, fields, line, column):
        super().__init__(NodeType.STRUCT_DECL, line, column)
        self.name = name
        self.fields = fields


@dataclass
class BlockNode(ASTNode):
    """Блок операторов в {}"""
    statements: List[ASTNode]

    def __init__(self, statements, line, column):
        super().__init__(NodeType.BLOCK, line, column)
        self.statements = statements


@dataclass
class IfStmtNode(ASTNode):
    """Условный оператор"""
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None

    def __init__(self, condition, then_branch, else_branch=None, line=0, column=0):
        super().__init__(NodeType.IF_STMT, line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


@dataclass
class WhileStmtNode(ASTNode):
    """Цикл while"""
    condition: ASTNode
    body: ASTNode

    def __init__(self, condition, body, line, column):
        super().__init__(NodeType.WHILE_STMT, line, column)
        self.condition = condition
        self.body = body


@dataclass
class ForStmtNode(ASTNode):
    """Цикл for"""
    init: Optional[ASTNode]
    condition: Optional[ASTNode]
    update: Optional[ASTNode]
    body: ASTNode

    def __init__(self, init, condition, update, body, line, column):
        super().__init__(NodeType.FOR_STMT, line, column)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body


@dataclass
class ReturnStmtNode(ASTNode):
    """Оператор return"""
    value: Optional[ASTNode] = None

    def __init__(self, value=None, line=0, column=0):
        super().__init__(NodeType.RETURN_STMT, line, column)
        self.value = value


@dataclass
class ExprStmtNode(ASTNode):
    """Выражение как оператор"""
    expression: ASTNode

    def __init__(self, expression, line, column):
        super().__init__(NodeType.EXPR_STMT, line, column)
        self.expression = expression


@dataclass
class BinaryExprNode(ASTNode):
    """Бинарное выражение (a + b, a * b и т.д.)"""
    left: ASTNode
    operator: str
    right: ASTNode

    def __init__(self, left, operator, right, line, column):
        super().__init__(NodeType.BINARY_EXPR, line, column)
        self.left = left
        self.operator = operator
        self.right = right


@dataclass
class UnaryExprNode(ASTNode):
    """Унарное выражение (-a, !b)"""
    operator: str
    operand: ASTNode

    def __init__(self, operator, operand, line, column):
        super().__init__(NodeType.UNARY_EXPR, line, column)
        self.operator = operator
        self.operand = operand


@dataclass
class LiteralNode(ASTNode):
    """Литерал (число, строка, булево значение)"""
    value: Any
    literal_type: str  # "int", "float", "bool", "string"

    def __init__(self, value, literal_type, line, column):
        super().__init__(NodeType.LITERAL, line, column)
        self.value = value
        self.literal_type = literal_type


@dataclass
class IdentifierNode(ASTNode):
    """Идентификатор (имя переменной/функции)"""
    name: str

    def __init__(self, name, line, column):
        super().__init__(NodeType.IDENTIFIER, line, column)
        self.name = name


@dataclass
class CallNode(ASTNode):
    """Вызов функции"""
    callee: str
    arguments: List[ASTNode]

    def __init__(self, callee, arguments, line, column):
        super().__init__(NodeType.CALL, line, column)
        self.callee = callee
        self.arguments = arguments


@dataclass
class AssignmentNode(ASTNode):
    """Присваивание (x = 5)"""
    target: str
    operator: str  # "=", "+=", "-=" и т.д.
    value: ASTNode

    def __init__(self, target, operator, value, line, column):
        super().__init__(NodeType.ASSIGNMENT, line, column)
        self.target = target
        self.operator = operator
        self.value = value