
```markdown
# MiniCompiler

Лёгкая реализация компилятора для языка, похожего на C, с поддержкой лексического, синтаксического и семантического анализа (построение AST, проверка типов, таблица символов), генерацией промежуточного представления (IR), генерацией x86-64 ассемблерного кода, обработки ошибок и набором тестов.

## Команда

- Индивидуальный проект (выполнен в рамках курса по конструированию компиляторов)

## Возможности

### Спринт 1 (Лексический анализ)
- Лексический анализ (токенизация) для C-подобного языка
- Поддержка ключевых слов, идентификаторов, литералов, операторов и разделителей
- Точное отслеживание строк и столбцов
- Комплексная обработка ошибок с восстановлением после них
- Поддержка UTF-8
- Временная сложность O(n) с эффективным использованием памяти

### Спринт 2 (Синтаксический анализ)
- Формальная грамматика языка в нотации EBNF
- Рекурсивный парсер с методом рекурсивного спуска
- Построение абстрактного синтаксического дерева (AST)
- Поддержка приоритета операторов (от унарных до логических)
- Вывод AST в трёх форматах: текст, Graphviz DOT, JSON
- Командная строка с настраиваемыми параметрами
- Обработка синтаксических ошибок с указанием позиции

### Спринт 3 (Семантический анализ)
- Иерархическая таблица символов с поддержкой вложенных областей видимости
- Система типов с проверкой совместимости (int, float, bool, void, string)
- Обход AST с проверкой всех семантических правил
- Проверка объявлений (функции, переменные, структуры)
- Проверка типов в выражениях, присваиваниях и вызовах функций
- Проверка областей видимости и использование необъявленных идентификаторов
- Декорирование AST аннотациями типов
- Подробные сообщения об ошибках с указанием позиции
- Восстановление после ошибок с продолжением анализа

### Спринт 4 (Генерация промежуточного представления - IR)
- Трёхадресный код в форме четырёх операций (3-address code)
- Система виртуальных регистров (t1, t2, ...) для временных значений
- Поддержка всех типов операций: арифметические, логические, сравнения, работа с памятью
- Базовые блоки и контрольный граф потока (CFG) для управляющих конструкций
- Генерация IR для выражений, присваиваний, условий (if/else) и циклов (while, for)
- Интеграция с семантическим анализатором (типы и таблица символов)
- Вывод IR в трёх форматах: текст для чтения, JSON для машинной обработки, DOT для визуализации
- Набор юнит-тестов для проверки корректности генерации IR

### Спринт 5 (Генерация x86-64 ассемблерного кода)
- Трансляция IR в ассемблерный код x86-64 (синтаксис NASM)
- Поддержка System V AMD64 ABI (стековый кадр, регистры, передача параметров)
- Правильные пролог и эпилог функций: `push rbp`, `mov rbp, rsp`, `sub rsp, N`, `mov rsp, rbp`, `pop rbp`, `ret`
- Управление стековым кадром для локальных переменных и временных значений
- Базовый аллокатор регистров с выбрасыванием на стек
- Генерация инструкций: `mov`, `add`, `sub`, `imul`, `idiv`, `cmp`, `jmp`, `jnz`, `call`, `ret`
- Runtime библиотека на ассемблере с функциями `print_int`, `print_string`, `exit`, `_start`
- Полный пайплайн: исходный код → IR → ассемблер → исполняемый файл (через NASM и LD)

### Спринт 6 (Управляющие конструкции и short-circuit evaluation)
- Генерация кода для условных операторов (if/else) с правильными переходами
- Трансляция циклов while и for в ассемблер x86-64
- Реализация short-circuit evaluation для логических операторов && и ||
- Поддержка реляционных операторов (`<`, `<=`, `>`, `>=`, `==`, `!=`) с генерацией соответствующих инструкций сравнения
- Генерация условных переходов: `jg`, `jl`, `jge`, `jle`, `je`, `jne`, `jmp`
- Правильная обработка вложенных управляющих конструкций
- Демонстрационные примеры в папке `sprint6_demo/`

## Спецификация языка

Полная спецификация языка доступна в файле [`docs/language_spec.md`](docs/language_spec.md) и включает:

- Формальное EBNF-определение грамматики
- Категории токенов с регулярными выражениями
- Ключевые слова: `if`, `else`, `while`, `for`, `int`, `float`, `bool`, `return`, `true`, `false`, `void`, `struct`, `fn`
- Идентификаторы: буквы, цифры, подчёркивания (макс. 255 символов, регистрозависимые)
- Литералы: целые числа, числа с плавающей точкой, строки, булевы значения
- Операторы: арифметические (`+ - * / %`), реляционные (`== != < <= > >=`), логические (`&& || !`), присваивание (`=`)
- Разделители: `() {} [] ; ,`
- Комментарии: однострочные (`//`) и многострочные (`/* */`) с опциональной вложенностью
- Пробельные символы: пробел, табуляция, перевод строки (`\n`), возврат каретки (`\r`)

## Структура проекта

```
compiler-project/
├── src/
│   ├── lexer/                  # Sprint 1
│   │   ├── __init__.py
│   │   ├── token.py
│   │   ├── scanner.py
│   │   └── errors.py
│   ├── parser/                 # Sprint 2
│   │   ├── __init__.py
│   │   ├── ast.py
│   │   ├── parser.py
│   │   ├── ast_printer.py
│   │   └── grammar.txt
│   ├── semantic/               # Sprint 3
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── symbol_table.py
│   │   ├── type_system.py
│   │   ├── ast_decorator.py
│   │   └── errors.py
│   ├── ir/                     # Sprint 4
│   │   ├── __init__.py
│   │   ├── ir_instructions.py
│   │   ├── basic_block.py
│   │   └── ir_generator.py
│   ├── codegen/                # Sprint 5-6
│   │   ├── __init__.py
│   │   ├── abi.py              # System V ABI константы
│   │   ├── stack_frame.py      # Управление стековым кадром
│   │   ├── register_allocator.py # Аллокатор регистров
│   │   └── x86_generator.py    # Генератор ассемблера x86-64
│   ├── runtime/                # Sprint 5
│   │   └── runtime.asm         # Runtime библиотека (NASM)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── main.py
├── tests/
│   ├── lexer/
│   │   ├── valid/
│   │   └── invalid/
│   ├── parser/
│   │   ├── valid/
│   │   └── invalid/
│   ├── semantic/
│   │   ├── valid/
│   │   ├── invalid/
│   │   ├── golden/
│   │   └── run_tests.py
│   ├── control_flow/           # Sprint 6
│   │   ├── valid/
│   │   └── invalid/
│   └── test_runner.py
├── examples/
│   ├── hello.src
│   ├── correct.src
│   └── factorial.src
├── sprint6_demo/               # Sprint 6 демо
│   ├── source.c
│   ├── output.asm
│   └── demo.bat
├── docs/
│   └── language_spec.md
├── README.md
├── pyproject.toml
└── setup.py
```

## Инструкция по сборке

### Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)
- NASM (для сборки ассемблера)
- LD (линковщик, входит в binutils)

### Установка

```bash
# Клонирование репозитория
git clone <repository-url>
cd compiler-project

# Установка в режиме разработки
pip install -e .

# Или установка с зависимостями для тестирования
pip install -e .[test]
```

### Примечания для разных платформ

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**Windows (WSL рекомендуется для codegen):**
```bash
# Для генерации ассемблера лучше использовать WSL
wsl
cd /mnt/c/Users/user/PycharmProjects/compiler-project
```

## Быстрый старт

### Лексический анализ

```bash
python -m src.lexer.scanner --input examples/hello.src --output tokens.txt
```

### Синтаксический анализ (построение AST)

```bash
# Базовый запуск
python src/main.py --input examples/hello.src

# Сохранение AST в файл
python src/main.py --input examples/hello.src --output ast.txt

# Генерация DOT графа
python src/main.py --input examples/hello.src --format dot --output ast.dot

# Экспорт в JSON
python src/main.py --input examples/hello.src --format json --output ast.json
```

### Семантический анализ

```bash
# Семантическая проверка
python src/main.py --input examples/correct.src --check

# Вывод таблицы символов
python src/main.py --input examples/correct.src --symbols

# Вывод декорированного AST
python src/main.py --input examples/correct.src --decorated-ast
```

### Генерация промежуточного представления (IR) — Sprint 4

```bash
# Генерация IR в консоль
python src/main.py --input test_asm.src --ir

# Сохранение IR в файл
python src/main.py --input test_asm.src --ir --ir-output test.ir

# Генерация IR в JSON формате
python src/main.py --input test_asm.src --ir --ir-format json
```

### Генерация x86-64 ассемблерного кода — Sprint 5-6

```bash
# Полный пайплайн: исходник → IR → ассемблер
python -c "
from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.ir.ir_generator import IRGenerator
from src.codegen.x86_generator import X86Generator

source = open('test_asm.src', 'r', encoding='utf-8').read()
scanner = Scanner(source)
tokens = scanner.scan_tokens()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)
ir_gen = IRGenerator(analyzer.get_symbol_table())
ir_funcs = ir_gen.generate(ast)
x86_gen = X86Generator()
print(x86_gen.generate(ir_funcs))
" > output.asm

# Сборка исполняемого файла
nasm -f elf64 output.asm -o output.o
ld -o output_program output.o

# Запуск
./output_program
echo $?  # выводит код возврата (результат программы)
```

### Пример исходного файла

Создайте файл `test_asm.src`:

```
fn main() int {
    int x = 2 * 3 + 4;
    return x;
}
```

### Пример сгенерированного ассемблера для if-else с short-circuit (Sprint 6)

**Исходный код:**
```c
fn main() int {
    int a = 0;
    int b = 5;
    
    if (a != 0 && b / a > 2) {
        return 1;
    } else {
        return 2;
    }
}
```

**Сгенерированный ассемблер x86-64:**
```asm
main:
    push rbp
    mov rbp, rsp

    mov eax, 0          ; a = 0
    mov eax, 5          ; b = 5
    cmp eax, 0          ; проверка a != 0
    je L1               ; если a == 0, прыжок в else (short-circuit!)
    ...
    idiv eax            ; деление (выполняется только если a != 0)
    cmp eax, 2
    jg .Lcmp_true_2
    ...
L1:                     ; else-ветка
    mov eax, 0
    ...
    mov eax, 2          ; return 2
    jmp .epilogue
```

**Ключевая особенность:** Благодаря short-circuit evaluation, инструкция `idiv` не выполняется при `a == 0`, что предотвращает деление на ноль.

## Тестирование

### Запуск всех тестов

```bash
# Тесты лексера
python tests/test_runner.py

# Тесты парсера
python tests/parser/test_parser.py

# Семантические тесты
python tests/semantic/run_tests.py

# Тесты IR генерации (Sprint 4)
python test_ir_arithmetic.py
python test_ir_if.py
python test_ir_while.py

# Тесты управляющих конструкций (Sprint 6)
python tests/control_flow/run_tests.py

# С использованием pytest
pytest tests/ -v
```

### Набор тестов

**Тесты лексера, парсера, семантики, IR** — описаны в предыдущих спринтах.

**Тесты codegen (Sprint 5):**
- Проверка генерации пролога/эпилога
- Проверка арифметических инструкций
- Проверка работы со стеком
- ABI compliance (регистры, выравнивание)

**Тесты управляющих конструкций (Sprint 6):**
- If-else statement (true/false paths)
- While and for loops
- Nested conditionals
- Short-circuit evaluation for && and ||
- Mixed arithmetic and logical expressions

## Грамматика языка (EBNF)

Формальная грамматика описана в файле [`src/parser/grammar.txt`](src/parser/grammar.txt).

## Детали реализации

### Компоненты лексера
- **token.py**: Определения токенов
- **scanner.py**: Сканер с отслеживанием позиции
- **errors.py**: Обработка ошибок

### Компоненты парсера
- **ast.py**: Классы узлов AST
- **parser.py**: Рекурсивный парсер
- **ast_printer.py**: Вывод AST

### Компоненты семантического анализатора
- **symbol_table.py**: Таблица символов
- **type_system.py**: Система типов
- **analyzer.py**: Обход AST с проверками

### Компоненты генератора IR (Sprint 4)
- **ir_instructions.py**: Инструкции и операнды IR
- **basic_block.py**: Базовые блоки и CFG
- **ir_generator.py**: Генерация IR из AST

### Компоненты codegen (Sprint 5-6)
- **abi.py**: Константы System V AMD64 ABI
- **stack_frame.py**: Управление стековым кадром
- **register_allocator.py**: Аллокатор регистров
- **x86_generator.py**: Генератор ассемблера x86-64 (расширен для поддержки управляющих конструкций)
- **runtime.asm**: Runtime библиотека (NASM)

### Ключевые особенности
- Точное отслеживание позиции (строка/столбец)
- Поддержка UTF-8
- Восстановление после ошибок
- Три формата вывода AST и IR
- Таблица символов с областями видимости
- Проверка типов с неявным расширением
- Трёхадресный код с виртуальными регистрами
- Визуализация CFG в формате DOT
- **Новое (Sprint 5):** Генерация ассемблера x86-64 с соблюдением ABI
- **Новое (Sprint 5):** Runtime библиотека для вывода и ввода
- **Новое (Sprint 6):** Поддержка if/else, циклов while/for
- **Новое (Sprint 6):** Short-circuit evaluation для && и ||
- **Новое (Sprint 6):** Генерация условных переходов x86-64

### Производительность
- Лексер: O(n)
- Парсер: O(n) для LL(1) грамматики
- Семантический анализ: O(n)
- Генерация IR: O(n)
- Генерация ассемблера: O(n) с одним проходом
- Память: пропорционально размеру AST, таблице символов, IR и ассемблеру
```
