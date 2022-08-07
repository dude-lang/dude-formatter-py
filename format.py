import os
import sys

sys.path.append(str(os.path.dirname(__file__) + '\\..'))

from dude_ast import *


def format_expression(expression: Expression, ctx: Context) -> str:
    if isinstance(expression, Number):
        return str(expression.number)
    elif isinstance(expression, Identifier):
        return expression.name
    elif isinstance(expression, Boolean):
        return str(expression.boolean)
    elif isinstance(expression, String):
        return expression.string
    elif isinstance(expression, Character):
        return expression.char
    elif isinstance(expression, Operator):
        return expression.operator
    elif isinstance(expression, Condition):
        return '{} {} {}'.format(
            *[format_expression(x, ctx) for x in [expression.left, expression.operator, expression.right]])
    elif isinstance(expression, NestedExpression):
        return '({})'.format(format_expression(expression.expression, ctx))

    return str(expression)


def format_statement(statement: Statement, ctx: Context) -> str:
    if isinstance(statement, AssignmentStatement):
        return '\n{} = {}\n'.format(statement.var.name, format_expression(statement.expression, ctx))

    elif isinstance(statement, ReturnStatement):
        return 'ret' if not statement.expression else 'ret {}'.format(format_expression(statement.expression, ctx))

    elif isinstance(statement, FunctionStatement):
        return 'fun {}({})\n{}\nend\n\n'.format(
            statement.name.name,
            ','.join([format_expression(x, ctx) for x in statement.arguments]),
            '\n'.join([format_statement(x, ctx) for x in statement.body]))

    elif isinstance(statement, ConditionalStatement):
        _if = '{:6s} {} {}'.format(
            'if',
            format_expression(statement.if_condition, ctx),
            '\n'.join([format_statement(x, ctx) for x in statement.if_body]))

        _elif = '' if not statement.elif_condition else '{:6s} {} {}'.format(
            'elif',
            format_expression(statement.elif_condition, ctx),
            '\n'.join([format_statement(x, ctx) for x in statement.elif_body]))

        _else = '' if not statement.else_body else '{:6s} {}'.format(
            'else',
            '\n'.join([format_statement(x, ctx) for x in statement.else_body]))

        return f'{_if}\n{_elif}\n{_else}\nend\n\n'

    return str(statement)


def formatit(ast: Program, ctx: Context = None) -> str:
    formatted = ''
    for statement in ast.statements:
        formatted += format_statement(statement, ctx)

    return formatted
