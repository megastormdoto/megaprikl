# sprint6_demo.py - ???????????????? ?????? ??? Sprint 6
import sys
import os

# ????????? ???? ? ???????
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator

def compile_and_show(filename):
    """??????????? ???? ? ?????????? IR ? Assembly"""
    print(f"\n{'='*70}")
    print(f"File: {filename}")
    print(f"{'='*70}")
    
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    
    print(f"\nSource code:")
    print(f"{'-'*50}")
    print(source)
    print(f"{'-'*50}")
    
    # ??????????
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    ir_gen = IRGenerator(analyzer.get_symbol_table())
    ir_funcs = ir_gen.generate(ast)
    
    # ?????????? IR
    print(f"\nIntermediate Representation (IR):")
    print(f"{'-'*50}")
    for name, func in ir_funcs.items():
        print(f"Function {name}:")
        for block in func.blocks:
            if block.label:
                print(f"  {block.label}:")
            for instr in block.instructions:
                print(f"    {instr}")
    print(f"{'-'*50}")
    
    # ?????????? Assembly
    x86_gen = X86Generator()
    asm = x86_gen.generate(ir_funcs)
    print(f"\nGenerated Assembly (x86-64):")
    print(f"{'-'*50}")
    # ?????????? ?????? ???????? ????? (?????? 30 ?????)
    asm_lines = asm.split('\n')
    for line in asm_lines[:30]:
        print(line)
    if len(asm_lines) > 30:
        print(f"... ({len(asm_lines)-30} more lines)")
    print(f"{'-'*50}")

def main():
    print(f"\n{'='*60}")
    print(f"    SPRINT 6: CONTROL FLOW & SHORT-CIRCUIT EVALUATION")
    print(f"{'='*60}")
    
    demos = [
        ("demo1_ifelse.c", "If-Else Statement"),
        ("demo2_while.c", "While Loop"),
        ("demo3_for.c", "For Loop"),
        ("demo4_shortcircuit.c", "Short-Circuit AND (&&)"),
        ("demo5_nested.c", "Nested If Statements"),
        ("demo6_complex.c", "Complex Logical Expression"),
    ]
    
    for filename, description in demos:
        if os.path.exists(filename):
            print(f"\n{'='*60}")
            print(f"Demo: {description}")
            compile_and_show(filename)
            input("\nPress Enter to continue...")
        else:
            print(f"\nFile {filename} not found!")
    
    print(f"\n{'='*60}")
    print(f"    DEMONSTRATION COMPLETE")
    print(f"{'='*60}")
    print(f"\nSPRINT 6 SUMMARY:")
    print(f"   - If-Else Statement Translation")
    print(f"   - While Loop Translation")
    print(f"   - For Loop Translation")
    print(f"   - Short-Circuit AND (&&)")
    print(f"   - Short-Circuit OR (||)")
    print(f"   - Nested Control Flow")
    print(f"   - Relational Operators (<, <=, >, >=, ==, !=)")
    print(f"   - Proper x86-64 Conditional Jumps")

if __name__ == "__main__":
    main()
