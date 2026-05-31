from src.lexer.scanner import Scanner
from src.parser.parser import Parser
import sys

print("=== Step 1: Scanning ===", flush=True)
with open('test_array.src', 'r', encoding='utf-8') as f:
    source = f.read()

scanner = Scanner(source)
tokens = scanner.scan_tokens()
print(f"Tokens generated: {len(tokens)}", flush=True)

print("\n=== Step 2: First 20 tokens ===", flush=True)
for i, t in enumerate(tokens[:20]):
    print(f"  {i}: {t.type.name} '{t.lexeme}'", flush=True)

print("\n=== Step 3: Parsing ===", flush=True)
parser = Parser(tokens)
sys.stdout.flush()

try:
    ast = parser.parse()
    print("Parsing successful!", flush=True)
except Exception as e:
    print(f"Parsing failed: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print(f"\n=== AST Structure ===", flush=True)
print(f"Program declarations: {len(ast.declarations)}", flush=True)

for i, decl in enumerate(ast.declarations):
    print(f'\nDeclaration {i+1}: {type(decl).__name__}', flush=True)
    if hasattr(decl, 'name'):
        print(f'  name: {decl.name}', flush=True)
    if hasattr(decl, 'var_type'):
        print(f'  type: {decl.var_type}', flush=True)
    if hasattr(decl, 'dimensions'):
        print(f'  dimensions: {decl.dimensions}', flush=True)
    if hasattr(decl, 'initializer'):
        print(f'  initializer: {decl.initializer}', flush=True)
    if hasattr(decl, 'body'):
        print(f'  has body: {decl.body is not None}', flush=True)
    if hasattr(decl, 'parameters'):
        print(f'  parameters: {len(decl.parameters)}', flush=True)

print("\n=== Done ===", flush=True)
