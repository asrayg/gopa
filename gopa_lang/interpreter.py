"""Interpreter for Gopa AST."""

import sys
import json
import time
from typing import Any, Optional, List, Dict
from .runtime import Runtime
from .permissions import Permissions
from .builtin_stdlib import BUILTINS
from .ast_nodes import *


class ControlSignal(Exception):
    """Base class for control flow signals."""
    pass


class ReturnSignal(ControlSignal):
    def __init__(self, value: Any):
        self.value = value


class BreakSignal(ControlSignal):
    pass


class ContinueSignal(ControlSignal):
    pass


class StopSignal(ControlSignal):
    pass


class Interpreter:
    """Interpreter for executing Gopa AST."""

    def __init__(self, permissions: Permissions, output_stream=None, input_stream=None, debug: bool = False):
        self.permissions = permissions
        self.output_stream = output_stream or sys.stdout
        self.input_stream = input_stream or sys.stdin
        self.debug = debug
        self.runtime = Runtime()
        self.graphics = None
        self.scheduler = None
        self.python_modules = {}

        for name, func in BUILTINS.items():
            self.runtime.define_function(name, func)

    def evaluate(self, node: Expression) -> Any:
        """Evaluate an expression node."""
        try:
            if isinstance(node, NumberLiteral):
                return node.value
            elif isinstance(node, StringLiteral):
                return node.value
            elif isinstance(node, BooleanLiteral):
                return node.value
            elif isinstance(node, NothingLiteral):
                return None
            elif isinstance(node, PiLiteral):
                return 3.141592653589793
            elif isinstance(node, Identifier):
                return self.runtime.get(node.name)
            elif isinstance(node, BinaryOp):
                return self.evaluate_binary_op(node)
            elif isinstance(node, UnaryOp):
                return self.evaluate_unary_op(node)
            elif isinstance(node, PropertyAccess):
                obj = self.evaluate(node.obj)
                if obj is None:
                    raise RuntimeError(f"Cannot access property '{node.prop}' on nothing")
                if isinstance(obj, dict):
                    return obj.get(node.prop, None)
                elif hasattr(obj, node.prop):
                    return getattr(obj, node.prop)
                else:
                    return None
            elif isinstance(node, IndexAccess):
                obj = self.evaluate(node.obj)
                index = self.evaluate(node.index)
                if isinstance(obj, list):
                    if isinstance(index, int) and 0 <= index < len(obj):
                        return obj[index]
                    return None
                elif isinstance(obj, dict):
                    return obj.get(index, None)
                else:
                    raise RuntimeError(f"Cannot index {type(obj)}")
            elif isinstance(node, ListLiteral):
                return [self.evaluate(elem) for elem in node.elements]
            elif isinstance(node, DictionaryLiteral):
                result = {}
                for key, value_expr in node.pairs:
                    result[key] = self.evaluate(value_expr)
                return result
            elif isinstance(node, ObjectLiteral):
                result = {}
                for name, value_expr in node.properties:
                    result[name] = self.evaluate(value_expr)
                return result
            elif isinstance(node, FunctionCall):
                return self.evaluate_function_call(node)
            elif isinstance(node, FindExpression):
                return self.evaluate_find(node)
            elif isinstance(node, FilterExpression):
                return self.evaluate_filter(node)
            elif isinstance(node, MapExpression):
                return self.evaluate_map(node)
            elif isinstance(node, StringSplit):
                return self.evaluate_string_split(node)
            elif isinstance(node, StringJoin):
                return self.evaluate_string_join(node)
            elif isinstance(node, StringReplace):
                return self.evaluate_string_replace(node)
            elif isinstance(node, StringFind):
                return self.evaluate_string_find(node)
            elif isinstance(node, StringSlice):
                return self.evaluate_string_slice(node)
            elif isinstance(node, GetRequest):
                return self.evaluate_get_request(node)
            elif isinstance(node, PostRequest):
                return self.evaluate_post_request(node)
            elif isinstance(node, ReadFile):
                return self.evaluate_read_file(node)
            elif isinstance(node, CreateCanvas):
                return self.evaluate_create_canvas(node)
            elif isinstance(node, PythonCall):
                return self.evaluate_python_call(node)
            else:
                raise RuntimeError(f"Unknown expression type: {type(node)}")
        except RuntimeError as e:
            if self.debug:
                raise
            print(str(e), file=self.output_stream)
            return None

    def evaluate_binary_op(self, node: BinaryOp) -> Any:
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.op == "plus":
            return left + right
        elif node.op == "minus":
            return left - right
        elif node.op == "times":
            return left * right
        elif node.op == "divided_by":
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        elif node.op == "equals":
            return left == right
        elif node.op == "does_not_equal":
            return left != right
        elif node.op == "is_greater_than":
            return left > right
        elif node.op == "is_less_than":
            return left < right
        elif node.op == "is_at_least":
            return left >= right
        elif node.op == "is_at_most":
            return left <= right
        elif node.op == "and":
            return left and right
        elif node.op == "or":
            return left or right
        else:
            raise RuntimeError(f"Unknown binary operator: {node.op}")

    def evaluate_unary_op(self, node: UnaryOp) -> Any:
        operand = self.evaluate(node.operand)

        if node.op == "not":
            return not operand
        else:
            raise RuntimeError(f"Unknown unary operator: {node.op}")

    def evaluate_function_call(self, node: FunctionCall) -> Any:
        if node.name in BUILTINS:
            args = [self.evaluate(arg) for arg in node.args]
            return BUILTINS[node.name](*args)

        try:
            func = self.runtime.get_function(node.name)
            args = [self.evaluate(arg) for arg in node.args]

            func_runtime = self.runtime.child_scope()
            old_runtime = self.runtime
            self.runtime = func_runtime

            for i, param in enumerate(func.params):
                if i < len(args):
                    func_runtime.set(param, args[i])
                else:
                    func_runtime.set(param, None)

            try:
                for stmt in func.body:
                    self.execute(stmt)
                return None
            except ReturnSignal as ret:
                return ret.value
            finally:
                self.runtime = old_runtime
        except NameError:
            raise RuntimeError(f"Function '{node.name}' not defined")

    def evaluate_find(self, node: FindExpression) -> bool:
        value = self.evaluate(node.value)
        container = self.evaluate(node.in_expr)

        if isinstance(container, list):
            return value in container
        elif isinstance(container, str):
            return str(value) in container
        elif isinstance(container, dict):
            return value in container.values() or value in container
        else:
            return False

    def evaluate_filter(self, node: FilterExpression) -> List:
        list_expr = self.evaluate(node.list_expr)
        if not isinstance(list_expr, list):
            raise RuntimeError("filter expects a list")

        result = []
        for item in list_expr:
            old_item = self.runtime.variables.get('item')
            self.runtime.set('item', item)
            condition = self.evaluate(node.condition)
            if old_item is not None:
                self.runtime.set('item', old_item)
            else:
                self.runtime.variables.pop('item', None)

            if condition:
                result.append(item)

        return result

    def evaluate_map(self, node: MapExpression) -> List:
        list_expr = self.evaluate(node.list_expr)
        if not isinstance(list_expr, list):
            raise RuntimeError("map expects a list")

        result = []
        for item in list_expr:
            old_item = self.runtime.variables.get('item')
            self.runtime.set('item', item)
            transformed = self.evaluate(node.transform)
            if old_item is not None:
                self.runtime.set('item', old_item)
            else:
                self.runtime.variables.pop('item', None)
            result.append(transformed)

        return result

    def evaluate_string_split(self, node: StringSplit) -> List[str]:
        string = self.evaluate(node.string)
        if not isinstance(string, str):
            string = str(string)
        return string.split(node.delimiter)

    def evaluate_string_join(self, node: StringJoin) -> str:
        list_expr = self.evaluate(node.list_expr)
        if not isinstance(list_expr, list):
            raise RuntimeError("join expects a list")
        return node.delimiter.join(str(item) for item in list_expr)

    def evaluate_string_replace(self, node: StringReplace) -> str:
        string = self.evaluate(node.string)
        if not isinstance(string, str):
            string = str(string)
        return string.replace(node.old, node.new)

    def evaluate_string_find(self, node: StringFind) -> bool:
        string = self.evaluate(node.string)
        if not isinstance(string, str):
            string = str(string)
        return node.pattern in string

    def evaluate_string_slice(self, node: StringSlice) -> str:
        string = self.evaluate(node.string)
        if not isinstance(string, str):
            string = str(string)
        start = int(self.evaluate(node.start))
        end = int(self.evaluate(node.end))
        return string[start:end]

    def evaluate_get_request(self, node: GetRequest) -> Any:
        self.permissions.check_network()

        try:
            import requests
        except ImportError:
            raise RuntimeError("requests library not installed")

        url = node.url
        params = {}
        for key, value_expr in node.params.items():
            params[key] = self.evaluate(value_expr)

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json() if response.content else {}
        except Exception as e:
            if self.debug:
                raise
            raise RuntimeError(f"Network request failed: {str(e)}")

    def evaluate_post_request(self, node: PostRequest) -> Any:
        self.permissions.check_network()

        try:
            import requests
        except ImportError:
            raise RuntimeError("requests library not installed")

        url = node.url
        data = {}
        for key, value_expr in node.params.items():
            data[key] = self.evaluate(value_expr)

        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            return response.json() if response.content else {}
        except Exception as e:
            if self.debug:
                raise
            raise RuntimeError(f"Network request failed: {str(e)}")

    def evaluate_read_file(self, node: ReadFile) -> str:
        self.permissions.check_files()

        try:
            with open(node.filename, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            if self.debug:
                raise
            raise RuntimeError(f"Failed to read file: {str(e)}")

    def evaluate_create_canvas(self, node: CreateCanvas) -> Any:
        self.permissions.check_graphics()

        width = int(self.evaluate(node.width))
        height = int(self.evaluate(node.height))

        if self.graphics:
            return self.graphics.create_canvas(width, height)
        return {"type": "canvas", "width": width, "height": height}

    def evaluate_python_call(self, node: PythonCall) -> Any:
        self.permissions.check_python_ffi()

        parts = node.module_attr.split('.')
        if len(parts) < 2:
            raise RuntimeError("python.call requires 'module.attr' format")

        module_name = parts[0]
        attr_name = '.'.join(parts[1:])

        ALLOWED_MODULES = {'math', 'random', 'datetime', 're'}
        if module_name not in ALLOWED_MODULES:
            raise RuntimeError(f"Module '{module_name}' not in allowlist")

        if module_name not in self.python_modules:
            if module_name == 'math':
                import math
                self.python_modules['math'] = math
            elif module_name == 'random':
                import random
                self.python_modules['random'] = random
            elif module_name == 'datetime':
                import datetime
                self.python_modules['datetime'] = datetime
            elif module_name == 're':
                import re
                self.python_modules['re'] = re

        module = self.python_modules[module_name]

        attr = module
        for part in attr_name.split('.'):
            attr = getattr(attr, part)

        if not callable(attr):
            raise RuntimeError(f"'{node.module_attr}' is not callable")

        args = [self.evaluate(arg) for arg in node.args]
        converted_args = []
        for arg in args:
            if isinstance(arg, dict):
                converted_args.append(arg)
            elif isinstance(arg, list):
                converted_args.append(arg)
            else:
                converted_args.append(arg)

        try:
            result = attr(*converted_args)

            if isinstance(result, (int, float, str, bool)):
                return result
            elif result is None:
                return None
            elif isinstance(result, (list, tuple)):
                return list(result)
            elif isinstance(result, dict):
                return dict(result)
            else:
                raise RuntimeError(f"Cannot return {type(result)} from Python call")
        except Exception as e:
            if self.debug:
                raise
            raise RuntimeError(f"Python call failed: {str(e)}")

    def execute(self, node: Statement) -> Any:
        """Execute a statement node."""
        try:
            if isinstance(node, Assignment):
                return self.execute_assignment(node)
            elif isinstance(node, Mutation):
                return self.execute_mutation(node)
            elif isinstance(node, SayStatement):
                return self.execute_say(node)
            elif isinstance(node, PrintStatement):
                return self.execute_print(node)
            elif isinstance(node, ClearScreen):
                return self.execute_clear_screen(node)
            elif isinstance(node, ShowTable):
                return self.execute_show_table(node)
            elif isinstance(node, AskStatement):
                return self.execute_ask(node)
            elif isinstance(node, IfStatement):
                return self.execute_if(node)
            elif isinstance(node, RepeatForever):
                return self.execute_repeat_forever(node)
            elif isinstance(node, RepeatTimes):
                return self.execute_repeat_times(node)
            elif isinstance(node, RepeatUntil):
                return self.execute_repeat_until(node)
            elif isinstance(node, DoUntil):
                return self.execute_do_until(node)
            elif isinstance(node, BreakStatement):
                raise BreakSignal()
            elif isinstance(node, ContinueStatement):
                raise ContinueSignal()
            elif isinstance(node, StopStatement):
                raise StopSignal()
            elif isinstance(node, FunctionDef):
                return self.execute_function_def(node)
            elif isinstance(node, ReturnStatement):
                return self.execute_return(node)
            elif isinstance(node, MatchStatement):
                return self.execute_match(node)
            elif isinstance(node, ListAdd):
                return self.execute_list_add(node)
            elif isinstance(node, ListRemove):
                return self.execute_list_remove(node)
            elif isinstance(node, ListSort):
                return self.execute_list_sort(node)
            elif isinstance(node, ListReverse):
                return self.execute_list_reverse(node)
            elif isinstance(node, ListShuffle):
                return self.execute_list_shuffle(node)
            elif isinstance(node, WriteFile):
                return self.execute_write_file(node)
            elif isinstance(node, DrawCircle):
                return self.execute_draw_circle(node)
            elif isinstance(node, DrawRectangle):
                return self.execute_draw_rectangle(node)
            elif isinstance(node, DrawLine):
                return self.execute_draw_line(node)
            elif isinstance(node, DrawText):
                return self.execute_draw_text(node)
            elif isinstance(node, WhenMouseClicks):
                return self.execute_when_mouse_clicks(node)
            elif isinstance(node, WaitStatement):
                return self.execute_wait(node)
            elif isinstance(node, AfterStatement):
                return self.execute_after(node)
            elif isinstance(node, EveryStatement):
                return self.execute_every(node)
            elif isinstance(node, UseStatement):
                return self.execute_use(node)
            elif isinstance(node, InstallStatement):
                return self.execute_install(node)
            elif isinstance(node, UsePython):
                return self.execute_use_python(node)
            elif isinstance(node, ServerBlock):
                return self.execute_server(node)
            elif isinstance(node, JobStatement):
                return self.execute_job(node)
            elif isinstance(node, StopJob):
                return self.execute_stop_job(node)
            elif isinstance(node, CronStatement):
                return self.execute_cron(node)
            elif isinstance(node, FunctionCall):
                return self.evaluate_function_call(node)
            else:
                raise RuntimeError(f"Unknown statement type: {type(node)}")
        except (BreakSignal, ContinueSignal, StopSignal, ReturnSignal) as e:
            raise
        except RuntimeError as e:
            if self.debug:
                raise
            print(str(e), file=self.output_stream)
            return None

    def execute_assignment(self, node: Assignment):
        value = self.evaluate(node.value)
        self.set_target(node.target, value)

    def execute_mutation(self, node: Mutation):
        if node.op == "becomes":
            value = self.evaluate(node.value)
            self.set_target(node.target, value)
        elif node.op == "increase":
            increment = self.evaluate(node.value)
            current = self.get_target(node.target)
            self.set_target(node.target, current + increment)
        elif node.op == "decrease":
            decrement = self.evaluate(node.value)
            current = self.get_target(node.target)
            self.set_target(node.target, current - decrement)

    def get_target(self, target: Expression) -> Any:
        """Get value from assignment target."""
        if isinstance(target, Identifier):
            return self.runtime.get(target.name)
        elif isinstance(target, PropertyAccess):
            obj = self.evaluate(target.obj)
            if isinstance(obj, dict):
                return obj.get(target.prop, None)
            elif hasattr(obj, target.prop):
                return getattr(obj, target.prop)
            return None
        elif isinstance(target, IndexAccess):
            obj = self.evaluate(target.obj)
            index = self.evaluate(target.index)
            if isinstance(obj, list):
                if isinstance(index, int) and 0 <= index < len(obj):
                    return obj[index]
                return None
            elif isinstance(obj, dict):
                return obj.get(index, None)
            return None
        else:
            raise RuntimeError(f"Cannot get from target: {type(target)}")

    def set_target(self, target: Expression, value: Any):
        """Set value to assignment target."""
        if isinstance(target, Identifier):
            self.runtime.set(target.name, value)
        elif isinstance(target, PropertyAccess):
            obj = self.evaluate(target.obj)
            if isinstance(obj, dict):
                obj[target.prop] = value
            elif hasattr(obj, target.prop):
                setattr(obj, target.prop, value)
            else:
                raise RuntimeError(f"Cannot set property '{target.prop}'")
        elif isinstance(target, IndexAccess):
            obj = self.evaluate(target.obj)
            index = self.evaluate(target.index)
            if isinstance(obj, list):
                if isinstance(index, int) and 0 <= index < len(obj):
                    obj[index] = value
                else:
                    raise RuntimeError(f"Index {index} out of range")
            elif isinstance(obj, dict):
                obj[index] = value
            else:
                raise RuntimeError(f"Cannot index {type(obj)}")
        else:
            raise RuntimeError(f"Cannot assign to target: {type(target)}")

    def execute_say(self, node: SayStatement):
        parts = [str(self.evaluate(part)) for part in node.parts]
        print("".join(parts), file=self.output_stream)

    def execute_print(self, node: PrintStatement):
        value = self.evaluate(node.expr)
        print(value, file=self.output_stream)

    def execute_clear_screen(self, node: ClearScreen):
        print("\033[2J\033[H", end='', file=self.output_stream)

    def execute_show_table(self, node: ShowTable):
        rows = self.evaluate(node.rows)
        if not isinstance(rows, list):
            raise RuntimeError("show table expects a list of rows")

        from .builtin_stdlib import builtin_print_table
        table_str = builtin_print_table(node.headers, rows)
        print(table_str, file=self.output_stream)

    def execute_ask(self, node: AskStatement):
        print(node.prompt, end='', file=self.output_stream)
        self.output_stream.flush()

        try:
            response = self.input_stream.readline().strip()

            if node.ask_type == "number":
                try:
                    value = float(response)
                    self.runtime.set(node.var_name, value)
                except ValueError:
                    self.runtime.set(node.var_name, 0.0)
            elif node.ask_type == "yes_or_no":
                value = response.lower() in ('yes', 'y', 'true', '1')
                self.runtime.set(node.var_name, value)
            else:
                self.runtime.set(node.var_name, response)
        except EOFError:
            self.runtime.set(node.var_name, "")

    def execute_if(self, node: IfStatement):
        condition = self.evaluate(node.condition)
        if condition:
            for stmt in node.then_block:
                self.execute(stmt)
        elif node.else_block:
            for stmt in node.else_block:
                self.execute(stmt)

    def execute_repeat_forever(self, node: RepeatForever):
        while True:
            try:
                for stmt in node.body:
                    self.execute(stmt)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
            except StopSignal:
                raise

    def execute_repeat_times(self, node: RepeatTimes):
        count = int(self.evaluate(node.count))
        for _ in range(count):
            try:
                for stmt in node.body:
                    self.execute(stmt)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
            except StopSignal:
                raise

    def execute_repeat_until(self, node: RepeatUntil):
        while True:
            condition = self.evaluate(node.condition)
            if condition:
                break

            try:
                for stmt in node.body:
                    self.execute(stmt)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
            except StopSignal:
                raise

    def execute_do_until(self, node: DoUntil):
        while True:
            try:
                for stmt in node.body:
                    self.execute(stmt)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
            except StopSignal:
                raise

            condition = self.evaluate(node.condition)
            if condition:
                break

    def execute_function_def(self, node: FunctionDef):
        closure_env = {}
        for name in self.runtime.variables:
            closure_env[name] = self.runtime.variables[name]

        func = FunctionDef(node.name, node.params, node.body, closure_env)
        self.runtime.define_function(node.name, func)

    def execute_return(self, node: ReturnStatement):
        value = self.evaluate(node.value) if node.value else None
        raise ReturnSignal(value)

    def execute_match(self, node: MatchStatement):
        value = self.evaluate(node.expr)

        for start, end, body in node.cases:
            start_val = self.evaluate(start)
            end_val = self.evaluate(end)

            if isinstance(value, (int, float)) and isinstance(start_val, (int, float)) and isinstance(end_val, (int, float)):
                if start_val <= value <= end_val:
                    for stmt in body:
                        self.execute(stmt)
                    return
            elif value == start_val:
                for stmt in body:
                    self.execute(stmt)
                return

    def execute_list_add(self, node: ListAdd):
        list_obj = self.evaluate(node.list_expr)
        if not isinstance(list_obj, list):
            raise RuntimeError("add expects a list")
        value = self.evaluate(node.value)
        list_obj.append(value)

    def execute_list_remove(self, node: ListRemove):
        list_obj = self.evaluate(node.list_expr)
        if not isinstance(list_obj, list):
            raise RuntimeError("remove expects a list")

        if node.index is not None:
            index = int(self.evaluate(node.index))
            if 0 <= index < len(list_obj):
                list_obj.pop(index)
        else:
            value = self.evaluate(node.value)
            if value in list_obj:
                list_obj.remove(value)

    def execute_list_sort(self, node: ListSort):
        list_obj = self.evaluate(node.list_expr)
        if not isinstance(list_obj, list):
            raise RuntimeError("sort expects a list")
        list_obj.sort()

    def execute_list_reverse(self, node: ListReverse):
        list_obj = self.evaluate(node.list_expr)
        if not isinstance(list_obj, list):
            raise RuntimeError("reverse expects a list")
        list_obj.reverse()

    def execute_list_shuffle(self, node: ListShuffle):
        import random
        list_obj = self.evaluate(node.list_expr)
        if not isinstance(list_obj, list):
            raise RuntimeError("shuffle expects a list")
        random.shuffle(list_obj)

    def execute_write_file(self, node: WriteFile):
        self.permissions.check_files()

        content = self.evaluate(node.content)
        if not isinstance(content, str):
            content = str(content)

        try:
            with open(node.filename, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            if self.debug:
                raise
            raise RuntimeError(f"Failed to write file: {str(e)}")

    def execute_draw_circle(self, node: DrawCircle):
        self.permissions.check_graphics()

        x = int(self.evaluate(node.x))
        y = int(self.evaluate(node.y))
        size = int(self.evaluate(node.size))

        if self.graphics:
            self.graphics.draw_circle(x, y, size, node.color)
        else:
            print(f"[canvas] circle x={x} y={y} size={size} color={node.color}", file=self.output_stream)

    def execute_draw_rectangle(self, node: DrawRectangle):
        self.permissions.check_graphics()

        x1 = int(self.evaluate(node.x1))
        y1 = int(self.evaluate(node.y1))
        x2 = int(self.evaluate(node.x2))
        y2 = int(self.evaluate(node.y2))

        if self.graphics:
            self.graphics.draw_rectangle(x1, y1, x2, y2, node.color)
        else:
            print(f"[canvas] rectangle from {x1},{y1} to {x2},{y2} color={node.color}", file=self.output_stream)

    def execute_draw_line(self, node: DrawLine):
        self.permissions.check_graphics()

        x1 = int(self.evaluate(node.x1))
        y1 = int(self.evaluate(node.y1))
        x2 = int(self.evaluate(node.x2))
        y2 = int(self.evaluate(node.y2))

        if self.graphics:
            self.graphics.draw_line(x1, y1, x2, y2, node.color)
        else:
            print(f"[canvas] line from {x1},{y1} to {x2},{y2} color={node.color}", file=self.output_stream)

    def execute_draw_text(self, node: DrawText):
        self.permissions.check_graphics()

        text = str(self.evaluate(node.text))
        x = int(self.evaluate(node.x))
        y = int(self.evaluate(node.y))
        size = int(self.evaluate(node.size))

        if self.graphics:
            self.graphics.draw_text(text, x, y, size, node.color)
        else:
            print(f"[canvas] text '{text}' at {x},{y} size={size} color={node.color}", file=self.output_stream)

    def execute_when_mouse_clicks(self, node: WhenMouseClicks):
        self.permissions.check_graphics()

        canvas = self.evaluate(node.canvas)

        if self.graphics:
            self.graphics.register_mouse_click(canvas, node.body, self)
        else:
            print(f"[event] registered mouse click handler for canvas", file=self.output_stream)

    def execute_wait(self, node: WaitStatement):
        self.permissions.check_timers()

        seconds = float(self.evaluate(node.seconds))
        if self.scheduler:
            self.scheduler.wait(seconds)
        else:
            time.sleep(seconds)

    def execute_after(self, node: AfterStatement):
        self.permissions.check_timers()

        seconds = float(self.evaluate(node.seconds))
        if self.scheduler:
            self.scheduler.after(seconds, node.body, self)
        else:
            print(f"[timer] registered after {seconds} seconds", file=self.output_stream)

    def execute_every(self, node: EveryStatement):
        self.permissions.check_timers()

        seconds = float(self.evaluate(node.seconds))
        if self.scheduler:
            self.scheduler.every(seconds, node.body, self)
        else:
            print(f"[timer] registered every {seconds} seconds", file=self.output_stream)

    def execute_use(self, node: UseStatement):
        if not hasattr(self, 'package_manager'):
            raise RuntimeError("Package manager not initialized")
        self.package_manager.use(node.package_name, self)

    def execute_install(self, node: InstallStatement):
        if not hasattr(self, 'package_manager'):
            raise RuntimeError("Package manager not initialized")
        self.package_manager.install(node.package_name)

    def execute_use_python(self, node: UsePython):
        self.permissions.check_python_ffi()

        ALLOWED_MODULES = {'math', 'random', 'datetime', 're'}
        if node.module_name not in ALLOWED_MODULES:
            raise RuntimeError(f"Module '{node.module_name}' not in allowlist")

        if node.module_name == 'math':
            import math
            self.python_modules['math'] = math
            self.runtime.set(node.alias, math)
        elif node.module_name == 'random':
            import random
            self.python_modules['random'] = random
            self.runtime.set(node.alias, random)
        elif node.module_name == 'datetime':
            import datetime
            self.python_modules['datetime'] = datetime
            self.runtime.set(node.alias, datetime)
        elif node.module_name == 're':
            import re
            self.python_modules['re'] = re
            self.runtime.set(node.alias, re)

    def execute_server(self, node: ServerBlock):
        self.permissions.check_server()

        port = int(self.evaluate(node.port))

        if self.graphics and hasattr(self.graphics, 'start_server'):
            self.graphics.start_server(port, node.handlers, self)
        else:
            print(f"[server] registered on port {port}", file=self.output_stream)
            for method, path, body in node.handlers:
                print(f"[server] registered {method} {path}", file=self.output_stream)

    def execute_job(self, node: JobStatement):
        self.permissions.check_timers()

        seconds = float(self.evaluate(node.seconds))
        if self.scheduler:
            self.scheduler.job(node.name, seconds, node.body, self)
        else:
            print(f"[job] registered '{node.name}' every {seconds} seconds", file=self.output_stream)

    def execute_stop_job(self, node: StopJob):
        if self.scheduler:
            self.scheduler.stop_job(node.name)
        else:
            print(f"[job] stop '{node.name}'", file=self.output_stream)

    def execute_cron(self, node: CronStatement):
        self.permissions.check_cron()

        if self.scheduler:
            self.scheduler.cron(node.schedule, node.body, self)
        else:
            print(f"[cron] registered '{node.schedule}'", file=self.output_stream)

