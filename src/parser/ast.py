# src/parser/ast.py
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Any


class NodeType(Enum):
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
    ARRAY_DECL = "array_decl"
    ARRAY_ACCESS = "array_access"


@dataclass
class ASTNode:
    node_type: NodeType
    line: int
    column: int

    def __str__(self):
        return f"{self.node_type.value} [{self.line}:{self.column}]"


@dataclass
class ProgramNode(ASTNode):
    declarations: List[ASTNode] = field(default_factory=list)

    def __init__(self, declarations=None, line=0, column=0):
        super().__init__(NodeType.PROGRAM, line, column)
        self.declarations = declarations or []


@dataclass
class FunctionDeclNode(ASTNode):
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
    name: str
    param_type: str

    def __init__(self, name, param_type, line, column):
        super().__init__(NodeType.PARAM, line, column)
        self.name = name
        self.param_type = param_type


@dataclass
class VarDeclNode(ASTNode):
    var_type: str
    name: str
    initializer: Optional[ASTNode] = None

    def __init__(self, var_type, name, initializer=None, line=0, column=0):
        super().__init__(NodeType.VAR_DECL, line, column)
        self.var_type = var_type
        self.name = name
        self.initializer = initializer


@dataclass
class ArrayDeclNode(ASTNode):
    element_type: str
    name: str
    size: ASTNode

    def __init__(self, element_type, name, size, line, column):
        super().__init__(NodeType.ARRAY_DECL, line, column)
        self.element_type = element_type
        self.name = name
        self.size = size


@dataclass
class ArrayAccessNode(ASTNode):
    array: str
    index: ASTNode

    def __init__(self, array, index, line, column):
        super().__init__(NodeType.ARRAY_ACCESS, line, column)
        self.array = array
        self.index = index


@dataclass
class StructDeclNode(ASTNode):
    name: str
    fields: List[VarDeclNode]

    def __init__(self, name, fields, line, column):
        super().__init__(NodeType.STRUCT_DECL, line, column)
        self.name = name
        self.fields = fields


@dataclass
class BlockNode(ASTNode):
    statements: List[ASTNode]

    def __init__(self, statements, line, column):
        super().__init__(NodeType.BLOCK, line, column)
        self.statements = statements


@dataclass
class IfStmtNode(ASTNode):
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
    condition: ASTNode
    body: ASTNode

    def __init__(self, condition, body, line, column):
        super().__init__(NodeType.WHILE_STMT, line, column)
        self.condition = condition
        self.body = body


@dataclass
class ForStmtNode(ASTNode):
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
    value: Optional[ASTNode] = None

    def __init__(self, value=None, line=0, column=0):
        super().__init__(NodeType.RETURN_STMT, line, column)
        self.value = value


@dataclass
class ExprStmtNode(ASTNode):
    expression: ASTNode

    def __init__(self, expression, line, column):
        super().__init__(NodeType.EXPR_STMT, line, column)
        self.expression = expression


@dataclass
class BinaryExprNode(ASTNode):
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
    operator: str
    operand: ASTNode

    def __init__(self, operator, operand, line, column):
        super().__init__(NodeType.UNARY_EXPR, line, column)
        self.operator = operator
        self.operand = operand


@dataclass
class LiteralNode(ASTNode):
    value: Any
    literal_type: str

    def __init__(self, value, literal_type, line, column):
        super().__init__(NodeType.LITERAL, line, column)
        self.value = value
        self.literal_type = literal_type


@dataclass
class IdentifierNode(ASTNode):
    name: str

    def __init__(self, name, line, column):
        super().__init__(NodeType.IDENTIFIER, line, column)
        self.name = name


@dataclass
class CallNode(ASTNode):
    callee: str
    arguments: List[ASTNode]

    def __init__(self, callee, arguments, line, column):
        super().__init__(NodeType.CALL, line, column)
        self.callee = callee
        self.arguments = arguments


@dataclass
class AssignmentNode(ASTNode):
    target: str
    operator: str
    value: ASTNode

    def __init__(self, target, operator, value, line, column):
        super().__init__(NodeType.ASSIGNMENT, line, column)
        self.target = target
        self.operator = operator
        self.value = value


@dataclass
class ArrayInitNode(ASTNode):
    values: List[ASTNode]

    def __init__(self, values, line, column):
        super().__init__(NodeType.LITERAL, line, column)
        self.values = values

@dataclass
class ArrayDeclNode(ASTNode):
    element_type: str
    name: str
    size: ASTNode
    initializer: Optional[List[ASTNode]] = None  # добавить это поле

    def __init__(self, element_type, name, size, line, column, initializer=None):
        super().__init__(NodeType.VAR_DECL, line, column)
        self.element_type = element_type
        self.name = name
        self.size = size
        self.initializer = initializer