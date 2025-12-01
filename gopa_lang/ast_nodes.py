"""AST node definitions for Gopa."""

from abc import ABC
from typing import List, Optional


class ASTNode(ABC):
    """Base class for all AST nodes."""
    pass


class Statement(ASTNode):
    """Base class for statements."""
    pass


class Expression(ASTNode):
    """Base class for expressions."""
    pass


class NumberLiteral(Expression):
    def __init__(self, value: float):
        self.value = value


class StringLiteral(Expression):
    def __init__(self, value: str):
        self.value = value


class BooleanLiteral(Expression):
    def __init__(self, value: bool):
        self.value = value


class NothingLiteral(Expression):
    pass


class PiLiteral(Expression):
    pass


class Identifier(Expression):
    def __init__(self, name: str):
        self.name = name


class BinaryOp(Expression):
    def __init__(self, left: Expression, op: str, right: Expression):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(Expression):
    def __init__(self, op: str, operand: Expression):
        self.op = op
        self.operand = operand


class PropertyAccess(Expression):
    def __init__(self, obj: Expression, prop: str):
        self.obj = obj
        self.prop = prop


class IndexAccess(Expression):
    def __init__(self, obj: Expression, index: Expression):
        self.obj = obj
        self.index = index


class ListLiteral(Expression):
    def __init__(self, elements: List[Expression]):
        self.elements = elements


class DictionaryLiteral(Expression):
    def __init__(self, pairs: List[tuple]):
        self.pairs = pairs


class ObjectLiteral(Expression):
    def __init__(self, properties: List[tuple]):
        self.properties = properties


class FunctionCall(Expression):
    def __init__(self, name: str, args: List[Expression]):
        self.name = name
        self.args = args


class Assignment(Statement):
    def __init__(self, target: Expression, value: Expression):
        self.target = target
        self.value = value


class Mutation(Statement):
    def __init__(self, target: Expression, op: str, value: Optional[Expression] = None):
        self.target = target
        self.op = op
        self.value = value


class SayStatement(Statement):
    def __init__(self, parts: List[Expression]):
        self.parts = parts


class PrintStatement(Statement):
    def __init__(self, expr: Expression):
        self.expr = expr


class ClearScreen(Statement):
    pass


class ShowTable(Statement):
    def __init__(self, headers: List[str], rows: Expression):
        self.headers = headers
        self.rows = rows


class AskStatement(Statement):
    def __init__(self, prompt: str, var_name: str, ask_type: str = "string"):
        self.prompt = prompt
        self.var_name = var_name
        self.ask_type = ask_type


class IfStatement(Statement):
    def __init__(self, condition: Expression, then_block: List[Statement], else_block: Optional[List[Statement]] = None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class RepeatForever(Statement):
    def __init__(self, body: List[Statement]):
        self.body = body


class RepeatTimes(Statement):
    def __init__(self, count: Expression, body: List[Statement]):
        self.count = count
        self.body = body


class RepeatUntil(Statement):
    def __init__(self, condition: Expression, body: List[Statement]):
        self.condition = condition
        self.body = body


class DoUntil(Statement):
    def __init__(self, body: List[Statement], condition: Expression):
        self.body = body
        self.condition = condition


class BreakStatement(Statement):
    pass


class ContinueStatement(Statement):
    pass


class StopStatement(Statement):
    pass


class FunctionDef(Statement):
    def __init__(self, name: str, params: List[str], body: List[Statement], closure_env: Optional[dict] = None):
        self.name = name
        self.params = params
        self.body = body
        self.closure_env = closure_env


class ReturnStatement(Statement):
    def __init__(self, value: Optional[Expression] = None):
        self.value = value


class MatchStatement(Statement):
    def __init__(self, expr: Expression, cases: List[tuple]):
        self.expr = expr
        self.cases = cases


class ListAdd(Statement):
    def __init__(self, list_expr: Expression, value: Expression):
        self.list_expr = list_expr
        self.value = value


class ListRemove(Statement):
    def __init__(self, list_expr: Expression, value: Optional[Expression] = None, index: Optional[Expression] = None):
        self.list_expr = list_expr
        self.value = value
        self.index = index


class ListSort(Statement):
    def __init__(self, list_expr: Expression):
        self.list_expr = list_expr


class ListReverse(Statement):
    def __init__(self, list_expr: Expression):
        self.list_expr = list_expr


class ListShuffle(Statement):
    def __init__(self, list_expr: Expression):
        self.list_expr = list_expr


class FindExpression(Expression):
    def __init__(self, value: Expression, in_expr: Expression):
        self.value = value
        self.in_expr = in_expr


class FilterExpression(Expression):
    def __init__(self, list_expr: Expression, condition: Expression):
        self.list_expr = list_expr
        self.condition = condition


class MapExpression(Expression):
    def __init__(self, list_expr: Expression, transform: Expression):
        self.list_expr = list_expr
        self.transform = transform


class StringSplit(Expression):
    def __init__(self, string: Expression, delimiter: str):
        self.string = string
        self.delimiter = delimiter


class StringJoin(Expression):
    def __init__(self, list_expr: Expression, delimiter: str):
        self.list_expr = list_expr
        self.delimiter = delimiter


class StringReplace(Expression):
    def __init__(self, string: Expression, old: str, new: str):
        self.string = string
        self.old = old
        self.new = new


class StringFind(Expression):
    def __init__(self, string: Expression, pattern: str):
        self.string = string
        self.pattern = pattern


class StringSlice(Expression):
    def __init__(self, string: Expression, start: Expression, end: Expression):
        self.string = string
        self.start = start
        self.end = end


class GetRequest(Expression):
    def __init__(self, url: str, params: dict):
        self.url = url
        self.params = params


class PostRequest(Expression):
    def __init__(self, url: str, params: dict):
        self.url = url
        self.params = params


class WriteFile(Statement):
    def __init__(self, content: Expression, filename: str):
        self.content = content
        self.filename = filename


class ReadFile(Expression):
    def __init__(self, filename: str):
        self.filename = filename


class CreateCanvas(Expression):
    def __init__(self, width: Expression, height: Expression):
        self.width = width
        self.height = height


class DrawCircle(Statement):
    def __init__(self, x: Expression, y: Expression, size: Expression, color: str):
        self.x = x
        self.y = y
        self.size = size
        self.color = color


class DrawRectangle(Statement):
    def __init__(self, x1: Expression, y1: Expression, x2: Expression, y2: Expression, color: str):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color


class DrawLine(Statement):
    def __init__(self, x1: Expression, y1: Expression, x2: Expression, y2: Expression, color: str):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color


class DrawText(Statement):
    def __init__(self, text: Expression, x: Expression, y: Expression, size: Expression, color: str):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.color = color


class WhenMouseClicks(Statement):
    def __init__(self, canvas: Expression, body: List[Statement]):
        self.canvas = canvas
        self.body = body


class WaitStatement(Statement):
    def __init__(self, seconds: Expression):
        self.seconds = seconds


class AfterStatement(Statement):
    def __init__(self, seconds: Expression, body: List[Statement]):
        self.seconds = seconds
        self.body = body


class EveryStatement(Statement):
    def __init__(self, seconds: Expression, body: List[Statement]):
        self.seconds = seconds
        self.body = body


class UseStatement(Statement):
    def __init__(self, package_name: str):
        self.package_name = package_name


class InstallStatement(Statement):
    def __init__(self, package_name: str):
        self.package_name = package_name


class UsePython(Statement):
    def __init__(self, module_name: str, alias: str):
        self.module_name = module_name
        self.alias = alias


class PythonCall(Expression):
    def __init__(self, module_attr: str, args: List[Expression]):
        self.module_attr = module_attr
        self.args = args


class ServerBlock(Statement):
    def __init__(self, port: Expression, handlers: List[tuple]):
        self.port = port
        self.handlers = handlers


class JobStatement(Statement):
    def __init__(self, name: str, seconds: Expression, body: List[Statement]):
        self.name = name
        self.seconds = seconds
        self.body = body


class StopJob(Statement):
    def __init__(self, name: str):
        self.name = name


class CronStatement(Statement):
    def __init__(self, schedule: str, body: List[Statement]):
        self.schedule = schedule
        self.body = body


class Program(ASTNode):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

