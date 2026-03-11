# tests/parser/test_parser.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.parser.ast_printer import ASTPrinter


class ParserTester:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0

    def test_valid(self, name, source_code):
        """Тест на валидный код (должен работать)"""
        self.total_tests += 1
        print(f"\n📝 ТЕСТ: {name}")
        print("-" * 40)

        scanner = Scanner(source_code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()

        if parser.errors:
            print(f"❌ ОШИБКА: {parser.errors[0]}")
            return False
        else:
            print(f"✅ УСПЕХ")
            self.passed_tests += 1
            return True

    def test_invalid(self, name, source_code, expected_error_substring=""):
        """Тест на невалидный код (должна быть ошибка)"""
        self.total_tests += 1
        print(f"\n📝 ТЕСТ (ожидается ошибка): {name}")
        print("-" * 40)

        scanner = Scanner(source_code)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        ast = parser.parse()

        if parser.errors:
            print(f"✅ Найдена ошибка: {parser.errors[0]}")
            self.passed_tests += 1
            return True
        else:
            print(f"❌ ДОЛЖНА БЫТЬ ОШИБКА, но парсер прошел")
            return False

    def run_all_tests(self):
        """Запуск всех тестов"""
        print("=" * 60)
        print("ЗАПУСК ТЕСТОВ ПАРСЕРА")
        print("=" * 60)

        # === ТЕСТЫ ВЫРАЖЕНИЙ ===
        self.test_valid("Простое сложение",
                        "fn test() void { int x = 5 + 3; }")

        self.test_valid("Приоритет операций",
                        "fn test() void { int x = 5 + 3 * 2; }")

        self.test_valid("Скобки меняют приоритет",
                        "fn test() void { int x = (5 + 3) * 2; }")

        self.test_valid("Сравнение",
                        "fn test() void { bool b = x < y && z > 5; }")

        self.test_valid("Логические операции",
                        "fn test() void { bool b = (x > 0) || (y < 10); }")

        # === ТЕСТЫ ОПЕРАТОРОВ ===
        self.test_valid("If-else оператор",
                        """fn test() void {
                            if (x > 0) {
                                y = 10;
                            } else {
                                y = -10;
                            }
                        }""")

        self.test_valid("While цикл",
                        """fn test() void {
                            int i = 0;
                            while (i < 10) {
                                i = i + 1;
                            }
                        }""")

        self.test_valid("For цикл",
                        """fn test() void {
                            for (i = 0; i < 10; i = i + 1) {
                                sum = sum + i;
                            }
                        }""")

        # === ТЕСТЫ ОБЪЯВЛЕНИЙ ===
        self.test_valid("Функция с параметрами",
                        """fn add(a int, b int) int {
                            return a + b;
                        }""")

        self.test_valid("Пустая функция",
                        """fn empty() void {
                            return;
                        }""")

        self.test_valid("Несколько функций",
                        """fn first() void {
                            return;
                        }
            
                        fn second() int {
                            return 42;
                        }""")

        # === ПОЛНЫЕ ПРОГРАММЫ ===
        self.test_valid("Факториал",
                        """fn factorial(n int) int {
                            if (n <= 1) {
                                return 1;
                            } else {
                                return n * factorial(n - 1);
                            }
                        }
            
                        fn main() void {
                            int result = factorial(5);
                            return;
                        }""")

        self.test_valid("Сумма чисел",
                        """fn sum(n int) int {
                            int result = 0;
                            int i = 1;
                            while (i <= n) {
                                result = result + i;
                                i = i + 1;
                            }
                            return result;
                        }""")

        # === ТЕСТЫ НА ОШИБКИ ===
        self.test_invalid("Пропущена точка с запятой",
                          "fn test() void { int x = 5 }",
                          "Ожидается ';'")

        self.test_invalid("Незакрытая скобка",
                          "fn test() void { int x = (5 + 3; }",
                          "Ожидается ')'")

        self.test_invalid("Незакрытая функция",
                          "fn test() void { return; ",
                          "Ожидается '}'")

        # === РЕЗУЛЬТАТЫ ===
        print("\n" + "=" * 60)
        print(f"ИТОГИ ТЕСТИРОВАНИЯ:")
        print(f"  Всего тестов: {self.total_tests}")
        print(f"  Пройдено: {self.passed_tests}")
        print(f"  Провалено: {self.total_tests - self.passed_tests}")
        print("=" * 60)


if __name__ == "__main__":
    tester = ParserTester()
    tester.run_all_tests()