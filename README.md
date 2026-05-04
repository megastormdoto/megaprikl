 MiniCompiler

Лёгкая реализация компилятора для языка, похожего на C, с поддержкой лексического, синтаксического и семантического анализа (построение AST, проверка типов, таблица символов), генерацией промежуточного представления (IR), обработки ошибок и набором тестов.

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
│   ├── lexer/
│   │   ├── __init__.py
│   │   ├── token.py
│   │   ├── scanner.py
│   │   └── errors.py
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── ast.py
│   │   ├── parser.py
│   │   ├── ast_printer.py
│   │   └── grammar.txt
│   ├── semantic/
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── symbol_table.py
│   │   ├── type_system.py
│   │   ├── ast_decorator.py
│   │   └── errors.py
│   ├── ir/
│   │   ├── __init__.py
│   │   ├── ir_instructions.py
│   │   ├── basic_block.py
│   │   └── ir_generator.py
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
│   └── test_runner.py
├── examples/
│   ├── hello.src
│   ├── correct.src
│   └── factorial.src
├── docs/
│   └── language_spec.md
├── test_ir_arithmetic.py
├── test_ir_if.py
├── test_ir_while.py
├── README.md
├── pyproject.toml
└── setup.py
```

## Инструкция по сборке

### Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)

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

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -e .
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
python src/main.py --input examples/factorial.src --ir

# Сохранение IR в файл
python src/main.py --input examples/factorial.src --ir --ir-output factorial.ir

# Генерация IR в JSON формате
python src/main.py --input examples/factorial.src --ir --ir-format json

# Генерация CFG в формате DOT для визуализации
python src/main.py --input examples/factorial.src --ir --ir-format dot --ir-output cfg.dot

# Конвертация DOT в PNG (требуется Graphviz)
dot -Tpng cfg.dot -o cfg.png
```

### Пример исходного файла

Создайте файл `examples/correct.src`:

```
fn main() int {
    int x = 5;
    int y = 10;
    return x + y;
}
```

### Пример вывода AST (текстовый формат)

```
Program [2:1]:
  FunctionDecl: main -> void [2:1]
    Parameters:
    Body:
      Block [2:16]:
        VarDecl: int counter = ... [3:5]
          Literal: 42 (int) [3:18]
        Return [4:5]:
          Identifier: counter [4:12]
```

### Пример вывода декорированного AST (с типами)

```
Program [line 1:1]
  FunctionDecl: main [line 1:1]
    Body:
      Block [line 1:15]
        VarDecl: x: int [line 2:5]
          = Literal: 5 [int] [line 2:13]
        VarDecl: y: int [line 3:5]
          = Literal: 10 [int] [line 3:13]
        ReturnStmt [int] [line 4:5]
          BinaryOp: + [int] [line 4:12]
```

### Пример вывода таблицы символов

```
Global (scope 0):
  - main: function -> int (line 1)
```

### Пример вывода семантической ошибки

```
semantic error: return type mismatch in 'main'
  --> line 6, column 5
  = expected: void
  = found: int
```

### Пример генерации IR (Sprint 4)

**Входной код (`examples/if_example.src`):**
```
fn main() int {
    int x = 10;
    if (x > 5) {
        return 1;
    } else {
        return 0;
    }
}
```

**Сгенерированный IR:**
```
# Generated IR
#==================================================

function main: int ()

L0:
    STORE [t0], 10
    t1 = LOAD [t0]
    t2 = CMP_GT t1, 5
    JUMP_IF t2, L1
    JUMP L2

L1:
    RETURN 1

L2:
    RETURN 0
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

# С использованием pytest
pytest tests/ -v

# С отчётом о покрытии
pytest tests/ --cov=src --cov-report=term
```

### Набор тестов

**Тесты лексера:**
- Корректные тесты (20+): отдельные типы токенов, граничные случаи, комментарии
- Некорректные тесты (10+): недопустимые символы, незавершённые строки

**Тесты парсера:**
- Выражения, операторы, объявления, полные программы
- Синтаксические ошибки

**Тесты семантического анализа:**
- Проверка типов, областей видимости, обработка ошибок
- Golden-тестирование

**Тесты генерации IR (Sprint 4):**
- Арифметические выражения (MUL, ADD, RETURN)
- Условные операторы (CMP_GT, JUMP_IF)
- Циклы while (CMP_LT, JUMP_IF)

## Грамматика языка (EBNF)

Формальная грамматика описана в файле [`src/parser/grammar.txt`](src/parser/grammar.txt). Основные правила:

```
Program        ::= { Declaration }
FunctionDecl   ::= "fn" Identifier "(" [ Parameters ] ")" Type Block
VarDecl        ::= Type Identifier [ "=" Expression ] ";"
Statement      ::= Block | IfStmt | WhileStmt | ForStmt | ReturnStmt | ExprStmt | VarDecl
Expression     ::= Assignment
Assignment     ::= LogicalOr { "=" LogicalOr }
LogicalOr      ::= LogicalAnd { "||" LogicalAnd }
LogicalAnd     ::= Equality { "&&" Equality }
Equality       ::= Relational { ("==" | "!=") Relational }
Relational     ::= Additive { ("<" | "<=" | ">" | ">=") Additive }
Additive       ::= Multiplicative { ("+" | "-") Multiplicative }
Multiplicative ::= Unary { ("*" | "/" | "%") Unary }
Unary          ::= [ "-" | "!" ] Primary
Primary        ::= Literal | Identifier | "(" Expression ")" | Call
```

## Детали реализации

### Компоненты лексера
- **token.py**: Определения токенов и перечислений
- **scanner.py**: Основная реализация сканера
- **errors.py**: Обработка ошибок лексера

### Компоненты парсера
- **ast.py**: Классы узлов AST
- **parser.py**: Рекурсивный парсер
- **ast_printer.py**: Вывод AST
- **grammar.txt**: Грамматика в нотации EBNF

### Компоненты семантического анализатора
- **symbol_table.py**: Иерархическая таблица символов
- **type_system.py**: Система типов
- **analyzer.py**: Обход AST с проверками
- **ast_decorator.py**: Вывод AST с типами
- **errors.py**: Сбор семантических ошибок

### Компоненты генератора IR (Sprint 4)
- **ir_instructions.py**: Инструкции и операнды IR (OpCode, Operand, IRInstruction)
- **basic_block.py**: Базовые блоки и контрольный граф потока (BasicBlock, ControlFlowGraph)
- **ir_generator.py**: Генератор IR, обходящий декорированное AST

### Ключевые особенности
- Точное отслеживание позиции (строка/столбец)
- Поддержка UTF-8
- Восстановление после ошибок
- Три формата вывода AST и IR
- Таблица символов с областями видимости
- Проверка типов с неявным расширением
- Трёхадресный код с виртуальными регистрами
- Визуализация CFG в формате DOT

### Производительность
- Лексер: O(n)
- Парсер: O(n) для LL(1) грамматики
- Семантический анализ: O(n) однократный обход AST
- Генерация IR: O(n) однократный обход декорированного AST
- Память: пропорционально размеру AST, таблице символов и IR