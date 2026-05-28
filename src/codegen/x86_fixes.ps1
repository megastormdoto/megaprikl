    def _gen_store(self, instr: IRInstruction) -> str:
        """Generate store instruction."""
        dest_asm = self._operand_to_asm(instr.dest, for_store=True)
        src_asm = self._operand_to_asm(instr.src1, for_load=True)
        
        # Cannot move from memory to memory directly
        if src_asm.startswith('[') and dest_asm.startswith('['):
            # Load to eax first, then store
            return f"mov eax, {src_asm}\n    mov {dest_asm}, eax"
        else:
            return f"mov {dest_asm}, {src_asm}"
    
    def _generate_function(self, func: IRFunction) -> str:
        """Generate assembly for a single function."""
        self.current_function = func
        self.stack_manager = StackFrameManager()
        self.temp_locations = {}
        
        lines = []
        lines.append(f"\n{func.name}:")
        lines.append("    ; Prologue")
        lines.append("    push rbp")
        lines.append("    mov rbp, rsp")
        lines.append("    sub rsp, 64")
        lines.append("")
        
        # Generate code for each block
        for block in func.blocks:
            if block.label:
                label_str = str(block.label).replace(':', '')
                lines.append(f"{label_str}:")
            for instr in block.instructions:
                asm = self._generate_instruction(instr)
                if asm:
                    # Indent instructions
                    for line in asm.split('\n'):
                        lines.append(f"    {line}")
        
        # Add epilogue label and return
        lines.append(".epilogue:")
        lines.append("    mov rsp, rbp")
        lines.append("    pop rbp")
        lines.append("    ret")
        
        return "\n".join(lines)
    
    def _gen_return(self, instr: IRInstruction) -> str:
        """Generate return instruction."""
        if instr.dest:
            dest_asm = self._operand_to_asm(instr.dest, for_load=True)
            return f"mov eax, {dest_asm}\n    jmp .epilogue"
        return "jmp .epilogue"
