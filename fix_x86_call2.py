import re

with open('src/codegen/x86_generator.py', 'r') as f:
    content = f.read()

# Исправляем _gen_call
new_call = '''    def _gen_call(self, instr):
        func_name = str(instr.src1)

        if func_name in ["printf", "malloc", "free", "memcpy", "exit"]:
            lines = [f"; call {func_name}"]

            if func_name == "malloc":
                if instr.src2:
                    lines.append(f"mov rdi, {self._to_asm(instr.src2)}")
                lines.append("    xor eax, eax")
                lines.append("    call malloc")
                self.malloc_label_counter += 1
                ok_label = f"malloc_ok_{self.malloc_label_counter}"
                lines.append("    test rax, rax")
                lines.append(f"    jnz {ok_label}")
                lines.append("    mov rdi, malloc_error_msg")
                lines.append("    call printf")
                lines.append("    mov rdi, 1")
                lines.append("    call exit")
                lines.append(f"{ok_label}:")
                if instr.dest:
                    lines.append(f"mov {self._to_asm(instr.dest)}, rax")
                return "\\n    ".join(lines)

            elif func_name == "free":
                if instr.src2:
                    lines.append(f"mov rdi, {self._to_asm(instr.src2)}")
                lines.append("    xor eax, eax")
                lines.append("    call free")
                return "\\n    ".join(lines)

            lines.append("    xor eax, eax")
            lines.append(f"    call {func_name}")
            return "\\n    ".join(lines)

        # ПОЛЬЗОВАТЕЛЬСКИЕ ФУНКЦИИ
        lines = [f"; call {func_name}"]
        
        # Загружаем аргументы в регистры System V AMD64 ABI
        regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
        
        # Аргументы лежат в src2, src3 (больше нет)
        if hasattr(instr, 'src2') and instr.src2:
            lines.append(f"mov rdi, {self._to_asm(instr.src2)}")
        if hasattr(instr, 'src3') and instr.src3:
            lines.append(f"mov rsi, {self._to_asm(instr.src3)}")
        
        lines.append("    xor eax, eax")
        lines.append(f"    call {func_name}")
        
        if instr.dest:
            lines.append(f"mov {self._to_asm(instr.dest)}, rax")
        
        return "\\n    ".join(lines)'''

# Заменяем весь метод
pattern = r'    def _gen_call\(self, instr\):.*?(?=\n    def _gen_compare)'
content = re.sub(pattern, new_call, content, flags=re.DOTALL)

with open('src/codegen/x86_generator.py', 'w') as f:
    f.write(content)

print("Fixed!")
