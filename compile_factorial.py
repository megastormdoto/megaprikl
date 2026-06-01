from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator
import subprocess

source = '''int factorial(int n) {
    int result = 1;
    int i = 1;
    while (i <= n) {
        result = result * i;
        i = i + 1;
    }
    return result;
}

int main() {
    return factorial(5);
}'''

print("1. Scanning...")
scanner = Scanner(source)
tokens = scanner.scan_tokens()
print(f"   Tokens: {len(tokens)}")

print("2. Parsing...")
parser = Parser(tokens)
ast = parser.parse()
print(f"   Declarations: {len(ast.declarations)}")

print("3. Semantic analysis...")
analyzer = SemanticAnalyzer()
if not analyzer.analyze(ast):
    print("   Errors:")
    for err in analyzer.get_errors():
        print(f"     {err}")
    exit(1)
print("   OK")

print("4. Generating IR...")
ir_gen = IRGenerator(analyzer.get_symbol_table())
ir_funcs = ir_gen.generate(ast)
print(f"   Functions: {list(ir_funcs.keys())}")

print("5. Generating assembly...")
x86_gen = X86Generator()
asm = x86_gen.generate(ir_funcs)

with open('factorial.asm', 'w') as f:
    f.write(asm)

print("6. Assembling and linking...")
subprocess.run(['nasm', '-f', 'elf64', 'factorial.asm', '-o', 'factorial.o'])
subprocess.run(['gcc', '-no-pie', 'factorial.o', '-o', 'factorial'])

print("7. Running...")
result = subprocess.run(['./factorial'], capture_output=True)
print(f'Result: {result.returncode}')
