#!/bin/bash
# Правильная компиляция через Python

python3 -c "
from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator
import sys

with open('$1', 'r') as f:
    source = f.read()

scanner = Scanner(source)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)
ir_gen = IRGenerator(analyzer.get_symbol_table())
ir_funcs = ir_gen.generate(ast)
x86_gen = X86Generator()
asm = x86_gen.generate(ir_funcs)

out = '$2' if len(sys.argv) > 2 else 'a.out'
with open(out, 'w') as f:
    f.write(asm)
print(f'Assembly written to {out}')
" "$@"

if [ -f "$2" ]; then
    nasm -f elf64 "$2" -o "${2%.*}.o"
    gcc -no-pie "${2%.*}.o" -o "${2%.*}"
    rm "$2" "${2%.*}.o"
fi
