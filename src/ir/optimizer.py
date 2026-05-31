"""IR optimization passes: constant propagation, dead code elimination."""

from typing import Dict, List, Set, Optional
from .ir_instructions import IRInstruction, IRFunction, Operand, OpCode, OperandType
from .basic_block import BasicBlock


class IROptimizer:
    """Apply optimizations to IR."""

    def __init__(self):
        self.stats = {
            'constants_propagated': 0,
            'dead_instructions_removed': 0,
            'unreachable_blocks_removed': 0
        }

    def optimize(self, func: IRFunction, passes: List[str] = None) -> IRFunction:
        """Run optimization pipeline."""
        if passes is None:
            passes = ['const_prop', 'dead_code']

        changed = True
        iterations = 0
        while changed and iterations < 10:
            changed = False
            for pass_name in passes:
                if pass_name == 'const_prop':
                    changed = self.constant_propagation(func) or changed
                elif pass_name == 'dead_code':
                    changed = self.dead_code_elimination(func) or changed
            iterations += 1

        return func

    def constant_propagation(self, func: IRFunction) -> bool:
        """Replace variable uses with constant values where known."""
        changed = False
        const_values: Dict[str, int] = {}

        for block in func.blocks:
            new_instructions = []
            for instr in block.instructions:
                if instr.src1 and instr.src1.type == OperandType.TEMP:
                    name = str(instr.src1)
                    if name in const_values:
                        instr.src1 = Operand.literal(const_values[name], "int")
                        self.stats['constants_propagated'] += 1
                        changed = True

                if instr.src2 and instr.src2.type == OperandType.TEMP:
                    name = str(instr.src2)
                    if name in const_values:
                        instr.src2 = Operand.literal(const_values[name], "int")
                        self.stats['constants_propagated'] += 1
                        changed = True

                if instr.op == OpCode.ADD and instr.src1 and instr.src2:
                    if (instr.src1.type == OperandType.LITERAL and
                            instr.src2.type == OperandType.LITERAL and
                            instr.dest and instr.dest.type == OperandType.TEMP):
                        result = instr.src1.value + instr.src2.value
                        const_values[str(instr.dest)] = result
                        changed = True
                elif instr.op == OpCode.MUL and instr.src1 and instr.src2:
                    if (instr.src1.type == OperandType.LITERAL and
                            instr.src2.type == OperandType.LITERAL and
                            instr.dest and instr.dest.type == OperandType.TEMP):
                        result = instr.src1.value * instr.src2.value
                        const_values[str(instr.dest)] = result
                        changed = True
                elif instr.op == OpCode.STORE and instr.dest and instr.src1:
                    if instr.src1.type == OperandType.LITERAL:
                        const_values[str(instr.dest)] = instr.src1.value

                new_instructions.append(instr)
            block.instructions = new_instructions

        return changed

    def dead_code_elimination(self, func: IRFunction) -> bool:
        """Remove unreachable code."""
        changed = False

        if not func.blocks:
            return changed

        # Mark reachable blocks by label string
        reachable_labels = set()
        start_label = str(func.entry_block.label) if func.entry_block else None
        if start_label:
            worklist = [start_label]
        else:
            worklist = []

        while worklist:
            label_str = worklist.pop()
            if label_str in reachable_labels:
                continue
            reachable_labels.add(label_str)

            # Find the block with this label
            for block in func.blocks:
                if block.label and str(block.label) == label_str and block.instructions:
                    last = block.instructions[-1]
                    if last.op == OpCode.JUMP and last.src1:
                        target = str(last.src1)
                        worklist.append(target)
                    elif last.op in [OpCode.JUMP_IF, OpCode.JUMP_IF_NOT] and last.src1:
                        target = str(last.src1)
                        worklist.append(target)

        # Remove unreachable blocks
        unreachable = []
        for block in func.blocks:
            block_label = str(block.label) if block.label else None
            if block_label and block_label not in reachable_labels:
                unreachable.append(block)

        if unreachable:
            for block in unreachable:
                func.blocks.remove(block)
            self.stats['unreachable_blocks_removed'] += len(unreachable)
            changed = True

        return changed

    def get_stats(self) -> dict:
        return self.stats