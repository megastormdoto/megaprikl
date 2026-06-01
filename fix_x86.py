import re

with open('src/codegen/x86_generator.py', 'r') as f:
    content = f.read()

# Исправляем _gen_store
new_store = '''    def _gen_store(self, instr):
        dest_asm = self._to_asm(instr.dest)
        src_asm = self._to_asm(instr.src1)
        # Загружаем значение в eax если нужно
        if src_asm != 'eax':
            return f"mov eax, {src_asm}\\n    mov {dest_asm}, eax"
        else:
            return f"mov {dest_asm}, eax"'''

# Исправляем _gen_load
new_load = '''    def _gen_load(self, instr):
        src_asm = self._to_asm(instr.src1)
        dest_asm = self._to_asm(instr.dest)
        # Загружаем из памяти в eax
        return f"mov eax, {src_asm}\\n    mov {dest_asm}, eax"'''

# Заменяем
pattern_store = r'    def _gen_store\(self, instr\):.*?(?=\n    def _gen_jump_if)'
pattern_load = r'    def _gen_load\(self, instr\):.*?(?=\n    def _gen_jump_if)'

content = re.sub(pattern_store, new_store, content, flags=re.DOTALL)
content = re.sub(pattern_load, new_load, content, flags=re.DOTALL)

with open('src/codegen/x86_generator.py', 'w') as f:
    f.write(content)

print("Fixed!")
