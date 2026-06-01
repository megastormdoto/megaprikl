from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator
import subprocess

source = '''
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
int main() {
    return factorial(5);
}
'''

print("1. Lexing...")
scanner = Scanner(source)
tokens = scanner.scan_tokens()
print(f"   Tokens: {len(tokens)}")

print("2. Parsing...")
parser = Parser(tokens)
ast = parser.parse()
print(f"   AST generated")

print("3. Semantic analysis...")
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)
print(f"   Semantic OK")

print("4. IR generation...")
ir_gen = IRGenerator(analyzer.get_symbol_table())
ir_funcs = ir_gen.generate(ast)
print(f"   IR generated for {len(ir_funcs)} functions")

print("5. Code generation...")
x86_gen = X86Generator()
asm = x86_gen.generate(ir_funcs)

with open('factorial.asm', 'w') as f:
    f.write(asm)

print("6. Assembling...")
subprocess.run(['nasm', '-f', 'elf64', 'factorial.asm', '-o', 'factorial.o'])

print("7. Linking...")
subprocess.run(['gcc', '-no-pie', 'factorial.o', '-o', 'factorial'])

print("8. Running...")
result = subprocess.run(['./factorial'], capture_output=True)
print(f"\nResult: factorial(5) = {result.returncode} (should be 120)")