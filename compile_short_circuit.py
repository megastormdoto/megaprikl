from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator

print("=== Testing Short-Circuit ===\n")

with open("test_short_circuit.src", "r", encoding="utf-8") as f:
    source = f.read()

print("Source length:", len(source))

scanner = Scanner(source)
tokens = scanner.scan_tokens()
print("Tokens:", len(tokens))

parser = Parser(tokens)
ast = parser.parse()
print("Parsing OK")

analyzer = SemanticAnalyzer()
analyzer.analyze(ast)
print("Semantic OK")

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
