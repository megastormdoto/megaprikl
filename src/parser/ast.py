from enum import Enum
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


class ASTNode:
    def __init__(self, node_type: NodeType, line: int, column: int):
        self.node_type = node_type
        self.line = line
        self.column = column


class ProgramNode(ASTNode):
    def __init__(self, declarations: List[ASTNode] = None, line: int = 0, column: int = 0):
        super().__init__(NodeType.PROGRAM, line, column)
        self.declarations = declarations or []


class FunctionDeclNode(ASTNode):
    def __init__(self, name: str, return_type: str, parameters: List['ParameterNode'], 
                 body: Optional['BlockNode'], line: int, column: int, is_extern: bool = False):
        super().__init__(NodeType.FUNCTION_DECL, line, column)
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.body = body
        self.is_extern = is_extern


class ParameterNode(ASTNode):
    def __init__(self, name: str, param_type: str, line: int, column: int):
        super().__init__(NodeType.PARAM, line, column)
        self.name = name
        self.param_type = param_type


class VarDeclNode(ASTNode):
    def __init__(self, var_type: str, name: str, line: int, column: int, initializer: Optional[ASTNode] = None):
        super().__init__(NodeType.VAR_DECL, line, column)
        self.var_type = var_type
        self.name = name
        self.initializer = initializer


class ArrayDeclNode(ASTNode):
    def __init__(self, element_type: str, name: str, size: ASTNode, line: int, column: int, 
                 initializer: Optional[List[ASTNode]] = None):
        super().__init__(NodeType.ARRAY_DECL, line, column)
        self.element_type = element_type
        self.name = name
        self.size = size
        self.initializer = initializer


class ArrayAccessNode(ASTNode):
    def __init__(self, array: str, index: ASTNode, line: int, column: int):
        super().__init__(NodeType.ARRAY_ACCESS, line, column)
        self.array = array
        self.index = index


class StructDeclNode(ASTNode):
    def __init__(self, name: str, fields: List[VarDeclNode], line: int, column: int):
        super().__init__(NodeType.STRUCT_DECL, line, column)
        self.name = name
        self.fields = fields


class BlockNode(ASTNode):
    def __init__(self, statements: List[ASTNode], line: int, column: int):
        super().__init__(NodeType.BLOCK, line, column)
        self.statements = statements


class IfStmtNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: ASTNode, line: int, column: int, 
                 else_branch: Optional[ASTNode] = None):
        super().__init__(NodeType.IF_STMT, line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStmtNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode, line: int, column: int):
        super().__init__(NodeType.WHILE_STMT, line, column)
        self.condition = condition
        self.body = body


class ForStmtNode(ASTNode):
    def __init__(self, init: Optional[ASTNode], condition: Optional[ASTNode], 
                 update: Optional[ASTNode], body: ASTNode, line: int, column: int):
        super().__init__(NodeType.FOR_STMT, line, column)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body


class ReturnStmtNode(ASTNode):
    def __init__(self, line: int, column: int, value: Optional[ASTNode] = None):
        super().__init__(NodeType.RETURN_STMT, line, column)
        self.value = value


class ExprStmtNode(ASTNode):
    def __init__(self, expression: ASTNode, line: int, column: int):
        super().__init__(NodeType.EXPR_STMT, line, column)
        self.expression = expression


class BinaryExprNode(ASTNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode, line: int, column: int):
        super().__init__(NodeType.BINARY_EXPR, line, column)
        self.left = left
        self.operator = operator
        self.right = right


class UnaryExprNode(ASTNode):
    def __init__(self, operator: str, operand: ASTNode, line: int, column: int):
        super().__init__(NodeType.UNARY_EXPR, line, column)
        self.operator = operator
        self.operand = operand


class LiteralNode(ASTNode):
    def __init__(self, value: Any, literal_type: str, line: int, column: int):
        super().__init__(NodeType.LITERAL, line, column)
        self.value = value
        self.literal_type = literal_type


class IdentifierNode(ASTNode):
    def __init__(self, name: str, line: int, column: int):
        super().__init__(NodeType.IDENTIFIER, line, column)
        self.name = name


class CallNode(ASTNode):
    def __init__(self, callee: str, arguments: List[ASTNode], line: int, column: int):
        super().__init__(NodeType.CALL, line, column)
        self.callee = callee
        self.arguments = arguments


class AssignmentNode(ASTNode):
    def __init__(self, target: str, operator: str, value: ASTNode, line: int, column: int):
        super().__init__(NodeType.ASSIGNMENT, line, column)
        self.target = target
        self.operator = operator
        self.value = value
