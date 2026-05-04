import sys
sys.path.insert(0, ".")

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator

def test_while():
    source = 'fn main() int { int i = 0; while (i < 10) { i = i + 1; } return i; }'
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator(analyzer.get_symbol_table())
    ir_gen.generate(ast)
    ir_text = ir_gen.get_ir_text()
    
    assert "CMP_LT" in ir_text, "CMP_LT instruction not found"
    assert "JUMP_IF" in ir_text, "JUMP_IF instruction not found"
    print("test_while: PASSED")

if __name__ == "__main__":
    test_while()
