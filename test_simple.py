# test_simple.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.parser.ast_printer import ASTPrinter


def test_simple_program():
    # Упрощенная программа БЕЗ стрелки
    source_code = """
    fn main() void {
        int x = 5;
        int y = 10;
        int z = x + y;
        return z;
    }
    """

    print("Исходный код:")
    print(source_code)
    print("-" * 50)

    # Лексический анализ
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()

    print("Токены:")
    for token in tokens:
        print(f"  {token}")
    print("-" * 50)

    # Синтаксический анализ
    parser = Parser(tokens)
    ast = parser.parse()

    if parser.errors:
        print("Ошибки парсера:")
        for error in parser.errors:
            print(f"  {error}")
    else:
        print("AST дерево:")
        printer = ASTPrinter()
        print(printer.print(ast))

    return ast


if __name__ == "__main__":
    test_simple_program()