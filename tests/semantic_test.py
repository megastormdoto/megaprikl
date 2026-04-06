#!/usr/bin/env python3
"""Testing semantic analyzer on different programs."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer


def test_program(name, source_code, expect_success):
    """Run a single program test."""
    print(f"\n{'=' * 60}")
    print(f"Test: {name}")
    print(f"{'=' * 60}")
    print(f"Code:\n{source_code}")

    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)

    try:
        ast = parser.parse()
    except Exception as e:
        print(f"FAIL: Syntax error - {e}")
        return False

    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)

    print(f"\nResult:")
    if success:
        print(f"  SUCCESS - no semantic errors")
    else:
        print(f"  FAILED - {len(analyzer.get_errors())} error(s)")
        print(f"\nErrors:")
        for err in analyzer.get_errors():
            print(f"  - {err}")

    print(f"\nSymbol Table:")
    analyzer.print_symbol_table()

    if success != expect_success:
        print(f"\nWARNING: Expected {'success' if expect_success else 'failure'} but got opposite")
        return False

    return True


def main():
    print("SEMANTIC ANALYSIS TESTS")
    print("=" * 60)

    tests = [
        # Valid programs (should succeed)
        ("Valid: Simple program with int",
         """
fn main() int {
    int x = 5;
    int y = 10;
    return x + y;
}
         """, True),

        ("Valid: Function with parameters",
         """
fn add(int a, int b) int {
    return a + b;
}

fn main() int {
    int result = add(3, 4);
    return result;
}
         """, True),

        ("Valid: Nested scopes",
         """
fn main() int {
    int x = 1;
    if (x == 1) {
        int y = 2;
        x = x + y;
    }
    return x;
}
         """, True),

        ("Valid: Void function without return",
         """
fn main() void {
    int x = 5;
    x = x + 1;
}
         """, True),

        # Invalid programs (should fail)
        ("Invalid: Undeclared variable",
         """
fn main() int {
    int x = 5;
    return y;
}
         """, False),

        ("Invalid: Duplicate variable",
         """
fn main() int {
    int x = 5;
    int x = 10;
    return x;
}
         """, False),

        ("Invalid: Type mismatch assignment",
         """
fn main() int {
    int x = 3.14;
    return x;
}
         """, False),

        ("Invalid: Wrong argument count",
         """
fn add(int a, int b) int {
    return a + b;
}

fn main() int {
    int x = add(5);
    return x;
}
         """, False),

        ("Invalid: Return value in void function",
         """
fn main() void {
    return 42;
}
         """, False),

        ("Invalid: Condition not boolean",
         """
fn main() void {
    int x = 5;
    if (x + 3) {
        x = 0;
    }
}
         """, False),
    ]

    passed = 0
    failed = 0

    for name, code, expect in tests:
        try:
            if test_program(name, code, expect):
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\nEXCEPTION in test '{name}': {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)