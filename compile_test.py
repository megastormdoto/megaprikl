from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator

print("Starting compilation...")

with open("test_ifelse.src", "r", encoding="utf-8") as f:
    source = f.read()

scanner = Scanner(source)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)
ir_gen = IRGenerator(analyzer.get_symbol_table())
ir_funcs = ir_gen.generate(ast)

print("\n--- GENERATED IR ---")
for name, func in ir_funcs.items():
    print(f"Function {name}:")
    for block in func.blocks:
        if block.label:
            print(f"  {block.label}:")
        for instr in block.instructions:
            print(f"    {instr}")

x86_gen = X86Generator()
asm = x86_gen.generate(ir_funcs)
print("\n--- GENERATED ASSEMBLY ---")
print(asm)

with open("test.asm", "w") as f:
    f.write(asm)
print("Done. Assembly written to test.asm")
