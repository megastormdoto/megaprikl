import sys
sys.path.insert(0, ".")

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator

def test_if():
    source = 'fn main() int { int x = 10; if (x > 5) { return 1; } else { return 0; } }'
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator(analyzer.get_symbol_table())
    ir_gen.generate(ast)
    ir_text = ir_gen.get_ir_text()
    
    assert "CMP_GT" in ir_text, "CMP_GT instruction not found"
    assert "JUMP_IF" in ir_text, "JUMP_IF instruction not found"
    print("test_if: PASSED")

if __name__ == "__main__":
    test_if()
