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

# Убираем дубликаты меток
lines = asm.split('\n')
seen = set()
result = []
for line in lines:
    if line.strip().endswith(':'):
        label = line.strip().rstrip(':')
        if label in seen:
            continue
        seen.add(label)
    result.append(line)

asm = '\n'.join(result)

with open('factorial.asm', 'w') as f:
    f.write(asm)
print("Generated factorial.asm")

# Показываем первые 30 строк
print("\n=== First 30 lines === ")
print('\n'.join(asm.split('\n')[:30]))
