import sys
sys.path.append(".")
from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer

source = open("test_functions.src", "r", encoding="utf-8").read()
scanner = Scanner(source)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)
print("=== SYMBOL TABLE ===")
print(analyzer.get_symbol_table().dump())
print("=== ERRORS ===")
for err in analyzer.get_errors():
    print(err)
