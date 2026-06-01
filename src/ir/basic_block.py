"""Basic block and control flow graph structures."""

from typing import List, Optional, Set, Dict, Any
from enum import Enum

from .ir_instructions import IRInstruction, Operand, OpCode


class BlockType(Enum):
    """Type of basic block for visualization and analysis."""
    ENTRY = "entry"
    EXIT = "exit"
    NORMAL = "normal"


class BasicBlock:
    """A basic block: sequence of instructions with single entry and exit."""
    def __init__(self, label=None):
        self.label = label
        self.instructions = []
        self.predecessors = set()
        self.successors = set()
        self.block_type = BlockType.NORMAL

    def add_instruction(self, instr):
        """Add instruction to the block."""
        self.instructions.append(instr)

    def get_last_instruction(self):
        """Return last instruction (should be control flow)."""
        if self.instructions:
            return self.instructions[-1]
        return None

    def is_terminated(self):
        """Check if block ends with control flow instruction."""
        last = self.get_last_instruction()
        if last:
            return last.op in [
                OpCode.JUMP, OpCode.JUMP_IF, OpCode.JUMP_IF_NOT,
                OpCode.RETURN, OpCode.LABEL
            ]
        return False

    def add_successor(self, block):
        """Add control flow successor."""
        self.successors.add(block)
        block.predecessors.add(self)

    def __str__(self):
        label_str = str(self.label) if self.label else "unnamed"
        result = [f"\n{label_str}:"]
        for instr in self.instructions:
            result.append(f"    {instr}")
        return "\n".join(result)

    def get_instructions_text(self):
        """Return instructions as text lines (without block label)."""
        return [str(instr) for instr in self.instructions]


class ControlFlowGraph:
    """Control Flow Graph containing all basic blocks of a function."""
    def __init__(self):
        self.entry_block = None
        self.exit_blocks = []
        self.all_blocks = []

    def add_block(self, block):
        """Add block to CFG."""
        self.all_blocks.append(block)

    def set_entry(self, block):
        """Set entry block."""
        self.entry_block = block
        block.block_type = BlockType.ENTRY
        self.add_block(block)

    def add_exit(self, block):
        """Add exit block."""
        self.exit_blocks.append(block)
        block.block_type = BlockType.EXIT

    def get_block_by_label(self, label):
        """Find block by label."""
        for block in self.all_blocks:
            if block.label and str(block.label) == str(label):
                return block
        return None

    def validate(self):
        """Validate CFG properties. Returns list of errors."""
        errors = []

        for block in self.all_blocks:
            if block.block_type != BlockType.EXIT and not block.is_terminated():
                errors.append(f"Block {block.label} does not end with control flow")

            for succ in block.successors:
                if succ not in self.all_blocks:
                    errors.append(f"Block {block.label} has invalid successor {succ.label}")

        return errors

    def dump_dot(self):
        """Generate Graphviz DOT format for visualization."""
        lines = ["digraph CFG {"]
        lines.append('  node [shape=box, style=filled, fillcolor=lightblue];')

        for block in self.all_blocks:
            label = str(block.label) if block.label else f"block{id(block)}"
            instr_text = "\\n".join(block.get_instructions_text()[:3])
            if len(block.instructions) > 3:
                instr_text += "\\n..."
            fillcolor = "lightgreen" if block.block_type == BlockType.ENTRY else "lightcoral" if block.block_type == BlockType.EXIT else "lightblue"
            lines.append(f'  "{label}" [label="{label}\\n{instr_text}", fillcolor={fillcolor}];')

        for block in self.all_blocks:
            src_label = str(block.label) if block.label else f"block{id(block)}"
            for succ in block.successors:
                dst_label = str(succ.label) if succ.label else f"block{id(succ)}"
                lines.append(f'  "{src_label}" -> "{dst_label}";')

        lines.append("}")
        return "\n".join(lines)