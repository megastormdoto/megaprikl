# MiniCompiler

Лёгкая реализация компилятора для языка, похожего на C, с поддержкой лексического и синтаксического анализа (построение AST), обработки ошибок и набором тестов.

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
│   │   ├── token.py          # Определения токенов и перечисления
│   │   ├── scanner.py        # Основная реализация сканера
│   │   └── errors.py         # Обработка ошибок лексера
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── ast.py            # Классы узлов абстрактного синтаксического дерева
│   │   ├── parser.py         # Рекурсивный парсер
│   │   ├── ast_printer.py    # Вывод AST в читаемом формате
│   │   └── grammar.txt       # Формальная грамматика языка
│   └── utils/
│       ├── __init__.py
│       └── helpers.py        # Вспомогательные функции
├── tests/
│   ├── lexer/
│   │   ├── valid/             # Тесты лексера с корректным вводом
│   │   └── invalid/           # Тесты лексера с некорректным вводом
│   ├── parser/
│   │   ├── valid/             # Тесты парсера с корректным кодом
│   │   │   ├── expressions/
│   │   │   ├── statements/
│   │   │   ├── declarations/
│   │   │   └── full_programs/
│   │   └── invalid/           # Тесты парсера с синтаксическими ошибками
│   │       └── syntax_errors/
│   └── test_runner.py         # Автоматический запуск тестов
├── examples/
│   ├── hello.src              # Пример простой программы
│   └── factorial.src          # Пример с рекурсивной функцией
├── docs/
│   └── language_spec.md       # Формальная спецификация языка
├── README.md
├── pyproject.toml              # Конфигурация проекта
└── setup.py                    # Скрипт установки
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
# Создание и активация виртуального окружения (опционально, но рекомендуется)
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**Windows:**
```bash
# Создание и активация виртуального окружения (опционально, но рекомендуется)
python -m venv venv
venv\Scripts\activate
pip install -e .
```

## Быстрый старт

### Лексический анализ

```bash
# Запуск лексера на исходном файле
python -m src.lexer.scanner --input examples/hello.src --output tokens.txt

# Или через консольную команду (если настроено)
compiler lex --input examples/hello.src --output tokens.txt

# Пример вывода (tokens.txt):
# 1:1 KW_FN "fn"
# 1:4 IDENTIFIER "main"
# 1:8 LPAREN "("
# 1:9 RPAREN ")"
# 1:11 KW_VOID "void"
# 1:16 LBRACE "{"
# 2:5 KW_INT "int"
# 2:9 IDENTIFIER "counter"
# 2:16 ASSIGN "="
# 2:18 INT_LITERAL "42" 42
# 2:20 SEMICOLON ";"
# 3:1 RBRACE "}"
# 4:1 END_OF_FILE ""
```

### Синтаксический анализ (построение AST)

```bash
# Базовый запуск парсера (вывод в текстовом формате)
python src/main.py --input examples/hello.src

# Вывод с подробной информацией о токенах
python src/main.py --input examples/hello.src --verbose

# Сохранение AST в текстовый файл
python src/main.py --input examples/hello.src --output ast.txt

# Генерация DOT графа для визуализации
python src/main.py --input examples/hello.src --format dot --output ast.dot

# Конвертация DOT в PNG (требуется Graphviz)
dot -Tpng ast.dot -o ast.png

# Экспорт AST в JSON
python src/main.py --input examples/hello.src --format json --output ast.json
```

### Пример исходного файла

Создайте файл `examples/hello.src`:

```
fn main() void {
    int counter = 42;
    return counter;
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

### Пример вывода AST (JSON)

```json
{
  "type": "program",
  "line": 2,
  "column": 1,
  "declarations": [
    {
      "type": "function_decl",
      "line": 2,
      "column": 1,
      "name": "main",
      "return_type": "void",
      "body": {
        "type": "block",
        "line": 2,
        "column": 16,
        "statements": [
          {
            "type": "var_decl",
            "line": 3,
            "column": 5,
            "name": "counter",
            "var_type": "int",
            "initializer": {
              "type": "literal",
              "line": 3,
              "column": 18,
              "value": 42,
              "literal_type": "int"
            }
          },
          {
            "type": "return_stmt",
            "line": 4,
            "column": 5,
            "value": {
              "type": "identifier",
              "line": 4,
              "column": 12,
              "name": "counter"
            }
          }
        ]
      }
    }
  ]
}
```

## Тестирование

### Запуск всех тестов

```bash
# Запуск тестов лексера
python tests/test_runner.py

# Запуск тестов парсера
python tests/parser/test_parser.py

# Или с использованием pytest
pytest tests/ -v

# Запуск с отчётом о покрытии
pytest tests/ --cov=src --cov-report=term
```

### Набор тестов

**Тесты лексера:**
- Корректные тесты (20+): отдельные типы токенов, граничные случаи, комментарии, разные окончания строк
- Некорректные тесты (10+): недопустимые символы, незавершённые строки и комментарии, неправильно оформленные числа

**Тесты парсера:**
- Выражения: приоритет операторов, скобки, вызовы функций
- Операторы: if-else, while, for, return
- Объявления: функции с параметрами, переменные, структуры
- Полные программы: факториал, сумма чисел
- Синтаксические ошибки: пропущенные точки с запятой, незакрытые скобки

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

- **token.py**: Определяет класс Token и перечисление TokenType с более чем 40 категориями токенов
- **scanner.py**: Основная реализация сканера с отслеживанием позиции и поддержкой просмотра вперёд
- **errors.py**: Обработка ошибок с механизмами восстановления и понятными сообщениями

### Компоненты парсера

- **ast.py**: Иерархия классов для узлов AST (ProgramNode, FunctionDeclNode, BinaryExprNode и др.)
- **parser.py**: Рекурсивный парсер с методами для каждого правила грамматики
- **ast_printer.py**: Красивый вывод AST с отступами для визуального анализа
- **grammar.txt**: Полное описание грамматики в нотации EBNF

### Ключевые особенности

- **Типы токенов**: Классификация на основе перечислений с полным набором категорий
- **Отслеживание позиции**: Точное отслеживание строк и столбцов (нумерация с 1)
- **Извлечение литералов**: Типизированные значения для целых чисел, чисел с плавающей точкой, строк, булевых значений
- **Восстановление после ошибок**: Пропуск неверных токенов и продолжение сканирования
- **Приоритет операторов**: Правильная обработка через иерархию методов парсинга
- **Три формата вывода**: Текст для чтения, DOT для визуализации, JSON для машинной обработки

### Производительность

- Временная сложность лексера: O(n), где n - длина входных данных
- Временная сложность парсера: O(n) для LL(1) грамматики
- Использование памяти: Пропорционально размеру AST (не всего входа)
