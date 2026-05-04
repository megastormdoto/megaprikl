import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "\\..\\..")

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator

def test_arithmetic():
    source = 'fn main() int { int x = 2 * 3 + 4; return x; }'
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator(analyzer.get_symbol_table())
    ir_gen.generate(ast)
    ir_text = ir_gen.get_ir_text()
    
    assert "MUL" in ir_text, "MUL instruction not found"
    assert "ADD" in ir_text, "ADD instruction not found"
    assert "RETURN" in ir_text, "RETURN instruction not found"
    print("test_arithmetic: PASSED")

if __name__ == "__main__":
    test_arithmetic()
