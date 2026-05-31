import sys
sys.path.insert(0, '.')

print("1. Importing...")
from src.lexer.scanner import Scanner
from src.parser.parser import Parser
print("2. Imports OK")

source = open('test_fold.c').read()
print("3. Source read, length:", len(source))
print("4. Source content:")
print(source)

print("5. Creating scanner...")
scanner = Scanner(source)
tokens = scanner.scan_tokens()
print("6. Tokens count:", len(tokens))

for t in tokens:
    print(f"   {t.type}: {repr(t.lexeme)}")

print("7. Creating parser...")
parser = Parser(tokens)
print("8. Parsing...")
ast = parser.parse()
print("9. Parse result:", ast)
print("10. Parser errors:", parser.errors)
print("11. Done")
