"""IR instruction set and operand types for three-address code."""

from enum import Enum


class OperandType(Enum):
    """Types of operands in IR instructions."""
    TEMP = "temp"
    VARIABLE = "var"
    LITERAL = "literal"
    LABEL = "label"


class Operand:
    """An operand in an IR instruction."""

    def __init__(self, type, value, ir_type=None):
        self.type = type
        self.value = value
        self.ir_type = ir_type

    def __str__(self):
        if self.type == OperandType.TEMP:
            return f"t{self.value}"
        elif self.type == OperandType.VARIABLE:
            return f"{self.value}"
        elif self.type == OperandType.LITERAL:
            if isinstance(self.value, bool):
                return "true" if self.value else "false"
            return str(self.value)
        elif self.type == OperandType.LABEL:
            return f"L{self.value}"
        return f"<{self.type.value}:{self.value}>"

    @staticmethod
    def temp(idx, ir_type=None):
        return Operand(OperandType.TEMP, idx, ir_type)

    @staticmethod
    def var(name, ir_type=None):
        return Operand(OperandType.VARIABLE, name, ir_type)

    @staticmethod
    def literal(value, ir_type=None):
        if isinstance(value, bool):
            ir_type = ir_type or "bool"
        elif isinstance(value, int):
            ir_type = ir_type or "int"
        elif isinstance(value, float):
            ir_type = ir_type or "float"
        return Operand(OperandType.LITERAL, value, ir_type)

    @staticmethod
    def label(idx):
        return Operand(OperandType.LABEL, idx)


class OpCode(Enum):
    """IR instruction opcodes."""
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"
    NEG = "neg"
    AND = "and"
    OR = "or"
    NOT = "not"
    XOR = "xor"
    CMP_EQ = "cmp_eq"
    CMP_NE = "cmp_ne"
    CMP_LT = "cmp_lt"
    CMP_LE = "cmp_le"
    CMP_GT = "cmp_gt"
    CMP_GE = "cmp_ge"
    LOAD = "load"
    STORE = "store"
    ALLOCA = "alloca"
    GEP = "gep"
    JUMP = "jump"
    JUMP_IF = "jump_if"
    JUMP_IF_NOT = "jump_if_not"
    LABEL = "label"
    PHI = "phi"
    CALL = "call"
    RETURN = "return"
    PARAM = "param"


class IRInstruction:
    """IR instruction."""

    def __init__(self, op, dest=None, src1=None, src2=None, src3=None, src4=None, label=None, comment=None):
        self.op = op
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.src3 = src3
        self.src4 = src4  # FIXED: added src4 for more arguments
        self.label = label
        self.comment = comment

    def __str__(self):
        if self.op == OpCode.LABEL:
            return f"{self.dest}:"
        if self.op == OpCode.JUMP:
            return f"JUMP {self.src1}"
        if self.op == OpCode.JUMP_IF:
            return f"JUMP_IF {self.dest}, {self.src1}"
        if self.op == OpCode.JUMP_IF_NOT:
            return f"JUMP_IF_NOT {self.dest}, {self.src1}"
        if self.op == OpCode.PARAM:
            return f"PARAM {self.dest}"
        if self.op == OpCode.RETURN:
            return f"RETURN {self.dest}" if self.dest else "RETURN"
        if self.op == OpCode.CALL:
            # FIXED: include all arguments in CALL output
            args_str = []
            if self.src2 is not None:
                args_str.append(str(self.src2))
            if self.src3 is not None:
                args_str.append(str(self.src3))
            if self.src4 is not None:
                args_str.append(str(self.src4))

            if self.dest:
                if args_str:
                    return f"{self.dest} = CALL {self.src1}({', '.join(args_str)})"
                return f"{self.dest} = CALL {self.src1}"
            if args_str:
                return f"CALL {self.src1}({', '.join(args_str)})"
            return f"CALL {self.src1}"
        if self.op == OpCode.STORE:
            return f"STORE [{self.dest}], {self.src1}"
        if self.op == OpCode.LOAD:
            return f"{self.dest} = LOAD [{self.src1}]"

        if self.src2 is not None:
            result = f"{self.dest} = {self.op.value.upper()} {self.src1}, {self.src2}"
            if self.comment:
                result += f"  # {self.comment}"
            return result

        if self.src1 is not None:
            result = f"{self.dest} = {self.op.value.upper()} {self.src1}"
            if self.comment:
                result += f"  # {self.comment}"
            return result

        result = self.op.value.upper()
        if self.comment:
            result += f"  # {self.comment}"
        return result


class IRFunction:
    """Represents a function in IR form."""

    def __init__(self, name, return_type, parameters, blocks, entry_block, next_temp_id=0, next_label_id=0):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.blocks = blocks
        self.entry_block = entry_block
        self.next_temp_id = next_temp_id
        self.next_label_id = next_label_id

    def new_temp(self, ir_type=None):
        self.next_temp_id += 1
        return Operand.temp(self.next_temp_id - 1, ir_type)

    def new_label(self):
        self.next_label_id += 1
        return Operand.label(self.next_label_id - 1)