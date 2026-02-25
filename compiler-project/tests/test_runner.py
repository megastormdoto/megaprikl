#!/usr/bin/env python3
import sys
import os
import glob
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.lexer.scanner import Scanner


def run_test(input_file: str, expected_file: str) -> bool:
    """Run a single test case"""
    with open(input_file, 'r') as f:
        source = f.read()

    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    # Generate actual output
    actual_output = []
    for token in tokens:
        if token.literal_value is not None:
            actual_output.append(
                f"{token.line}:{token.column} {token.type.name} \"{token.lexeme}\" {token.literal_value}")
        else:
            actual_output.append(f"{token.line}:{token.column} {token.type.name} \"{token.lexeme}\"")

    # Read expected output
    with open(expected_file, 'r') as f:
        expected_output = [line.strip() for line in f.readlines()]

    # Compare
    if actual_output == expected_output:
        print(f"✅ PASS: {os.path.basename(input_file)}")
        return True
    else:
        print(f"❌ FAIL: {os.path.basename(input_file)}")
        print("Expected:")
        for line in expected_output:
            print(f"  {line}")
        print("Actual:")
        for line in actual_output:
            print(f"  {line}")
        return False


def run_all_tests():
    """Run all test cases"""
    test_dir = Path(__file__).parent

    passed = 0
    failed = 0

    # Run valid tests
    print("\n=== VALID TESTS ===\n")
    for input_file in sorted(glob.glob(str(test_dir / 'lexer/valid/*.src'))):
        expected_file = input_file.replace('.src', '.expected')
        if run_test(input_file, expected_file):
            passed += 1
        else:
            failed += 1

    # Run invalid tests
    print("\n=== INVALID TESTS ===\n")
    for input_file in sorted(glob.glob(str(test_dir / 'lexer/invalid/*.src'))):
        expected_file = input_file.replace('.src', '.expected')
        if run_test(input_file, expected_file):
            passed += 1
        else:
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)