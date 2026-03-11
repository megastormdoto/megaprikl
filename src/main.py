# src/main.py
import sys
import os
import argparse
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.scanner import Scanner
from src.parser.parser import Parser
from src.parser.ast_printer import ASTPrinter


def read_file(filename):
    """Читает содержимое файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)


def ast_to_json(node):
    """Конвертирует AST в JSON формат"""
    if node is None:
        return None

    # Базовый объект для всех узлов
    result = {
        'type': node.node_type.value,
        'line': node.line,
        'column': node.column
    }

    # Добавляем общие поля
    if hasattr(node, 'name') and node.name:
        result['name'] = node.name

    if hasattr(node, 'value') and node.value is not None:
        result['value'] = node.value

    if hasattr(node, 'operator') and node.operator:
        result['operator'] = node.operator

    # ProgramNode
    if hasattr(node, 'declarations') and node.declarations:
        result['declarations'] = [ast_to_json(d) for d in node.declarations]

    # FunctionDeclNode
    if hasattr(node, 'return_type') and node.return_type:
        result['return_type'] = node.return_type

    if hasattr(node, 'parameters') and node.parameters:
        result['parameters'] = [ast_to_json(p) for p in node.parameters]

    if hasattr(node, 'body') and node.body:
        result['body'] = ast_to_json(node.body)

    # VarDeclNode
    if hasattr(node, 'var_type') and node.var_type:
        result['var_type'] = node.var_type

    if hasattr(node, 'initializer') and node.initializer:
        result['initializer'] = ast_to_json(node.initializer)

    # StructDeclNode
    if hasattr(node, 'fields') and node.fields:
        result['fields'] = [ast_to_json(f) for f in node.fields]

    # ParameterNode
    if hasattr(node, 'param_type') and node.param_type:
        result['param_type'] = node.param_type

    # BlockNode
    if hasattr(node, 'statements') and node.statements:
        result['statements'] = [ast_to_json(s) for s in node.statements]

    # IfStmtNode
    if hasattr(node, 'condition') and node.condition:
        result['condition'] = ast_to_json(node.condition)

    if hasattr(node, 'then_branch') and node.then_branch:
        result['then_branch'] = ast_to_json(node.then_branch)

    if hasattr(node, 'else_branch') and node.else_branch:
        result['else_branch'] = ast_to_json(node.else_branch)

    # WhileStmtNode
    if hasattr(node, 'condition') and node.condition and not hasattr(node, 'then_branch'):
        result['condition'] = ast_to_json(node.condition)

    if hasattr(node, 'body') and node.body and not hasattr(node, 'return_type'):
        result['body'] = ast_to_json(node.body)

    # ForStmtNode
    if hasattr(node, 'init') and node.init:
        result['init'] = ast_to_json(node.init)

    if hasattr(node, 'condition') and node.condition and hasattr(node, 'init'):
        result['condition'] = ast_to_json(node.condition)

    if hasattr(node, 'update') and node.update:
        result['update'] = ast_to_json(node.update)

    # ReturnStmtNode
    if hasattr(node, 'value') and node.value and node.node_type.value == 'return_stmt':
        result['value'] = ast_to_json(node.value)

    # ExprStmtNode
    if hasattr(node, 'expression') and node.expression:
        result['expression'] = ast_to_json(node.expression)

    # BinaryExprNode
    if hasattr(node, 'left') and node.left:
        result['left'] = ast_to_json(node.left)

    if hasattr(node, 'right') and node.right:
        result['right'] = ast_to_json(node.right)

    # UnaryExprNode
    if hasattr(node, 'operand') and node.operand:
        result['operand'] = ast_to_json(node.operand)

    # LiteralNode
    if hasattr(node, 'literal_type') and node.literal_type:
        result['literal_type'] = node.literal_type

    # CallNode
    if hasattr(node, 'callee') and node.callee:
        result['callee'] = node.callee

    if hasattr(node, 'arguments') and node.arguments:
        result['arguments'] = [ast_to_json(a) for a in node.arguments]

    # AssignmentNode
    if hasattr(node, 'target') and node.target:
        result['target'] = node.target

    return result


def ast_to_dot(node, node_id=0, lines=None):
    """Конвертирует AST в формат DOT для Graphviz"""
    if lines is None:
        lines = ['digraph AST {', '  node [shape=box, style=filled, fillcolor=lightblue];']

    if node is None:
        return node_id, lines

    # Формируем метку узла
    label = node.node_type.value

    # Добавляем дополнительную информацию
    if hasattr(node, 'name') and node.name:
        label += f"\\n{node.name}"
    if hasattr(node, 'value') and node.value is not None:
        label += f"\\n{node.value}"
    if hasattr(node, 'var_type') and node.var_type:
        label += f"\\ntype: {node.var_type}"
    if hasattr(node, 'return_type') and node.return_type:
        label += f"\\nreturn: {node.return_type}"
    if hasattr(node, 'operator') and node.operator:
        label += f"\\nop: {node.operator}"
    if hasattr(node, 'literal_type') and node.literal_type:
        label += f"\\n({node.literal_type})"

    lines.append(f'  node{node_id} [label="{label}"];')
    current_id = node_id + 1

    # ProgramNode
    if hasattr(node, 'declarations') and node.declarations:
        for child in node.declarations:
            child_id, lines = ast_to_dot(child, current_id, lines)
            lines.append(f'  node{node_id} -> node{current_id};')
            current_id = child_id

    # FunctionDeclNode
    if hasattr(node, 'parameters') and node.parameters:
        for param in node.parameters:
            child_id, lines = ast_to_dot(param, current_id, lines)
            lines.append(f'  node{node_id} -> node{current_id} [label="param"];')
            current_id = child_id

    if hasattr(node, 'body') and node.body:
        child_id, lines = ast_to_dot(node.body, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="body"];')
        current_id = child_id

    # BlockNode
    if hasattr(node, 'statements') and node.statements:
        for i, stmt in enumerate(node.statements):
            child_id, lines = ast_to_dot(stmt, current_id, lines)
            lines.append(f'  node{node_id} -> node{current_id} [label="{i}"];')
            current_id = child_id

    # VarDeclNode
    if hasattr(node, 'initializer') and node.initializer:
        child_id, lines = ast_to_dot(node.initializer, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="init"];')
        current_id = child_id

    # IfStmtNode
    if hasattr(node, 'condition') and node.condition:
        child_id, lines = ast_to_dot(node.condition, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="if"];')
        current_id = child_id

    if hasattr(node, 'then_branch') and node.then_branch:
        child_id, lines = ast_to_dot(node.then_branch, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="then"];')
        current_id = child_id

    if hasattr(node, 'else_branch') and node.else_branch:
        child_id, lines = ast_to_dot(node.else_branch, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="else"];')
        current_id = child_id

    # WhileStmtNode
    if hasattr(node, 'condition') and node.condition and not hasattr(node, 'then_branch'):
        child_id, lines = ast_to_dot(node.condition, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="while"];')
        current_id = child_id

    if hasattr(node, 'body') and node.body and not hasattr(node, 'return_type'):
        child_id, lines = ast_to_dot(node.body, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="body"];')
        current_id = child_id

    # ForStmtNode
    if hasattr(node, 'init') and node.init:
        child_id, lines = ast_to_dot(node.init, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="init"];')
        current_id = child_id

    if hasattr(node, 'condition') and node.condition and hasattr(node, 'init'):
        child_id, lines = ast_to_dot(node.condition, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="cond"];')
        current_id = child_id

    if hasattr(node, 'update') and node.update:
        child_id, lines = ast_to_dot(node.update, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="update"];')
        current_id = child_id

    # ReturnStmtNode
    if hasattr(node, 'value') and node.value and node.node_type.value == 'return_stmt':
        child_id, lines = ast_to_dot(node.value, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="return"];')
        current_id = child_id

    # ExprStmtNode
    if hasattr(node, 'expression') and node.expression:
        child_id, lines = ast_to_dot(node.expression, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id};')
        current_id = child_id

    # BinaryExprNode
    if hasattr(node, 'left') and node.left:
        child_id, lines = ast_to_dot(node.left, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="left"];')
        current_id = child_id

    if hasattr(node, 'right') and node.right:
        child_id, lines = ast_to_dot(node.right, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id} [label="right"];')
        current_id = child_id

    # UnaryExprNode
    if hasattr(node, 'operand') and node.operand:
        child_id, lines = ast_to_dot(node.operand, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id};')
        current_id = child_id

    # CallNode
    if hasattr(node, 'arguments') and node.arguments:
        for i, arg in enumerate(node.arguments):
            child_id, lines = ast_to_dot(arg, current_id, lines)
            lines.append(f'  node{node_id} -> node{current_id} [label="arg{i}"];')
            current_id = child_id

    # AssignmentNode
    if hasattr(node, 'value') and node.value and node.node_type.value == 'assignment':
        child_id, lines = ast_to_dot(node.value, current_id, lines)
        lines.append(f'  node{node_id} -> node{current_id};')
        current_id = child_id

    return current_id, lines


def main():
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(description='MiniCompiler - Парсер языка')
    parser.add_argument('--input', '-i', required=True, help='Входной файл с исходным кодом')
    parser.add_argument('--format', '-f', choices=['text', 'dot', 'json'],
                        default='text', help='Формат вывода AST (по умолчанию: text)')
    parser.add_argument('--output', '-o', help='Выходной файл (если не указан, вывод в консоль)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Показывать токены')

    args = parser.parse_args()

    print(f"Чтение файла: {args.input}")
    source = read_file(args.input)

    # Лексический анализ
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    if args.verbose:
        print("\nТокены:")
        for token in tokens:
            print(f"  {token}")

    # Синтаксический анализ
    parser = Parser(tokens)
    ast = parser.parse()

    if parser.errors:
        print("\nОшибки парсера:")
        for error in parser.errors:
            print(f"  {error}")
        sys.exit(1)

    # Вывод AST в нужном формате
    if args.format == 'text':
        print("\nAST дерево:")
        printer = ASTPrinter()
        output = printer.print(ast)
    elif args.format == 'dot':
        print("\nГенерация DOT графа...")
        _, lines = ast_to_dot(ast)
        lines.append('}')
        output = '\n'.join(lines)
    else:  # json
        print("\nГенерация JSON...")
        json_data = ast_to_json(ast)
        output = json.dumps(json_data, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\nРезультат сохранен в {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()