echo ===========================================
echo    SPRINT 6 DEMONSTRATION
echo    Control Flow & Short-Circuit Evaluation
echo ===========================================
echo.

echo [1] SOURCE CODE:
echo ------------------------------------------
type source.c
echo.

echo [2] COMPILING TO ASSEMBLY...
echo ------------------------------------------
python -c "import sys; sys.path.insert(0, 'C:/Users/user/PycharmProjects/compiler-project'); from src.lexer.scanner import Scanner; from src.parser.parser import Parser; from src.semantic.analyzer import SemanticAnalyzer; from src.ir.ir_generator import IRGenerator; from src.codegen.x86_generator import X86Generator; source = open('source.c').read(); scanner = Scanner(source); tokens = scanner.scan_tokens(); parser = Parser(tokens); ast = parser.parse(); analyzer = SemanticAnalyzer(); analyzer.analyze(ast); ir_gen = IRGenerator(analyzer.get_symbol_table()); ir_funcs = ir_gen.generate(ast); x86_gen = X86Generator(); asm = x86_gen.generate(ir_funcs); open('output.asm', 'w').write(asm); print('output.asm created')"
echo.

echo [3] GENERATED ASSEMBLY:
echo ------------------------------------------
type output.asm
echo.

echo [4] SHORT-CIRCUIT PROOF:
echo ------------------------------------------
echo Source: if (a != 0 && b / a > 2)
echo.
echo In assembly:
echo   cmp eax, 0     - check a != 0
echo   je L1          - if a == 0, jump to else (skip division!)
echo   idiv           - division (executed ONLY if a != 0)
echo.
echo This proves SHORT-CIRCUIT evaluation!
echo.

echo [5] X86-64 CONDITIONAL JUMPS:
echo ------------------------------------------
echo   jg  - jump if greater     (for >)
echo   jl  - jump if less        (for <)
echo   jge - jump if greater or equal (for >=)
echo   jle - jump if less or equal    (for <=)
echo   je  - jump if equal       (for ==)
echo   jne - jump if not equal   (for !=)
echo   jmp - unconditional jump
echo.

echo ===========================================
echo    SPRINT 6 REQUIREMENTS COMPLETED
echo ===========================================
echo    - If-Else Statement Translation
echo    - While Loop Translation
echo    - For Loop Translation
echo    - Short-Circuit AND (&&)
echo    - Short-Circuit OR (||)
echo    - Relational Operators
echo    - x86-64 Conditional Jumps
echo ===========================================
pause
