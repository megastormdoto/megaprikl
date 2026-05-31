from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator

with open('demo_factorial.src', 'r') as f:
    source = f.read()

scanner = Scanner(source)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()

analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

ir_gen = IRGenerator(analyzer.get_symbol_table())
ir_funcs = ir_gen.generate(ast)

x86_gen = X86Generator()
asm = x86_gen.generate(ir_funcs)

# Патчим ассемблер: делаем метки уникальными
lines = asm.split('\n')
func_names = list(ir_funcs.keys())
label_map = {}

new_lines = []
for line in lines:
    # Меняем L0: на L0_main: и т.д.
    if line.strip().endswith(':'):
        label = line.strip().rstrip(':')
        for func in func_names:
            if label in ['L0', '_epilogue']:
                new_label = f"{label}_{func}"
                label_map[label] = new_label
                line = line.replace(f"{label}:", f"{new_label}:")
                break
    # Заменяем ссылки на метки
    for old, new in label_map.items():
        if f" {old}" in line or f",{old}" in line or f"jmp {old}" in line:
            line = line.replace(f" {old}", f" {new}")
            line = line.replace(f",{old}", f",{new}")
    new_lines.append(line)

asm = '\n'.join(new_lines)

with open('factorial.asm', 'w') as f:
    f.write(asm)
print("Generated factorial.asm")

# Показываем метки
print("\n=== Checking labels ===")
for line in asm.split('\n')[:50]:
    if ':' in line and 'L0' not in line:
        print(line)
