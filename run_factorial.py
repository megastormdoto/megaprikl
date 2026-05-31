from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator

print("1. Reading source...")
with open('demo_factorial.src', 'r') as f:
    source = f.read()

print("2. Scanning...")
scanner = Scanner(source)
tokens = scanner.scan_tokens()
print(f"   Tokens: {len(tokens)}")

print("3. Parsing...")
parser = Parser(tokens)
ast = parser.parse()
print(f"   Declarations: {len(ast.declarations)}")

print("4. Semantic analysis...")
analyzer = SemanticAnalyzer()
if not analyzer.analyze(ast):
    print("   Errors:")
    for err in analyzer.get_errors():
        print(f"     {err}")
    exit(1)
print("   OK")

print("5. Generating IR...")
ir_gen = IRGenerator(analyzer.get_symbol_table())
ir_funcs = ir_gen.generate(ast)
print(f"   Functions: {list(ir_funcs.keys())}")

print("6. Generating assembly...")
x86_gen = X86Generator()
asm = x86_gen.generate(ir_funcs)

# Fix duplicate labels
lines = asm.split('\n')
func_names = list(ir_funcs.keys())
new_lines = []
current_func = None

for line in lines:
    if line.strip() in ['main:', 'factorial:']:
        current_func = line.strip().rstrip(':')
        new_lines.append(line)
    elif line.strip().endswith(':') and current_func:
        label = line.strip().rstrip(':')
        if label in ['L0', '_epilogue']:
            new_lines.append(f"{label}_{current_func}:")
        else:
            new_lines.append(line)
    else:
        # Replace label references
        for func in func_names:
            line = line.replace(' jmp L0', f' jmp L0_{func}')
            line = line.replace(' jmp _epilogue', f' jmp _epilogue_{func}')
            line = line.replace(' jne L0', f' jne L0_{func}')
            line = line.replace(' je L0', f' je L0_{func}')
        new_lines.append(line)

asm = '\n'.join(new_lines)

with open('factorial.asm', 'w') as f:
    f.write(asm)
print("   Assembly written to factorial.asm")

print("\n7. Compiling and running...")
import subprocess
import sys

result = subprocess.run(['nasm', '-f', 'elf64', 'factorial.asm', '-o', 'factorial.o'], 
                        capture_output=True, text=True)
if result.returncode != 0:
    print(f"NASM error: {result.stderr}")
    sys.exit(1)

result = subprocess.run(['gcc', '-no-pie', 'factorial.o', '-o', 'factorial'], 
                        capture_output=True, text=True)
if result.returncode != 0:
    print(f"GCC error: {result.stderr}")
    sys.exit(1)

result = subprocess.run(['./factorial'], capture_output=True, text=True)
print(f"Output: {result.stdout}")
print(f"Exit code: {result.returncode}")
