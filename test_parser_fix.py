from src.lexer.scanner import Scanner
from src.parser.parser import Parser

with open("test_optimize.src", "r") as f:
    source = f.read()

scanner = Scanner(source)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()

print("=== AST after fix ===")
for decl in ast.declarations:
    print(f"Type: {type(decl).__name__}")
    if hasattr(decl, "name"):
        print(f"  name: {decl.name}")
    if hasattr(decl, "return_type"):
        print(f"  return_type: {decl.return_type}")
    if hasattr(decl, "body") and decl.body:
        print(f"  body statements: {len(decl.body.statements)}")
    print()
