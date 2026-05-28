@echo off
chcp 65001 > nul
echo ==============================================
echo     SPRINT 4 - FULL TEST SUITE
echo     (9 valid + 6 invalid = 15 tests)
echo ==============================================
echo.

echo === VALID TESTS (9) ===
echo.

echo [1/9] test_arithmetic.src
python ..\src\main.py --input test_arithmetic.src --ir | findstr "RETURN" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [2/9] test_if.src
python ..\src\main.py --input test_if.src --ir | findstr "JUMP_IF" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [3/9] test_while.src
python ..\src\main.py --input test_while.src --ir | findstr "CMP_LT" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [4/9] test_nested_if.src
python ..\src\main.py --input test_nested_if.src --ir | findstr "CMP_GT" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [5/9] test_comparisons.src
python ..\src\main.py --input test_comparisons.src --ir | findstr "CMP_EQ" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [6/9] test_assignments.src
python ..\src\main.py --input test_assignments.src --ir | findstr "STORE" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [7/9] test_return_constant.src
python ..\src\main.py --input test_return_constant.src --ir | findstr "RETURN" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [8/9] test_multiple_vars.src
python ..\src\main.py --input test_multiple_vars.src --ir | findstr "ADD" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo [9/9] test_two_ifs.src
python ..\src\main.py --input test_two_ifs.src --ir | findstr "CMP_EQ" > nul
if %errorlevel% equ 0 (echo   PASS) else (echo   FAIL)

echo.
echo === INVALID TESTS (6) ===
echo.

echo [10/15] invalid_undeclared.src
echo ----------------------------------------------
python ..\src\main.py --input invalid_undeclared.src --ir 2>&1 | findstr "semantic error"
if %errorlevel% equ 0 (echo   STATUS: PASS) else (echo   STATUS: FAIL)
echo.

echo [11/15] invalid_type_mismatch.src
echo ----------------------------------------------
python ..\src\main.py --input invalid_type_mismatch.src --ir 2>&1 | findstr "semantic error"
if %errorlevel% equ 0 (echo   STATUS: PASS) else (echo   STATUS: FAIL)
echo.

echo [12/15] invalid_if_non_bool.src
echo ----------------------------------------------
python ..\src\main.py --input invalid_if_non_bool.src --ir 2>&1 | findstr "semantic error"
if %errorlevel% equ 0 (echo   STATUS: PASS) else (echo   STATUS: FAIL)
echo.

echo [13/15] invalid_duplicate_var.src
echo ----------------------------------------------
python ..\src\main.py --input invalid_duplicate_var.src --ir 2>&1 | findstr "semantic error"
if %errorlevel% equ 0 (echo   STATUS: PASS) else (echo   STATUS: FAIL)
echo.

echo [14/15] invalid_while_non_bool.src
echo ----------------------------------------------
python ..\src\main.py --input invalid_while_non_bool.src --ir 2>&1 | findstr "semantic error"
if %errorlevel% equ 0 (echo   STATUS: PASS) else (echo   STATUS: FAIL)
echo.

echo [15/15] invalid_missing_return.src
echo ----------------------------------------------
python ..\src\main.py --input invalid_missing_return.src --ir 2>&1 | findstr "RETURN 0"
if %errorlevel% equ 0 (echo   STATUS: PASS) else (echo   STATUS: FAIL)
echo.

echo.
echo ==============================================
echo     SPRINT 4 - ALL TESTS COMPLETE
echo ==============================================
pause
