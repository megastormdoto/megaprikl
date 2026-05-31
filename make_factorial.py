import re
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

# Делаем метки уникальными для каждой функции
lines = asm.split('\n')
new_lines = []
in_main = False
in_factorial = False
current_func = None

for line in lines:
    if line.strip() == 'main:':
        current_func = 'main'
        new_lines.append(line)
    elif line.strip() == 'factorial:':
        current_func = 'factorial'
        new_lines.append(line)
    elif line.strip().endswith(':') and current_func:
        if line.strip() in ['L0:', '_epilogue:']:
            new_lines.append(f"{line.strip().rstrip(':')}_{current_func}:")
        else:
            new_lines.append(line)
    else:
        # Заменяем ссылки на метки
        if current_func:
            line = line.replace(' jmp L0', f' jmp L0_{current_func}')
            line = line.replace(' jmp _epilogue', f' jmp _epilogue_{current_func}')
            line = line.replace(' jne L0', f' jne L0_{current_func}')
            line = line.replace(' je L0', f' je L0_{current_func}')
        new_lines.append(line)

asm = '\n'.join(new_lines)

with open('factorial.asm', 'w') as f:
    f.write(asm)
print("Generated factorial.asm")

# Показываем проблемные места
print("\n=== Labels in file ===")
for line in asm.split('\n')[:80]:
    if ':' in line and ('L0' in line or '_epilogue' in line):
        print(line)
