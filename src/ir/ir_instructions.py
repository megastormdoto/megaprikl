
"""IR instruction set and operand types for three-address code."""

from enum import Enum
from dataclasses import dataclass
from typing import Union, List, Optional, Any


class OperandType(Enum):
    """Types of operands in IR instructions."""
    TEMP = "temp"  # Virtual register: t1, t2, ...
    VARIABLE = "var"  # Source variable name: x, y, ...
    LITERAL = "literal"  # Constant: 42, 3.14, true
    LABEL = "label"  # Basic block label: L1, L2, ...


@dataclass
class Operand:
    """An operand in an IR instruction."""
    type: OperandType
    value: Any
    ir_type: Optional[str] = None

    def __str__(self) -> str:
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
    def temp(idx: int, ir_type: str = None) -> '"Operand"':
        return Operand(OperandType.TEMP, idx, ir_type)

    @staticmethod
    def var(name: str, ir_type: str = None) -> '"Operand"':
        return Operand(OperandType.VARIABLE, name, ir_type)

    @staticmethod
    def literal(value: Any, ir_type: str = None) -> '"Operand"':
        if isinstance(value, bool):
            ir_type = ir_type or "bool"
        elif isinstance(value, int):
            ir_type = ir_type or "int"
        elif isinstance(value, float):
            ir_type = ir_type or "float"
        return Operand(OperandType.LITERAL, value, ir_type)

    @staticmethod
    def label(idx: int) -> '"Operand"':
        return Operand(OperandType.LABEL, idx)


class OpCode(Enum):
    """IR instruction opcodes."""
    # Arithmetic
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"
    NEG = "neg"

    # Logical
    AND = "and"
    OR = "or"
    NOT = "not"
    XOR = "xor"

    # Comparison
    CMP_EQ = "cmp_eq"
    CMP_NE = "cmp_ne"
    CMP_LT = "cmp_lt"
    CMP_LE = "cmp_le"
    CMP_GT = "cmp_gt"
    CMP_GE = "cmp_ge"

    # Memory
    LOAD = "load"
    STORE = "store"
    ALLOCA = "alloca"
    GEP = "gep"

    # Control Flow
    JUMP = "jump"
    JUMP_IF = "jump_if"
    JUMP_IF_NOT = "jump_if_not"
    LABEL = "label"
    PHI = "phi"

    # Function
    CALL = "call"
    RETURN = "return"
    PARAM = "param"


@dataclass
class IRInstruction:
    """Base class for all IR instructions."""
    op: OpCode
    dest: Optional[Operand] = None
    src1: Optional[Operand] = None
    src2: Optional[Operand] = None
    src3: Optional[Operand] = None
    label: Optional[Operand] = None
    comment: Optional[str] = None

    def __str__(self) -> str:
        parts = [self.op.value.upper()]

        if self.dest:
            parts.append(str(self.dest))
            parts.append("=")

        if self.op == OpCode.LABEL:
            return f"{self.dest}:"

        if self.op == OpCode.JUMP:
            return f"JUMP {self.src1}"

        if self.op == OpCode.JUMP_IF:
            return f"JUMP_IF {self.dest}, {self.src1}"

        if self.op == OpCode.JUMP_IF_NOT:
            return f"JUMP_IF_NOT {self.dest}, {self.src1}"

        if self.op == OpCode.PHI:
            parts = [f"{self.dest} = PHI"]
            # src1 contains list of (value, block) pairs
            if isinstance(self.src1, list):
                pairs = [f"({v}, {b})" for v, b in self.src1]
                parts.append(", ".join(pairs))
            return " ".join(parts)

        if self.op == OpCode.RETURN:
            if self.dest:
                return f"RETURN {self.dest}"
            return "RETURN"

        if self.op == OpCode.CALL:
            args_str = ", ".join(str(a) for a in self.src_list) if hasattr(self, 'src_list') else ""
            return f"{self.dest} = CALL {self.src1}({args_str})"

        if self.op == OpCode.STORE:
            return f"STORE [{self.dest}], {self.src1}"

        if self.op == OpCode.LOAD:
            return f"{self.dest} = LOAD [{self.src1}]"

        # Binary operations: dest = src1 OP src2
        if self.src2 is not None:
            result = f"{self.dest} = {self.op.value.upper()} {self.src1}, {self.src2}"
            if self.comment:
                result += f"  # {self.comment}"
            return result

        # Unary operations: dest = OP src1
        if self.src1 is not None:
            result = f"{self.dest} = {self.op.value.upper()} {self.src1}"
            if self.comment:
                result += f"  # {self.comment}"
            return result

        result = self.op.value.upper()
        if self.comment:
            result += f"  # {self.comment}"
        return result


@dataclass
class IRFunction:
    """Represents a function in IR form."""
    name: str
    return_type: str
    parameters: List[tuple]  # (name, type)
    blocks: List['BasicBlock']
    entry_block: 'BasicBlock'
    next_temp_id: int = 0
    next_label_id: int = 0

    def new_temp(self, ir_type: str = None) -> Operand:
        """Generate a new temporary variable."""
        self.next_temp_id += 1
        return Operand.temp(self.next_temp_id - 1, ir_type)

    def new_label(self) -> Operand:
        """Generate a new label."""
        self.next_label_id += 1
        return Operand.label(self.next_label_id - 1)

    def get_block_by_label(self, label: Operand) -> Optional['BasicBlock']:
        """Find a basic block by its label operand."""
        for block in self.blocks:
            if block.label and str(block.label) == str(label):
                return block
        return None


