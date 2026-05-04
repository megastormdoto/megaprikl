import sys
import traceback
sys.path.append(".")

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator

source = open("test_add_only.src", "r", encoding="utf-8").read()
scanner = Scanner(source)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

with open("debug_ir.log", "w", encoding="utf-8") as log:
    log.write("Semantic errors: " + str(len(analyzer.get_errors())) + "\n")
    for err in analyzer.get_errors():
        log.write(str(err) + "\n")
    
    ir_gen = IRGenerator(analyzer.get_symbol_table())
    ir_gen.generate(ast)
    log.write("IR generated successfully:\n")
    log.write(ir_gen.get_ir_text())
