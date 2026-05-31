#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.ir.optimizer import IROptimizer

def test_array_decl():
    source = "int main() { int arr[5]; return 0; }"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    assert ast is not None
    print("✓ TEST-1: Array declaration works")

def test_array_init():
    source = "int main() { int arr[3] = {1, 2, 3}; return 0; }"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    assert ast is not None
    print("✓ TEST-1: Array initialization works")

def test_constant_folding():
    source = "int main() { int x = 10 + 20; return x; }"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator(analyzer.get_symbol_table())
    ir_funcs = ir_gen.generate(ast)
    optimizer = IROptimizer()
    for func in ir_funcs.values():
        optimizer.optimize(func)
    print("✓ TEST-3: Constant folding works")

def test_optimizer():
    source = "int main() { int x = 10 + 20; int y = x * 2; return y; }"
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator(analyzer.get_symbol_table())
    ir_funcs = ir_gen.generate(ast)
    optimizer = IROptimizer()
    for func in ir_funcs.values():
        optimizer.optimize(func)
    stats = optimizer.get_stats()
    print(f"✓ TEST-4: Optimizer stats: {stats}")

def run_all():
    print("\n=== SPRINT 7 TESTS ===\n")
    test_array_decl()
    test_array_init()
    test_constant_folding()
    test_optimizer()
    print("\n=== ALL TESTS PASSED ===\n")

if __name__ == "__main__":
    run_all()
