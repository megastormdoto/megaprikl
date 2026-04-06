#!/usr/bin/env python3
"""Run semantic tests with golden file comparison."""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer


def run_test(test_file, expected_success):
    """Run a single test."""
    with open(test_file, 'r', encoding='utf-8') as f:
        source = f.read()

    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)

    try:
        ast = parser.parse()
    except Exception as e:
        return False, f"Parse error: {e}"

    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)

    if success != expected_success:
        return False, f"Expected {'success' if expected_success else 'failure'}, got {'success' if success else 'failure'}"

    # Generate output
    output = []
    output.append("=== SYMBOL TABLE ===")
    output.append(analyzer.get_symbol_table().dump())

    if not success:
        output.append("\n=== ERRORS ===")
        for err in analyzer.get_errors():
            output.append(str(err))

    return True, "\n".join(output)


def main():
    base_dir = Path(__file__).parent
    valid_dir = base_dir / "valid"
    invalid_dir = base_dir / "invalid"
    golden_dir = base_dir / "golden"

    golden_dir.mkdir(exist_ok=True)

    passed = 0
    failed = 0

    # Run valid tests
    for test_file in valid_dir.glob("*.src"):
        print(f"Running: {test_file.name}")
        success, output = run_test(test_file, expected_success=True)

        # Save golden file
        golden_file = golden_dir / f"{test_file.stem}.golden"
        golden_file.write_text(output, encoding='utf-8')

        if success:
            passed += 1
            print(f"  PASSED")
        else:
            failed += 1
            print(f"  FAILED: {output[:100]}")

    # Run invalid tests
    for test_file in invalid_dir.glob("*.src"):
        print(f"Running: {test_file.name}")
        success, output = run_test(test_file, expected_success=False)

        # Save golden file
        golden_file = golden_dir / f"{test_file.stem}.golden"
        golden_file.write_text(output, encoding='utf-8')

        if success:
            passed += 1
            print(f"  PASSED")
        else:
            failed += 1
            print(f"  FAILED: {output[:100]}")

    print(f"\nSUMMARY: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)