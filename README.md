```markdown
# MiniCompiler

Лёгкая реализация компилятора для языка, похожего на C, с поддержкой лексического, синтаксического и семантического анализа (построение AST, проверка типов, таблица символов), генерацией промежуточного представления (IR), генерацией x86-64 ассемблерного кода, системой оптимизаций и набором тестов.

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

### Спринт 7 (Массивы, внешние вызовы и оптимизации)
- **Массивы:**
  - Синтаксис объявления: `int arr[5]`
  - Инициализация: `int arr[3] = {1, 2, 3}`
  - Доступ к элементам: `arr[i]`
  - Выделение памяти в куче через `malloc` (с поддержкой `free`)
  - Проверка границ массива (bounds checking)
  - Копирование массивов через `memcpy`

- **Внешние вызовы (System V AMD64 ABI):**
  - Объявление внешних функций: `extern int printf(char* fmt, ...)`
  - Поддержка стандартной библиотеки C: `printf`, `scanf`, `malloc`, `free`, `memcpy`, `exit`
  - Передача аргументов через регистры: `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`
  - Проверка возврата `malloc` на `NULL` с выводом ошибки

- **Оптимизации IR:**
  - **Constant folding** — свёртка константных выражений: `10 + 20 → 30`
  - **Constant propagation** — распространение констант по IR
  - **Dead code elimination** — удаление недостижимого кода
  - **Optimization pipeline** — цепочка последовательных оптимизаций

- **Демонстрационная программа:**
  - Рекурсивный факториал (`demo_factorial.src`)
  - Алгоритм быстрой сортировки Quicksort с использованием массивов

- **Тестирование:**
  - Тесты для массивов (объявление, инициализация, доступ)
  - Тесты для внешних вызовов
  - Тесты для оптимизаций (constant folding, propagation, dead code elimination)

## Спецификация языка

Полная спецификация языка доступна в файле [`docs/language_spec.md`](docs/language_spec.md) и включает:

- Формальное EBNF-определение грамматики
- Категории токенов с регулярными выражениями
- Ключевые слова: `if`, `else`, `while`, `for`, `int`, `float`, `bool`, `return`, `true`, `false`, `void`, `struct`, `extern`
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
│   │   ├── ir_generator.py
│   │   └── optimizer.py       # Sprint 7: оптимизации IR
│   ├── codegen/                # Sprint 5-7
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
│   ├── test_sprint7.py         # Sprint 7: тесты массивов и оптимизаций
│   └── test_runner.py
├── examples/
│   ├── hello.src
│   ├── correct.src
│   └── factorial.src
├── sprint6_demo/               # Sprint 6 демо
│   ├── source.c
│   ├── output.asm
│   └── demo.bat
├── demo_factorial.src          # Sprint 7: демо-программа (факториал)
├── demo_quicksort.src          # Sprint 7: демо-программа (быстрая сортировка)
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
- GCC (для линковки с библиотекой C)

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

**Windows (рекомендуется WSL):**
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

### Генерация x86-64 ассемблерного кода — Sprint 5-7

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
gcc -no-pie output.o -o output_program

# Запуск
./output_program
echo $?  # выводит код возврата (результат программы)
```

### Пример исходного файла с массивами (Sprint 7)

Создайте файл `test_array.src`:

```c
extern void printf(char* fmt, ...);

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    printf("arr[2] = %d\n", arr[2]);
    return 0;
}
```

### Пример сгенерированного ассемблера для массива (Sprint 7)

**Исходный код:**
```c
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    return arr[2];
}
```

**Сгенерированный IR:**
```
function main: int ()
L0:
    t0 = MUL 5, 4          # размер массива в байтах
    t1 = CALL malloc()     # выделение памяти в куче
    STORE [t2], t1         # сохранение указателя
    STORE [t3], 5          # сохранение размера
    # инициализация элементов 0-4
    t19 = LOAD [t2]
    t20 = MUL 2, 4         # индекс 2 * 4
    t21 = ADD t19, t20     # вычисление адреса arr[2]
    t22 = LOAD [t21]       # загрузка значения
    RETURN t22
```

**Особенности реализации:**
- Массивы выделяются в куче через `malloc`
- Добавлена проверка возврата `malloc` на `NULL`
- Поддержка `free` для освобождения памяти
- Проверка границ массива (опционально)

### Пример с оптимизациями (Sprint 7)

**Исходный код до оптимизаций:**
```c
int compute() {
    int x = 10 + 20;        // константное выражение
    int y = x * 2;          // использование константы
    if (y > 50) {           // константное условие
        return 1;
    } else {
        return 0;           // недостижимый код
    }
}
```

**После оптимизаций (constant folding + propagation + dead code elimination):**
```c
int compute() {
    return 1;               // весь код свёрнут в одну инструкцию
}
```

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

# Тесты Sprint 7 (массивы и оптимизации)
python tests/test_sprint7.py

# С использованием pytest
pytest tests/ -v
```

### Набор тестов Sprint 7

- **TEST-1:** Объявление и инициализация массивов
- **TEST-2:** Внешние вызовы (printf, malloc, free)
- **TEST-3:** Constant folding и propagation
- **TEST-4:** Dead code elimination и optimization pipeline

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

### Компоненты оптимизатора IR (Sprint 7)
- **optimizer.py**: Проходы оптимизаций:
  - Constant propagation
  - Dead code elimination
  - Optimization pipeline

### Компоненты codegen (Sprint 5-7)
- **abi.py**: Константы System V AMD64 ABI
- **stack_frame.py**: Управление стековым кадром
- **register_allocator.py**: Аллокатор регистров
- **x86_generator.py**: Генератор ассемблера x86-64 с поддержкой:
  - Управляющих конструкций (if/else, while, for)
  - Short-circuit evaluation (&&, ||)
  - Массивов (malloc, free, bounds checking)
  - Внешних вызовов (printf, malloc, free, memcpy)

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
- **Новое (Sprint 7):** Поддержка массивов (синтаксис, выделение в куче, bounds checking)
- **Новое (Sprint 7):** Внешние вызовы стандартной библиотеки C
- **Новое (Sprint 7):** Оптимизации IR (constant folding, propagation, dead code elimination)

### Производительность
- Лексер: O(n)
- Парсер: O(n) для LL(1) грамматики
- Семантический анализ: O(n)
- Генерация IR: O(n)
- Оптимизации IR: O(n) за проход
- Генерация ассемблера: O(n) с одним проходом
- Память: пропорционально размеру AST, таблице символов, IR и ассемблеру
```