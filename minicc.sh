#!/bin/bash

# ============================================
# MiniCompiler - Демонстрация всего проекта
# ============================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

VERSION="1.0.0"

clear

while true; do
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${GREEN}              MINICOMPILER - ПОЛНАЯ ДЕМОНСТРАЦИЯ                 ${CYAN}║${NC}"
    echo -e "${CYAN}║${YELLOW}                        Версия ${VERSION}                             ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ОСНОВНЫЕ ТЕСТЫ${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo "  1.  Запустить ВСЕ тесты (лексер + парсер + семантика + Sprint 7)"
    echo "  2.  Тесты лексера"
    echo "  3.  Тесты парсера"
    echo "  4.  Семантические тесты"
    echo "  5.  Тесты Sprint 7 (массивы + оптимизации)"
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  КОМПИЛЯЦИЯ И ГЕНЕРАЦИЯ${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo "  6.  Скомпилировать простую программу (42)"
    echo "  7.  Показать IR для массива (malloc)"
    echo "  8.  Скомпилировать и запустить factorial (5! = 120)"
    echo "  9.  Скомпилировать и запустить программу с массивом"
    echo " 10.  Сгенерировать ассемблер и показать его"
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ПРОСМОТР КОДА${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo " 11.  Показать оптимизатор (optimizer.py)"
    echo " 12.  Показать генератор ассемблера (x86_generator.py)"
    echo " 13.  Показать генератор IR (ir_generator.py)"
    echo " 14.  Показать демо-программу (factorial)"
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}  0.  Выход${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    read -p "Выберите пункт: " choice

    case $choice in
        1)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  ЗАПУСК ВСЕХ ТЕСТОВ${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo ""
            echo -e "${GREEN}--- Sprint 7 тесты ---${NC}"
            python3 tests/test_sprint7.py
            echo ""
            echo -e "${GREEN}--- Лексер тесты ---${NC}"
            python3 tests/test_runner.py
            echo ""
            echo -e "${GREEN}--- Парсер тесты ---${NC}"
            python3 tests/parser/test_parser.py
            echo ""
            echo -e "${GREEN}--- Семантические тесты ---${NC}"
            python3 tests/semantic/run_tests.py
            ;;
        2)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  ТЕСТЫ ЛЕКСЕРА${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            python3 tests/test_runner.py
            ;;
        3)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  ТЕСТЫ ПАРСЕРА${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            python3 tests/parser/test_parser.py
            ;;
        4)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  СЕМАНТИЧЕСКИЕ ТЕСТЫ${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            python3 tests/semantic/run_tests.py
            ;;
        5)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  ТЕСТЫ SPRINT 7${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            python3 tests/test_sprint7.py
            ;;
        6)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  КОМПИЛЯЦИЯ ПРОСТОЙ ПРОГРАММЫ${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            python3 -c "
from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator
import subprocess

source = 'int main() { int x = 42; return x; }'
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

with open('simple.asm', 'w') as f:
    f.write(asm)

subprocess.run(['nasm', '-f', 'elf64', 'simple.asm', '-o', 'simple.o'])
subprocess.run(['gcc', '-no-pie', 'simple.o', '-o', 'simple'])
result = subprocess.run(['./simple'], capture_output=True)
print(f'Result: exit code = {result.returncode} (should be 42)')
"
            ;;
        7)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  IR FOR ARRAY (malloc)${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            python3 -c "
from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator

source = 'int main() { int arr[5] = {1,2,3,4,5}; return arr[2]; }'
scanner = Scanner(source)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)
ir_gen = IRGenerator(analyzer.get_symbol_table())
ir_funcs = ir_gen.generate(ast)
print(ir_gen.get_ir_text())
"
            ;;
        8)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  FACTORIAL (5! = 120)${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            python3 -c "
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

with open('factorial.asm', 'w') as f:
    f.write(asm)

subprocess.run(['nasm', '-f', 'elf64', 'factorial.asm', '-o', 'factorial.o'])
subprocess.run(['gcc', '-no-pie', 'factorial.o', '-o', 'factorial'])
result = subprocess.run(['./factorial'], capture_output=True)
print(f'Result: factorial(5) = {result.returncode} (should be 120)')
"
            ;;
        9)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  PROGRAM WITH ARRAY${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            python3 -c "
from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator
import subprocess

source = 'int main() { int arr[5] = {10,20,30,40,50}; return arr[2]; }'
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

with open('array.asm', 'w') as f:
    f.write(asm)

subprocess.run(['nasm', '-f', 'elf64', 'array.asm', '-o', 'array.o'])
subprocess.run(['gcc', '-no-pie', 'array.o', '-o', 'array'])
result = subprocess.run(['./array'], capture_output=True)
print(f'Result: arr[2] = {result.returncode} (should be 30)')
"
            ;;
        10)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  GENERATED ASSEMBLY${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            if [ -f "test.asm" ]; then
                echo -e "${GREEN}File test.asm:${NC}"
                cat test.asm
            else
                echo -e "${YELLOW}Generating test.asm...${NC}"
                python3 -c "
from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator

source = 'int main() { int x = 42; return x; }'
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

with open('test.asm', 'w') as f:
    f.write(asm)
print('test.asm created')
"
                cat test.asm
            fi
            ;;
        11)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  OPTIMIZER (optimizer.py)${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            if [ -f "src/ir/optimizer.py" ]; then
                head -50 src/ir/optimizer.py
            else
                echo -e "${RED}File not found: src/ir/optimizer.py${NC}"
            fi
            ;;
        12)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  X86 GENERATOR (x86_generator.py)${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            head -60 src/codegen/x86_generator.py
            ;;
        13)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  IR GENERATOR (ir_generator.py)${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            head -60 src/ir/ir_generator.py
            ;;
        14)
            echo ""
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            echo -e "${YELLOW}  DEMO PROGRAM (factorial)${NC}"
            echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
            cat << 'EOF'
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
int main() {
    return factorial(5);  // 120
}
EOF
            ;;
        0)
            echo ""
            echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
            echo -e "${GREEN}║              THANK YOU FOR USING!                             ║${NC}"
            echo -e "${GREEN}║                   GOODBYE!                                    ║${NC}"
            echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice! Enter number 0-14${NC}"
            ;;
    esac

    echo ""
    read -p "Press Enter to continue..."
    clear
done