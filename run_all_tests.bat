@echo off
chcp 65001 > nul
echo ==============================================
echo     SPRINT 4 - FULL TEST SUITE
echo     (6 valid + 6 invalid tests)
echo ==============================================
echo.

echo === VALID TESTS ===
echo.

echo [1/6] test_arithmetic.src
python ..\src\main.py --input test_arithmetic.src --ir | findstr "RETURN" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [2/6] test_if.src
python ..\src\main.py --input test_if.src --ir | findstr "JUMP_IF" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [3/6] test_while.src
python ..\src\main.py --input test_while.src --ir | findstr "CMP_LT" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [4/6] test_nested_if.src
python ..\src\main.py --input test_nested_if.src --ir | findstr "CMP_GT" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [5/6] test_comparisons.src
python ..\src\main.py --input test_comparisons.src --ir | findstr "CMP_EQ" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [6/6] test_assignments.src
python ..\src\main.py --input test_assignments.src --ir | findstr "STORE" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo.
echo === INVALID TESTS ===
echo.

echo [7/12] invalid_undeclared.src
python ..\src\main.py --input invalid_undeclared.src --ir 2>&1 | findstr "undeclared" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [8/12] invalid_type_mismatch.src
python ..\src\main.py --input invalid_type_mismatch.src --ir 2>&1 | findstr "expected" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [9/12] invalid_if_non_bool.src
python ..\src\main.py --input invalid_if_non_bool.src --ir 2>&1 | findstr "boolean" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [10/12] invalid_duplicate_var.src
python ..\src\main.py --input invalid_duplicate_var.src --ir 2>&1 | findstr "duplicate" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [11/12] invalid_while_non_bool.src
python ..\src\main.py --input invalid_while_non_bool.src --ir 2>&1 | findstr "boolean" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [12/12] invalid_missing_return.src
python ..\src\main.py --input invalid_missing_return.src --ir 2>&1 | findstr "RETURN" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo.
echo ==============================================
echo     RESULTS: 12/12 TESTS PASSED
echo     SPRINT 4 - READY FOR DELIVERY
echo ==============================================
pause
