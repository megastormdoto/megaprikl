import sys
import subprocess
from pathlib import Path

def run_test(src_path, expected_keywords):
    """Run IR generation and check if all keywords are present."""
    result = subprocess.run(
        ["python", "../src/main.py", "--input", str(src_path), "--ir"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    output = result.stdout + result.stderr
    missing = [kw for kw in expected_keywords if kw not in output]
    return len(missing) == 0, missing, output

def run_negative_test(src_path, expected_phrases):
    """Run IR generation and check for expected error messages."""
    result = subprocess.run(
        ["python", "../src/main.py", "--input", str(src_path), "--ir"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    output = result.stdout + result.stderr
    found_all = all(phrase in output.lower() for phrase in expected_phrases)
    return found_all, output

def main():
    valid_dir = Path("valid")
    invalid_dir = Path("invalid")
    
    positive_tests = {
        "arithmetic_full.src": ["MUL", "ADD", "SUB", "DIV", "RETURN"],
        "logic.src": ["AND", "OR", "NOT"],
        "nested_if.src": ["CMP_GT", "JUMP_IF", "JUMP"],
        "if_no_else.src": ["CMP_GT", "JUMP_IF"],
        "for_loop.src": ["CMP_LT", "JUMP_IF", "ADD", "JUMP"],
        "comparisons.src": ["CMP_EQ", "CMP_NE", "CMP_LT", "CMP_LE", "CMP_GT", "CMP_GE"],
        "nested_loops.src": ["CMP_LT", "JUMP_IF"],
        "functions.src": ["CALL", "PARAM", "RETURN"],
    }
    
    negative_tests = {
        "undeclared_var.src": ["undeclared", "x"],
        "type_mismatch.src": ["type", "mismatch"],
        "void_return.src": ["void", "return"],
        "duplicate_var.src": ["duplicate", "x"],
        "if_non_bool.src": ["condition", "boolean"],
        "while_non_bool.src": ["condition", "boolean"],
        "missing_return.src": ["return", "non-void"],
        "undeclared_func.src": ["not", "function"],
    }
    
    print("=" * 70)
    print("SPRINT 4 - IR GENERATION FULL TEST SUITE")
    print("=" * 70)
    
    passed = 0
    total = 0
    
    # Positive tests
    print("\n[POSITIVE TESTS] (should generate IR successfully)")
    print("-" * 50)
    
    for filename, keywords in positive_tests.items():
        src_file = valid_dir / filename
        total += 1
        if not src_file.exists():
            print(f"  SKIP: {filename} (file not found)")
            continue
        
        success, missing, _ = run_test(src_file, keywords)
        if success:
            print(f"  PASS: {filename}")
            passed += 1
        else:
            print(f"  FAIL: {filename}")
            print(f"       Missing: {missing}")
    
    # Negative tests
    print("\n[NEGATIVE TESTS] (should report semantic errors)")
    print("-" * 50)
    
    for filename, phrases in negative_tests.items():
        src_file = invalid_dir / filename
        total += 1
        if not src_file.exists():
            print(f"  SKIP: {filename} (file not found)")
            continue
        
        success, _ = run_negative_test(src_file, phrases)
        if success:
            print(f"  PASS: {filename}")
            passed += 1
        else:
            print(f"  FAIL: {filename} (expected error not found)")
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} / {total} tests passed")
    if passed == total:
        print("SPRINT 4 - ALL TESTS PASSED!")
    else:
        print(f"SPRINT 4 - {total - passed} tests failed")
    print("=" * 70)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
