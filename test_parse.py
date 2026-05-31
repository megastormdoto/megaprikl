import sys
sys.path.insert(0, '.')

from src.lexer.scanner import Scanner
from src.parser.parser import Parser

print("1. Starting...")

source = open('demo_factorial.c').read()
print("2. Source read, length:", len(source))

scanner = Scanner(source)
tokens = scanner.scan_tokens()
print("3. Tokens count:", len(tokens))

parser = Parser(tokens)
print("3.5 Before parse")
try:
    ast = parser.parse()
    print("4. Parse done")
except Exception as e:
    print("Exception in parse:", e)
    import traceback
    traceback.print_exc()

print("5. Errors:", parser.errors)
