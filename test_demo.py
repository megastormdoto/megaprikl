import sys
sys.path.insert(0, '.')

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator

print("1. Starting...")

source = open('demo_factorial.c').read()
print("2. Source read, length:", len(source))

scanner = Scanner(source)
tokens = scanner.scan_tokens()
print("3. Tokens count:", len(tokens))

parser = Parser(tokens)
ast = parser.parse()
print("4. Parse done")

analyzer = SemanticAnalyzer()
analyzer.analyze(ast)
print("5. Semantic done")

ir_gen = IRGenerator(analyzer.get_symbol_table())
ir_funcs = ir_gen.generate(ast)
print("6. IR functions:", list(ir_funcs.keys()))

x86_gen = X86Generator()
asm = x86_gen.generate(ir_funcs)
with open('demo.asm', 'w') as f:
    f.write(asm)
print("7. OK")
