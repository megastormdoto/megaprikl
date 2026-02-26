```markdown
# Спецификация языка MiniCompiler

## 1. Лексическая структура

### 1.1. Пробельные символы
Следующие символы игнорируются лексером (служат только для разделения токенов):
- Пробел (` `)
- Табуляция (`\t`)
- Перевод строки (`\n`)
- Возврат каретки (`\r`)

### 1.2. Комментарии
- **Однострочные:** `//` - всё до конца строки игнорируется
- **Многострочные:** `/* ... */` - поддерживается вложенность

### 1.3. Идентификаторы
- Последовательность букв (латиница), цифр и символа подчёркивания `_`
- Не могут начинаться с цифры
- Максимальная длина: 255 символов
- Регистрозависимые: `count`, `Count` и `COUNT` - разные идентификаторы

### 1.4. Ключевые слова
```
if     else   while  for    int    float  bool
return true   false  void   struct fn
```

### 1.5. Литералы
- **Целые числа:** последовательность десятичных цифр (0-9)
- **Числа с плавающей точкой:** целая часть, точка, дробная часть (например, 3.14)
- **Строки:** последовательность символов в двойных кавычках (например, "hello")
- **Булевы:** `true`, `false`

### 1.6. Операторы
- **Арифметические:** `+` `-` `*` `/` `%`
- **Сравнения:** `==` `!=` `<` `<=` `>` `>=`
- **Логические:** `&&` `||` `!`

### 1.7. Разделители
```
( ) { } [ ] ; ,
```

## 2. Грамматика (EBNF)

```
Program           = { FunctionDefinition | StructDefinition }

FunctionDefinition = "fn", Identifier, "(", [ ParameterList ], ")", Block
ParameterList     = Parameter, { ",", Parameter }
Parameter         = TypeSpecifier, Identifier
TypeSpecifier     = "int" | "float" | "bool" | "void" | "struct", Identifier

StructDefinition  = "struct", Identifier, "{", { StructField }, "}"
StructField       = TypeSpecifier, Identifier, ";"

Block             = "{", { Statement }, "}"

Statement         = VariableDeclaration
                  | AssignmentStatement
                  | IfStatement
                  | WhileStatement
                  | ForStatement
                  | ReturnStatement
                  | ExpressionStatement
                  | Block

VariableDeclaration = TypeSpecifier, Identifier, [ "=", Expression ], ";"
AssignmentStatement = Expression, "=", Expression, ";"
IfStatement        = "if", "(", Expression, ")", Statement, [ "else", Statement ]
WhileStatement     = "while", "(", Expression, ")", Statement
ForStatement       = "for", "(", [ VariableDeclaration | ExpressionStatement ], ";",
                     [ Expression ], ";", [ ExpressionStatement ], ")", Statement
ReturnStatement    = "return", [ Expression ], ";"
ExpressionStatement = [ Expression ], ";"

Expression         = LogicalOrExpression
LogicalOrExpression = LogicalAndExpression, { "||", LogicalAndExpression }
LogicalAndExpression = EqualityExpression, { "&&", EqualityExpression }
EqualityExpression = RelationalExpression, { ("==" | "!="), RelationalExpression }
RelationalExpression = AdditiveExpression, { ("<" | "<=" | ">" | ">="), AdditiveExpression }
AdditiveExpression = MultiplicativeExpression, { ("+" | "-"), MultiplicativeExpression }
MultiplicativeExpression = UnaryExpression, { ("*" | "/" | "%"), UnaryExpression }
UnaryExpression    = [ "!" | "-" ], PrimaryExpression
PrimaryExpression  = Identifier
                   | Literal
                   | "(", Expression, ")"
                   | FunctionCall

FunctionCall       = Identifier, "(", [ ArgumentList ], ")"
ArgumentList       = Expression, { ",", Expression }

Literal            = INT_LITERAL | FLOAT_LITERAL | STRING_LITERAL | BOOL_LITERAL
Identifier         = IDENTIFIER
```