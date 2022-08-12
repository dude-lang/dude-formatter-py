from dude_ast import *

space = '  '


def format_expression(expression: Expression, ctx: Context) -> str:
    def format_condition(e):
        return '{} {} {}'.format(*[format_expression(x, ctx) for x in [e.left, e.operator, e.right]])

    def format_nested_expression(e):
        return '({})'.format(format_expression(e.expression, ctx))

    def format_list(e):
        return '[{}]'.format(','.join([format_expression(x, ctx) for x in e.elements]))

    def format_sequence(e):
        return '[{}:{}{}]'.format(format_expression(e.start, ctx),
                                  format_expression(e.stop, ctx),
                                  '' if e.step else ':{}'.format(format_expression(e.step, ctx)))

    lookup = {
        EmptyStatement:   lambda x: '',
        Null:             lambda x: 'null',
        Number:           lambda x: str(x.number),
        Identifier:       lambda x: str(x.name),
        Boolean:          lambda x: str(x.boolean),
        String:           lambda x: str(x.string),
        Character:        lambda x: str(x.char),
        Operator:         lambda x: str(x.operator),
        Condition:        format_condition,
        NestedExpression: format_nested_expression,
        List:             format_list,
        Sequence:         format_sequence
    }

    t = type(expression)
    if t in lookup:
        return lookup[t](expression)

    return str(expression)


def format_statement(statement: Statement, ctx: Context) -> str:
    indent = space * ctx.level
    indent1 = space * (ctx.level + 1)

    def format_assignment_statement(s):
        return '{}{} = {}\n'.format(indent, s.var.name, format_expression(s.expression, ctx))

    def format_return_statement(s):
        return f'{indent}ret\n' if not s.expression else '{}ret {}\n'.format(indent,
                                                                             format_expression(s.expression, ctx))

    def format_structure_statement(s):
        return '{}dat {}\n{}{}\n{}end\n'.format(
            indent,
            s.name.name,
            indent1,
            ','.join([format_expression(x, ctx) for x in s.members]),
            indent)

    def format_while_statement(s):
        return '{}while {}\n{}{}end\n'.format(
            indent,
            format_expression(s.condition, ctx),
            ''.join([format_statement(x, ctx) for x in s.body]),
            indent)

    def format_for_statement(s):
        return '{}for {} in {}\n{}{}end\n'.format(
            indent,
            s.index.name,
            format_expression(s.sequence, ctx),
            ''.join([format_statement(x, ctx) for x in s.body]),
            indent)

    def format_function_statement(s):
        return '{}fun {}({})\n{}{}end\n'.format(
            indent,
            s.name.name,
            ','.join([format_expression(x, ctx) for x in s.arguments]),
            ''.join([format_statement(x, ctx) for x in s.body]),
            indent)

    def format_condition_statement(s):
        _if = '{} {}\n{}'.format(
            'if',
            format_expression(s.if_condition, ctx),
            ''.join([format_statement(x, ctx) for x in s.if_body]))

        _elif = '' if not s.elif_condition else '{} {}\n{}'.format(
            'elif',
            format_expression(s.elif_condition, ctx),
            ''.join([format_statement(x, ctx) for x in s.elif_body]))

        _else = '' if not s.else_body else '{}\n{}'.format(
            'else',
            ''.join([format_statement(x, ctx) for x in s.else_body]))

        return f'{indent + _if}{indent + _elif}{indent + _else}{indent}end\n'

    lookup = {
        AssignmentStatement:  format_assignment_statement,
        ReturnStatement:      format_return_statement,
        StructureStatement:   format_structure_statement,
        WhileLoopStatement:   format_while_statement,
        ForLoopStatement:     format_for_statement,
        FunctionStatement:    format_function_statement,
        ConditionalStatement: format_condition_statement,
    }

    t = type(statement)
    if t in lookup:
        ctx.level += 1
        stm = lookup[t](statement)
        ctx.level -= 1
        return stm

    return str(statement)


def formatit(ast: Program, ctx: Context = None) -> str:
    formatted = ''
    is_assignement = False

    def assignment_before() -> bool:
        t = type(statement)

        return not is_assignement or (t == AssignmentStatement and not is_assignement) or (is_assignement and t != AssignmentStatement)

    for statement in ast.statements:
        if assignment_before():
            formatted += '\n\n'

        formatted += format_statement(statement, ctx)
        is_assignement = type(statement) == AssignmentStatement

    return formatted
