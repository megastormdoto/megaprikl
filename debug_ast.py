from src.lexer.scanner import Scanner
from src.parser.parser import Parser

with open('test_array.src', 'r', encoding='utf-8') as f:
    source = f.read()

print("=== Step 1: Scanning ===")
scanner = Scanner(source)
tokens = scanner.scan_tokens()
print(f"Tokens generated: {len(tokens)}")

print("\n=== Step 2: Parsing ===")
parser = Parser(tokens)
try:
    ast = parser.parse()
    print("Parsing successful")
except Exception as e:
    print(f"Parsing failed: {e}")
    import traceback
    traceback.print_exc()
    exit()

print(f"\n=== AST Structure ===")
print(f"Program declarations: {len(ast.declarations)}")

for i, decl in enumerate(ast.declarations):
    print(f'\nDeclaration {i+1}: {type(decl).__name__}')
    if hasattr(decl, 'name'):
        print(f'  name: {decl.name}')
    if hasattr(decl, 'var_type'):
        print(f'  type: {decl.var_type}')
    if hasattr(decl, 'dimensions'):
        print(f'  dimensions: {decl.dimensions}')
    if hasattr(decl, 'initializer'):
        print(f'  initializer: {decl.initializer}')
    if hasattr(decl, 'body'):
        print(f'  has body: {decl.body is not None}')
