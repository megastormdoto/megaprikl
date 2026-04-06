#!/usr/bin/env python3
"""Тест семантического анализатора."""

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer

# Тестовая программа
source_code = """
fn main() int {
    int x = 5;
    int y = 10;
    return x + y;
}
"""


def main():
    print("=== ЛЕКСИЧЕСКИЙ АНАЛИЗ ===")
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    print(f"Получено токенов: {len(tokens)}")

    print("\n=== СИНТАКСИЧЕСКИЙ АНАЛИЗ ===")
    parser = Parser(tokens)
    ast = parser.parse()
    print("Парсинг успешен!")

    print("\n=== СЕМАНТИЧЕСКИЙ АНАЛИЗ ===")
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)

    print("\n--- ТАБЛИЦА СИМВОЛОВ ---")
    analyzer.print_symbol_table()

    print("\n--- РЕЗУЛЬТАТ ---")
    if success:
        print("УСПЕХ! Нет семантических ошибок.")
    else:
        print("ОБНАРУЖЕНЫ ОШИБКИ:")
        analyzer.print_errors()


if __name__ == "__main__":
    main()