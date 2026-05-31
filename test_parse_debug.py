import sys
sys.path.insert(0, '.')

from src.lexer.scanner import Scanner
from src.parser.parser import Parser

source = open('test_fold.c').read()
scanner = Scanner(source)
tokens = scanner.scan_tokens()
parser = Parser(tokens)

# ??????? ????????
print("Calling parse_program...")
try:
    ast = parser.parse_program()
    print("parse_program returned:", ast)
except Exception as e:
    print("Exception:", e)
    import traceback
    traceback.print_exc()
