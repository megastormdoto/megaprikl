"""IR Generator - traverses decorated AST and produces Intermediate Representation."""
from typing import Dict, List, Optional, Any
from src.parser.ast import (
    ProgramNode, FunctionDeclNode, VarDeclNode, StructDeclNode,
    BlockNode, IfStmtNode, WhileStmtNode, ForStmtNode, ReturnStmtNode,
    AssignmentNode, BinaryExprNode, UnaryExprNode, CallNode,
    IdentifierNode, LiteralNode, ExprStmtNode, ParameterNode,
    ArrayDeclNode, ArrayAccessNode
)
from src.semantic.symbol_table import SymbolTable, Symbol
from src.semantic.type_system import Type, BaseType
from .ir_instructions import (
    IRInstruction, IRFunction, Operand, OpCode, OperandType
)
from .basic_block import BasicBlock, ControlFlowGraph, BlockType


class IRGenerator:
    """Generates IR from decorated AST."""

    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.functions: Dict[str, IRFunction] = {}
        self.current_function: Optional[IRFunction] = None
        self.current_block: Optional[BasicBlock] = None
        self.var_to_temp: Dict[str, Operand] = {}
        self.temp_counter = 0

    def generate(self, ast: ProgramNode) -> Dict[str, IRFunction]:
        """Generate IR for entire program."""
        for decl in ast.declarations:
            if isinstance(decl, FunctionDeclNode):
                self._generate_function(decl)
        return self.functions

    def _generate_function(self, node: FunctionDeclNode) -> IRFunction:
        """Generate IR for a single function."""
        if node.body is None:
            ir_func = IRFunction(
                name=node.name,
                return_type=node.return_type,
                parameters=[(p.name, p.param_type) for p in node.parameters],
                blocks=[],
                entry_block=None,
                next_temp_id=0,
                next_label_id=0
            )
            self.functions[node.name] = ir_func
            return ir_func

        ir_func = IRFunction(
            name=node.name,
            return_type=node.return_type,
            parameters=[(p.name, p.param_type) for p in node.parameters],
            blocks=[],
            entry_block=None,
            next_temp_id=0,
            next_label_id=0
        )
        self.current_function = ir_func
        self.var_to_temp = {}

        entry_block = BasicBlock(label=ir_func.new_label())
        self.current_block = entry_block
        ir_func.blocks.append(entry_block)

        # Map parameters to temporaries
        for i, (param_name, param_type) in enumerate(ir_func.parameters):
            temp = ir_func.new_temp(param_type)
            self.var_to_temp[param_name] = temp

            # Store parameter from register to temporary
            # rdi for first, rsi for second
            if i == 0:
                param_reg = Operand.var("rdi", param_type)
            elif i == 1:
                param_reg = Operand.var("rsi", param_type)
            else:
                param_reg = Operand.literal(0, param_type)

            store_instr = IRInstruction(
                op=OpCode.STORE,
                dest=temp,
                src1=param_reg,
                comment=f"store parameter {param_name} from register"
            )
            self.current_block.add_instruction(store_instr)

        self._generate_block(node.body)

        # Add implicit return if needed
        if self.current_block and self.current_block.instructions:
            last_instr = self.current_block.instructions[-1]
            if last_instr.op != OpCode.RETURN:
                if node.return_type == "void":
                    ret_instr = IRInstruction(op=OpCode.RETURN)
                    self.current_block.add_instruction(ret_instr)
                else:
                    zero = Operand.literal(0, "int")
                    ret_instr = IRInstruction(op=OpCode.RETURN, dest=zero)
                    self.current_block.add_instruction(ret_instr)

        ir_func.entry_block = entry_block
        self.functions[node.name] = ir_func
        self.current_function = None

        return ir_func

    def _generate_block(self, node: BlockNode):
        """Generate IR for a block statement."""
        if node is None:
            return
        for stmt in node.statements:
            self._generate_statement(stmt)

    def _generate_statement(self, node):
        """Dispatch to appropriate statement handler."""
        if node is None:
            return
        if isinstance(node, VarDeclNode):
            self._generate_var_decl(node)
        elif isinstance(node, AssignmentNode):
            self._generate_assignment(node)
        elif isinstance(node, IfStmtNode):
            self._generate_if(node)
        elif isinstance(node, WhileStmtNode):
            self._generate_while(node)
        elif isinstance(node, ForStmtNode):
            self._generate_for(node)
        elif isinstance(node, ReturnStmtNode):
            self._generate_return(node)
        elif isinstance(node, BlockNode):
            self._generate_block(node)
        elif isinstance(node, ExprStmtNode):
            if node.expression:
                self._generate_expression(node.expression)
        elif isinstance(node, CallNode):
            self._generate_call(node)
        elif isinstance(node, ArrayDeclNode):
            self._generate_array_decl(node)

    def _generate_var_decl(self, node: VarDeclNode):
        """Generate IR for variable declaration."""
        temp = self.current_function.new_temp(node.var_type)
        self.var_to_temp[node.name] = temp

        if node.initializer:
            init_temp = self._generate_expression(node.initializer)
            store_instr = IRInstruction(
                op=OpCode.STORE,
                dest=temp,
                src1=init_temp,
                comment=f"init {node.name}"
            )
            self.current_block.add_instruction(store_instr)

    def _generate_assignment(self, node: AssignmentNode):
        """Generate IR for assignment - handles array elements."""
        if isinstance(node.target, ArrayAccessNode):
            self._generate_array_assignment(node.target, node.value)
            return

        if node.target in self.var_to_temp:
            target_temp = self.var_to_temp[node.target]
        else:
            target_temp = self.current_function.new_temp("int")
            self.var_to_temp[node.target] = target_temp

        rhs_temp = self._generate_expression(node.value)

        store_instr = IRInstruction(
            op=OpCode.STORE,
            dest=target_temp,
            src1=rhs_temp,
            comment=f"assign {node.target}"
        )
        self.current_block.add_instruction(store_instr)

    def _generate_array_assignment(self, array_access: ArrayAccessNode, value_node):
        """Generate IR for array element assignment."""
        if array_access.array in self.var_to_temp:
            arr_ptr = self.var_to_temp[array_access.array]

            load_arr = IRInstruction(
                op=OpCode.LOAD,
                dest=self.current_function.new_temp("pointer"),
                src1=arr_ptr,
                comment=f"load array {array_access.array} pointer"
            )
            self.current_block.add_instruction(load_arr)

            index_temp = self._generate_expression(array_access.index)
            offset = IRInstruction(
                op=OpCode.MUL,
                dest=self.current_function.new_temp("int"),
                src1=index_temp,
                src2=Operand.literal(4, "int"),
                comment=f"byte offset"
            )
            self.current_block.add_instruction(offset)

            # ВАЖНО: адрес элемента помечаем как "address", чтобы x86_generator
            # знал, что его нужно разыменовывать при STORE
            addr = self.current_function.new_temp("address")
            gep = IRInstruction(
                op=OpCode.ADD,
                dest=addr,
                src1=load_arr.dest,
                src2=offset.dest,
                comment=f"address of {array_access.array}[{index_temp}]"
            )
            self.current_block.add_instruction(gep)

            rhs_temp = self._generate_expression(value_node)

            store_elem = IRInstruction(
                op=OpCode.STORE,
                dest=gep.dest,
                src1=rhs_temp,
                comment=f"store element"
            )
            self.current_block.add_instruction(store_elem)

    def _generate_expression(self, node) -> Operand:
        """Generate IR for expression and return result temp."""
        if node is None:
            return Operand.literal(0, "int")
        if isinstance(node, LiteralNode):
            return self._generate_literal(node)
        elif isinstance(node, IdentifierNode):
            return self._generate_identifier(node)
        elif isinstance(node, BinaryExprNode):
            return self._generate_binary_op(node)
        elif isinstance(node, UnaryExprNode):
            return self._generate_unary_op(node)
        elif isinstance(node, CallNode):
            return self._generate_call(node)
        elif isinstance(node, ArrayAccessNode):
            return self._generate_array_access(node)
        else:
            return Operand.literal(0, "int")

    def _generate_literal(self, node: LiteralNode) -> Operand:
        """Generate IR for literal."""
        if node.literal_type == "int":
            return Operand.literal(int(node.value), "int")
        elif node.literal_type == "float":
            return Operand.literal(float(node.value), "float")
        elif node.literal_type == "bool":
            return Operand.literal(node.value == "true", "bool")
        elif node.literal_type == "string":
            return Operand.var(str(node.value), "string")
        return Operand.literal(0, "int")

    def _generate_identifier(self, node: IdentifierNode) -> Operand:
        """Generate IR for identifier (load variable)."""
        if node.name in self.var_to_temp:
            temp = self.var_to_temp[node.name]
            load_instr = IRInstruction(
                op=OpCode.LOAD,
                dest=self.current_function.new_temp("int"),
                src1=temp,
                comment=f"load {node.name}"
            )
            self.current_block.add_instruction(load_instr)
            return load_instr.dest
        else:
            return self.current_function.new_temp("int")

    def _generate_binary_op(self, node: BinaryExprNode) -> Operand:
        """Generate IR for binary operation."""
        from src.parser.ast import LiteralNode

        left_is_const = isinstance(node.left, LiteralNode)
        right_is_const = isinstance(node.right, LiteralNode)

        if left_is_const and right_is_const:
            left_val = node.left.value
            right_val = node.right.value
            op = node.operator

            try:
                if op == '+':
                    result = left_val + right_val
                elif op == '-':
                    result = left_val - right_val
                elif op == '*':
                    result = left_val * right_val
                elif op == '/':
                    if right_val == 0:
                        return None
                    result = left_val // right_val
                elif op == '%':
                    if right_val == 0:
                        return None
                    result = left_val % right_val
                else:
                    pass
                return Operand.literal(result, "int")
            except:
                pass

        if node.operator == '&&':
            return self._generate_logical_and(node)
        elif node.operator == '||':
            return self._generate_logical_or(node)

        left_temp = self._generate_expression(node.left)
        right_temp = self._generate_expression(node.right)

        op_map = {
            '+': OpCode.ADD,
            '-': OpCode.SUB,
            '*': OpCode.MUL,
            '/': OpCode.DIV,
            '%': OpCode.MOD,
            '==': OpCode.CMP_EQ,
            '!=': OpCode.CMP_NE,
            '<': OpCode.CMP_LT,
            '<=': OpCode.CMP_LE,
            '>': OpCode.CMP_GT,
            '>=': OpCode.CMP_GE,
        }

        opcode = op_map.get(node.operator, OpCode.ADD)
        result_temp = self.current_function.new_temp("int")

        instr = IRInstruction(
            op=opcode,
            dest=result_temp,
            src1=left_temp,
            src2=right_temp,
            comment=f"{left_temp} {node.operator} {right_temp}"
        )
        self.current_block.add_instruction(instr)

        return result_temp

    def _generate_logical_and(self, node: BinaryExprNode) -> Operand:
        """Generate short-circuit AND."""
        result = self.current_function.new_temp("bool")

        false_label = self.current_function.new_label()
        end_label = self.current_function.new_label()

        left_val = self._generate_expression(node.left)

        jump_if_false = IRInstruction(
            op=OpCode.JUMP_IF_NOT,
            dest=left_val,
            src1=false_label
        )
        self.current_block.add_instruction(jump_if_false)

        right_val = self._generate_expression(node.right)

        jump_if_false2 = IRInstruction(
            op=OpCode.JUMP_IF_NOT,
            dest=right_val,
            src1=false_label
        )
        self.current_block.add_instruction(jump_if_false2)

        store_true = IRInstruction(
            op=OpCode.STORE,
            dest=result,
            src1=Operand.literal(1, "bool")
        )
        self.current_block.add_instruction(store_true)

        jump_to_end = IRInstruction(
            op=OpCode.JUMP,
            src1=end_label
        )
        self.current_block.add_instruction(jump_to_end)

        false_block = BasicBlock(label=false_label)
        self.current_function.blocks.append(false_block)
        self.current_block = false_block

        store_false = IRInstruction(
            op=OpCode.STORE,
            dest=result,
            src1=Operand.literal(0, "bool")
        )
        self.current_block.add_instruction(store_false)

        end_block = BasicBlock(label=end_label)
        self.current_function.blocks.append(end_block)
        self.current_block = end_block

        return result

    def _generate_logical_or(self, node: BinaryExprNode) -> Operand:
        """Generate short-circuit OR."""
        result = self.current_function.new_temp("bool")

        true_label = self.current_function.new_label()
        end_label = self.current_function.new_label()

        left_val = self._generate_expression(node.left)

        jump_if_true = IRInstruction(
            op=OpCode.JUMP_IF,
            dest=left_val,
            src1=true_label
        )
        self.current_block.add_instruction(jump_if_true)

        right_val = self._generate_expression(node.right)

        jump_if_true2 = IRInstruction(
            op=OpCode.JUMP_IF,
            dest=right_val,
            src1=true_label
        )
        self.current_block.add_instruction(jump_if_true2)

        store_false = IRInstruction(
            op=OpCode.STORE,
            dest=result,
            src1=Operand.literal(0, "bool")
        )
        self.current_block.add_instruction(store_false)

        jump_to_end = IRInstruction(
            op=OpCode.JUMP,
            src1=end_label
        )
        self.current_block.add_instruction(jump_to_end)

        true_block = BasicBlock(label=true_label)
        self.current_function.blocks.append(true_block)
        self.current_block = true_block

        store_true = IRInstruction(
            op=OpCode.STORE,
            dest=result,
            src1=Operand.literal(1, "bool")
        )
        self.current_block.add_instruction(store_true)

        end_block = BasicBlock(label=end_label)
        self.current_function.blocks.append(end_block)
        self.current_block = end_block

        return result

    def _generate_unary_op(self, node: UnaryExprNode) -> Operand:
        """Generate IR for unary operation."""
        operand_temp = self._generate_expression(node.operand)

        if node.operator == '-':
            result_temp = self.current_function.new_temp("int")
            instr = IRInstruction(
                op=OpCode.NEG,
                dest=result_temp,
                src1=operand_temp,
                comment=f"-{operand_temp}"
            )
            self.current_block.add_instruction(instr)
            return result_temp
        elif node.operator == '!':
            result_temp = self.current_function.new_temp("bool")
            instr = IRInstruction(
                op=OpCode.NOT,
                dest=result_temp,
                src1=operand_temp,
                comment=f"!{operand_temp}"
            )
            self.current_block.add_instruction(instr)
            return result_temp
        else:
            return operand_temp

    def _generate_return(self, node: ReturnStmtNode):
        """Generate IR for return statement."""
        if node.value:
            value_temp = self._generate_expression(node.value)
            ret_instr = IRInstruction(op=OpCode.RETURN, dest=value_temp)
        else:
            ret_instr = IRInstruction(op=OpCode.RETURN)

        self.current_block.add_instruction(ret_instr)

    def _generate_if(self, node: IfStmtNode):
        """Generate IR for if statement."""
        cond_temp = self._generate_expression(node.condition)

        then_label = self.current_function.new_label()
        else_label = self.current_function.new_label()
        merge_label = self.current_function.new_label()

        jump_if_instr = IRInstruction(
            op=OpCode.JUMP_IF,
            dest=cond_temp,
            src1=then_label,
            comment="if condition true"
        )
        self.current_block.add_instruction(jump_if_instr)

        jump_to_else = IRInstruction(
            op=OpCode.JUMP,
            src1=else_label
        )
        self.current_block.add_instruction(jump_to_else)

        then_block = BasicBlock(label=then_label)
        self.current_function.blocks.append(then_block)
        self.current_block = then_block
        self._generate_statement(node.then_branch)
        if not self.current_block.is_terminated():
            jump_to_merge = IRInstruction(op=OpCode.JUMP, src1=merge_label)
            self.current_block.add_instruction(jump_to_merge)

        else_block = BasicBlock(label=else_label)
        self.current_function.blocks.append(else_block)
        self.current_block = else_block
        if node.else_branch:
            self._generate_statement(node.else_branch)
        if not self.current_block.is_terminated():
            jump_to_merge = IRInstruction(op=OpCode.JUMP, src1=merge_label)
            self.current_block.add_instruction(jump_to_merge)

        merge_block = BasicBlock(label=merge_label)
        self.current_function.blocks.append(merge_block)
        self.current_block = merge_block

    def _generate_while(self, node: WhileStmtNode):
        """Generate IR for while loop."""
        header_label = self.current_function.new_label()
        body_label = self.current_function.new_label()
        exit_label = self.current_function.new_label()

        jump_to_header = IRInstruction(op=OpCode.JUMP, src1=header_label)
        self.current_block.add_instruction(jump_to_header)

        header_block = BasicBlock(label=header_label)
        self.current_function.blocks.append(header_block)
        self.current_block = header_block

        cond_temp = self._generate_expression(node.condition)

        jump_if_instr = IRInstruction(
            op=OpCode.JUMP_IF,
            dest=cond_temp,
            src1=body_label,
            comment="while condition true"
        )
        self.current_block.add_instruction(jump_if_instr)

        jump_to_exit = IRInstruction(op=OpCode.JUMP, src1=exit_label)
        self.current_block.add_instruction(jump_to_exit)

        body_block = BasicBlock(label=body_label)
        self.current_function.blocks.append(body_block)
        self.current_block = body_block

        self._generate_statement(node.body)

        if not self.current_block.is_terminated():
            jump_back = IRInstruction(op=OpCode.JUMP, src1=header_label)
            self.current_block.add_instruction(jump_back)

        exit_block = BasicBlock(label=exit_label)
        self.current_function.blocks.append(exit_block)
        self.current_block = exit_block

    def _generate_for(self, node: ForStmtNode):
        """Generate IR for for loop."""
        if node.init:
            self._generate_statement(node.init)

        header_label = self.current_function.new_label()
        body_label = self.current_function.new_label()
        increment_label = self.current_function.new_label()
        exit_label = self.current_function.new_label()

        jump_to_header = IRInstruction(op=OpCode.JUMP, src1=header_label)
        self.current_block.add_instruction(jump_to_header)

        header_block = BasicBlock(label=header_label)
        self.current_function.blocks.append(header_block)
        self.current_block = header_block

        if node.condition:
            cond_temp = self._generate_expression(node.condition)
            jump_if_instr = IRInstruction(
                op=OpCode.JUMP_IF,
                dest=cond_temp,
                src1=body_label,
                comment="for condition true"
            )
            self.current_block.add_instruction(jump_if_instr)
        else:
            jump_if_instr = IRInstruction(op=OpCode.JUMP, src1=body_label)
            self.current_block.add_instruction(jump_if_instr)

        jump_to_exit = IRInstruction(op=OpCode.JUMP, src1=exit_label)
        self.current_block.add_instruction(jump_to_exit)

        body_block = BasicBlock(label=body_label)
        self.current_function.blocks.append(body_block)
        self.current_block = body_block

        self._generate_statement(node.body)

        if not self.current_block.is_terminated():
            jump_to_inc = IRInstruction(op=OpCode.JUMP, src1=increment_label)
            self.current_block.add_instruction(jump_to_inc)

        increment_block = BasicBlock(label=increment_label)
        self.current_function.blocks.append(increment_block)
        self.current_block = increment_block

        if node.update:
            self._generate_expression(node.update)

        jump_back = IRInstruction(op=OpCode.JUMP, src1=header_label)
        self.current_block.add_instruction(jump_back)

        exit_block = BasicBlock(label=exit_label)
        self.current_function.blocks.append(exit_block)
        self.current_block = exit_block

    def _generate_call(self, node: CallNode) -> Operand:
        """Generate IR for function call."""
        result_temp = self.current_function.new_temp("int")

        # Generate all arguments
        arg_temps = []
        for arg in node.arguments:
            arg_temp = self._generate_expression(arg)
            arg_temps.append(arg_temp)

        # Create call instruction with arguments in src2, src3, etc.
        if len(arg_temps) >= 1:
            call_instr = IRInstruction(
                op=OpCode.CALL,
                dest=result_temp,
                src1=Operand.var(node.callee, "function"),
                src2=arg_temps[0],
                comment=f"call {node.callee} with {len(arg_temps)} args"
            )
            if len(arg_temps) >= 2:
                call_instr.src3 = arg_temps[1]
        else:
            call_instr = IRInstruction(
                op=OpCode.CALL,
                dest=result_temp,
                src1=Operand.var(node.callee, "function"),
                comment=f"call {node.callee}"
            )

        self.current_block.add_instruction(call_instr)
        return result_temp

    def _generate_array_decl(self, node):
        """Generate IR for array declaration."""
        size_temp = self._generate_expression(node.size)
        mul_instr = IRInstruction(
            op=OpCode.MUL,
            dest=self.current_function.new_temp("int"),
            src1=size_temp,
            src2=Operand.literal(4, "int"),
            comment=f"array size in bytes"
        )
        self.current_block.add_instruction(mul_instr)
        bytes_count = mul_instr.dest

        call_malloc = IRInstruction(
            op=OpCode.CALL,
            dest=self.current_function.new_temp("pointer"),
            src1=Operand.var("malloc", "function"),
            src2=bytes_count,
            comment=f"malloc for array {node.name}"
        )
        self.current_block.add_instruction(call_malloc)

        arr_ptr = self.current_function.new_temp("pointer")
        store_ptr = IRInstruction(
            op=OpCode.STORE,
            dest=arr_ptr,
            src1=call_malloc.dest,
            comment=f"store array pointer"
        )
        self.current_block.add_instruction(store_ptr)
        self.var_to_temp[node.name] = arr_ptr

        size_var = self.current_function.new_temp("int")
        store_size = IRInstruction(
            op=OpCode.STORE,
            dest=size_var,
            src1=size_temp,
            comment=f"store array size"
        )
        self.current_block.add_instruction(store_size)
        self.var_to_temp[f"{node.name}_size"] = size_var

        if node.initializer and isinstance(node.initializer, list):
            for i, init_expr in enumerate(node.initializer):
                val_temp = self._generate_expression(init_expr)

                load_arr = IRInstruction(
                    op=OpCode.LOAD,
                    dest=self.current_function.new_temp("pointer"),
                    src1=arr_ptr,
                    comment=f"load array pointer"
                )
                self.current_block.add_instruction(load_arr)

                offset = IRInstruction(
                    op=OpCode.MUL,
                    dest=self.current_function.new_temp("int"),
                    src1=Operand.literal(i, "int"),
                    src2=Operand.literal(4, "int"),
                    comment=f"offset"
                )
                self.current_block.add_instruction(offset)

                # ВАЖНО: адрес элемента помечаем как "address", чтобы x86_generator
                # разыменовывал его при STORE
                addr = self.current_function.new_temp("address")
                gep = IRInstruction(
                    op=OpCode.ADD,
                    dest=addr,
                    src1=load_arr.dest,
                    src2=offset.dest,
                    comment=f"address of {node.name}[{i}]"
                )
                self.current_block.add_instruction(gep)

                store_elem = IRInstruction(
                    op=OpCode.STORE,
                    dest=gep.dest,
                    src1=val_temp,
                    comment=f"store element"
                )
                self.current_block.add_instruction(store_elem)

    def _generate_array_access(self, node):
        """Generate IR for array access."""
        if node.array in self.var_to_temp:
            arr_ptr = self.var_to_temp[node.array]

            # Load array pointer
            load_arr = IRInstruction(
                op=OpCode.LOAD,
                dest=self.current_function.new_temp("pointer"),
                src1=arr_ptr,
                comment=f"load array pointer for {node.array}"
            )
            self.current_block.add_instruction(load_arr)

            # Compute index
            index_temp = self._generate_expression(node.index)

            # Compute offset (index * 4)
            offset = IRInstruction(
                op=OpCode.MUL,
                dest=self.current_function.new_temp("int"),
                src1=index_temp,
                src2=Operand.literal(4, "int"),
                comment=f"byte offset for index {index_temp}"
            )
            self.current_block.add_instruction(offset)

            # ВАЖНО: адрес элемента помечаем как "address", чтобы x86_generator
            # разыменовывал его при LOAD
            addr = self.current_function.new_temp("address")
            gep = IRInstruction(
                op=OpCode.ADD,
                dest=addr,
                src1=load_arr.dest,
                src2=offset.dest,
                comment=f"address of {node.array}[{index_temp}]"
            )
            self.current_block.add_instruction(gep)

            # Load value from address
            load_val = IRInstruction(
                op=OpCode.LOAD,
                dest=self.current_function.new_temp("int"),
                src1=addr,
                comment=f"load {node.array}[{index_temp}]"
            )
            self.current_block.add_instruction(load_val)
            return load_val.dest

        return self.current_function.new_temp("int")

    def _get_type_name(self, type_obj) -> str:
        """Convert type object to string name."""
        if hasattr(type_obj, 'kind'):
            if type_obj.kind == BaseType.INT:
                return "int"
            elif type_obj.kind == BaseType.FLOAT:
                return "float"
            elif type_obj.kind == BaseType.BOOL:
                return "bool"
            elif type_obj.kind == BaseType.VOID:
                return "void"
            elif type_obj.kind == BaseType.STRING:
                return "string"
        return "int"

    def get_ir_text(self, func_name: str = None) -> str:
        """Get human-readable IR text."""
        lines = ["# Generated IR", "# " + "= " * 50]

        if func_name:
            funcs = [(func_name, self.functions[func_name])]
        else:
            funcs = self.functions.items()

        for name, func in funcs:
            param_str = ', '.join([f'{p[0]}: {p[1]}' for p in func.parameters])
            lines.append(f"\nfunction {name}: {func.return_type} ({param_str})")

            sorted_blocks = sorted(func.blocks, key=lambda b: str(b.label) if b.label else "")
            for block in sorted_blocks:
                if block.label:
                    lines.append(f"\n{block.label}:")
                for instr in block.instructions:
                    lines.append(f"    {instr}")

        return "\n".join(lines)

    def get_all_ir(self) -> Dict[str, IRFunction]:
        return self.functions

    def generate_array_copy(self, dest_arr: str, src_arr: str, size: Operand):
        """Generate memcpy."""
        dest_ptr = self.var_to_temp.get(dest_arr)
        src_ptr = self.var_to_temp.get(src_arr)

        if not dest_ptr or not src_ptr:
            return

        load_dest = IRInstruction(
            op=OpCode.LOAD,
            dest=self.current_function.new_temp("pointer"),
            src1=dest_ptr
        )
        self.current_block.add_instruction(load_dest)

        load_src = IRInstruction(
            op=OpCode.LOAD,
            dest=self.current_function.new_temp("pointer"),
            src1=src_ptr
        )
        self.current_block.add_instruction(load_src)

        bytes_count = self.current_function.new_temp("int")
        mul = IRInstruction(
            op=OpCode.MUL,
            dest=bytes_count,
            src1=size,
            src2=Operand.literal(4, "int")
        )
        self.current_block.add_instruction(mul)

        call_memcpy = IRInstruction(
            op=OpCode.CALL,
            dest=None,
            src1=Operand.var("memcpy", "function"),
            src2=load_dest.dest,
            src3=load_src.dest,
            src4=bytes_count
        )
        self.current_block.add_instruction(call_memcpy)