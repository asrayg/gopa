"""Recursive descent parser for Gopa."""

from typing import List, Optional
from .tokens import Token, TokenType
from .ast_nodes import *


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Optional[Token]:
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def peek_token(self, n: int = 1) -> Optional[Token]:
        if self.pos + n >= len(self.tokens):
            return None
        return self.tokens[self.pos + n]

    def advance(self):
        if self.pos < len(self.tokens):
            self.pos += 1

    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if not token or token.type != token_type:
            raise SyntaxError(f"Expected {token_type.name}, got {token.type.name if token else 'EOF'}")
        self.advance()
        return token

    def match(self, *token_types: TokenType) -> bool:
        token = self.current_token()
        if not token:
            return False
        return token.type in token_types

    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            self.advance()

    def parse(self) -> Program:
        statements = []
        self.skip_newlines()

        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()

        return Program(statements)

    def parse_statement(self) -> Optional[Statement]:
        self.skip_newlines()

        if self.match(TokenType.SAY):
            return self.parse_say()
        elif self.match(TokenType.PRINT):
            return self.parse_print()
        elif self.match(TokenType.CLEAR):
            return self.parse_clear()
        elif self.match(TokenType.SHOW):
            return self.parse_show_table()
        elif self.match(TokenType.ASK):
            return self.parse_ask()
        elif self.match(TokenType.IF):
            return self.parse_if()
        elif self.match(TokenType.REPEAT):
            return self.parse_repeat()
        elif self.match(TokenType.DO):
            return self.parse_do_until()
        elif self.match(TokenType.BREAK):
            self.advance()
            return BreakStatement()
        elif self.match(TokenType.CONTINUE):
            self.advance()
            return ContinueStatement()
        elif self.match(TokenType.STOP):
            self.advance()
            return StopStatement()
        elif self.match(TokenType.DEFINE):
            return self.parse_function_def()
        elif self.match(TokenType.RETURN):
            return self.parse_return()
        elif self.match(TokenType.MATCH):
            return self.parse_match()
        elif self.match(TokenType.ADD):
            return self.parse_list_add()
        elif self.match(TokenType.REMOVE):
            return self.parse_list_remove()
        elif self.match(TokenType.SORT):
            return self.parse_list_sort()
        elif self.match(TokenType.REVERSE):
            return self.parse_list_reverse()
        elif self.match(TokenType.SHUFFLE):
            return self.parse_list_shuffle()
        elif self.match(TokenType.WRITE):
            return self.parse_write_file()
        elif self.match(TokenType.DRAW):
            return self.parse_draw()
        elif self.match(TokenType.WHEN):
            return self.parse_when_mouse()
        elif self.match(TokenType.WAIT):
            return self.parse_wait()
        elif self.match(TokenType.AFTER):
            return self.parse_after()
        elif self.match(TokenType.EVERY):
            return self.parse_every()
        elif self.match(TokenType.USE):
            return self.parse_use()
        elif self.match(TokenType.INSTALL):
            return self.parse_install()
        elif self.match(TokenType.SERVER):
            return self.parse_server()
        elif self.match(TokenType.JOB):
            return self.parse_job()
        elif self.match(TokenType.CRON):
            return self.parse_cron()
        elif self.match(TokenType.IDENTIFIER):
            return self.parse_assignment_or_mutation()
        else:
            return None

    def parse_expression(self) -> Expression:
        return self.parse_or()

    def parse_or(self) -> Expression:
        left = self.parse_and()
        while self.match(TokenType.OR):
            self.advance()
            right = self.parse_and()
            left = BinaryOp(left, "or", right)
        return left

    def parse_and(self) -> Expression:
        left = self.parse_not()
        while self.match(TokenType.AND):
            self.advance()
            right = self.parse_not()
            left = BinaryOp(left, "and", right)
        return left

    def parse_not(self) -> Expression:
        if self.match(TokenType.NOT):
            self.advance()
            return UnaryOp("not", self.parse_comparison())
        return self.parse_comparison()

    def parse_comparison(self) -> Expression:
        left = self.parse_arithmetic()

        if self.match(TokenType.EQUALS):
            self.advance()
            return BinaryOp(left, "equals", self.parse_arithmetic())
        elif self.match(TokenType.DOES_NOT_EQUAL):
            self.advance()
            return BinaryOp(left, "does_not_equal", self.parse_arithmetic())
        elif self.match(TokenType.IS_GREATER_THAN):
            self.advance()
            return BinaryOp(left, "is_greater_than", self.parse_arithmetic())
        elif self.match(TokenType.IS_LESS_THAN):
            self.advance()
            return BinaryOp(left, "is_less_than", self.parse_arithmetic())
        elif self.match(TokenType.IS_AT_LEAST):
            self.advance()
            return BinaryOp(left, "is_at_least", self.parse_arithmetic())
        elif self.match(TokenType.IS_AT_MOST):
            self.advance()
            return BinaryOp(left, "is_at_most", self.parse_arithmetic())

        return left

    def parse_arithmetic(self) -> Expression:
        left = self.parse_term()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token()
            self.advance()
            op = "plus" if op_token.type == TokenType.PLUS else "minus"
            right = self.parse_term()
            left = BinaryOp(left, op, right)

        return left

    def parse_term(self) -> Expression:
        left = self.parse_factor()

        while self.match(TokenType.TIMES_OP, TokenType.DIVIDED):
            if self.match(TokenType.TIMES_OP):
                self.advance()
                right = self.parse_factor()
                left = BinaryOp(left, "times", right)
            elif self.match(TokenType.DIVIDED):
                self.advance()
                self.expect(TokenType.BY)
                right = self.parse_factor()
                left = BinaryOp(left, "divided_by", right)

        return left

    def parse_factor(self) -> Expression:
        if self.match(TokenType.NUMBER):
            token = self.current_token()
            self.advance()
            return NumberLiteral(token.value)

        if self.match(TokenType.STRING):
            token = self.current_token()
            self.advance()
            return StringLiteral(token.value)

        if self.match(TokenType.TRUE):
            self.advance()
            return BooleanLiteral(True)

        if self.match(TokenType.FALSE):
            self.advance()
            return BooleanLiteral(False)

        if self.match(TokenType.NOTHING):
            self.advance()
            return NothingLiteral()

        if self.match(TokenType.PI):
            self.advance()
            return PiLiteral()

        if self.match(TokenType.IDENTIFIER):
            name = self.current_token().value
            self.advance()

            expr = Identifier(name)
            if self.match(TokenType.DOT):
                self.advance()
                prop = self.expect(TokenType.IDENTIFIER).value
                expr = PropertyAccess(expr, prop)
            elif self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = IndexAccess(expr, index)
            elif self.match(TokenType.AT):
                self.advance()
                index = self.parse_expression()
                expr = IndexAccess(expr, index)
            elif self.match(TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER, TokenType.TRUE, 
                         TokenType.FALSE, TokenType.NOTHING, TokenType.PI, TokenType.NOT):
                args = []
                while not self.match(TokenType.NEWLINE, TokenType.EOF, TokenType.END, TokenType.AND, 
                                   TokenType.OR, TokenType.THEN, TokenType.OTHERWISE, TokenType.UNTIL,
                                   TokenType.TIMES, TokenType.DO, TokenType.FROM, TokenType.AT, TokenType.TO,
                                   TokenType.WHERE, TokenType.USING, TokenType.BY, TokenType.WITH):
                    if self.match(TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER, TokenType.TRUE,
                                TokenType.FALSE, TokenType.NOTHING, TokenType.PI, TokenType.NOT):
                        arg = self.parse_expression()
                        args.append(arg)
                    else:
                        break
                return FunctionCall(name, args)

            while True:
                if self.match(TokenType.DOT):
                    self.advance()
                    prop = self.expect(TokenType.IDENTIFIER).value
                    expr = PropertyAccess(expr, prop)
                elif self.match(TokenType.LBRACKET):
                    self.advance()
                    index = self.parse_expression()
                    self.expect(TokenType.RBRACKET)
                    expr = IndexAccess(expr, index)
                elif self.match(TokenType.AT):
                    self.advance()
                    index = self.parse_expression()
                    expr = IndexAccess(expr, index)
                else:
                    break

            return expr

        if self.match(TokenType.LBRACKET):
            return self.parse_list_literal()

        if self.match(TokenType.DICTIONARY):
            return self.parse_dictionary_literal()

        if self.match(TokenType.OBJECT):
            return self.parse_object_literal()

        if self.match(TokenType.FIND):
            return self.parse_find()

        if self.match(TokenType.FILTER):
            return self.parse_filter()

        if self.match(TokenType.MAP):
            return self.parse_map()

        if self.match(TokenType.SPLIT):
            return self.parse_string_split()

        if self.match(TokenType.JOIN):
            return self.parse_string_join()

        if self.match(TokenType.REPLACE):
            return self.parse_string_replace()

        if self.match(TokenType.GET):
            return self.parse_get_request()

        if self.match(TokenType.READ):
            return self.parse_read_file()

        if self.match(TokenType.CREATE):
            return self.parse_create_canvas()

        if self.match(TokenType.PYTHON):
            return self.parse_python_call()

        raise SyntaxError(f"Unexpected token: {self.current_token()}")

    def parse_list_literal(self) -> Expression:
        self.expect(TokenType.LBRACKET)
        elements = []

        if not self.match(TokenType.RBRACKET):
            elements.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                elements.append(self.parse_expression())

        self.expect(TokenType.RBRACKET)
        return ListLiteral(elements)

    def parse_dictionary_literal(self) -> Expression:
        self.expect(TokenType.DICTIONARY)
        pairs = []

        self.skip_newlines()
        while not self.match(TokenType.END):
            key = self.expect(TokenType.STRING).value
            self.expect(TokenType.IS)
            value = self.parse_expression()
            pairs.append((key, value))
            self.skip_newlines()

        self.expect(TokenType.END)
        return DictionaryLiteral(pairs)

    def parse_object_literal(self) -> Expression:
        self.expect(TokenType.OBJECT)
        properties = []

        self.skip_newlines()
        while not self.match(TokenType.END):
            name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.IS)
            value = self.parse_expression()
            properties.append((name, value))
            self.skip_newlines()

        self.expect(TokenType.END)
        return ObjectLiteral(properties)

    def parse_assignment_or_mutation(self) -> Statement:
        name = self.expect(TokenType.IDENTIFIER).value
        target = Identifier(name)

        while True:
            if self.match(TokenType.DOT):
                self.advance()
                prop = self.expect(TokenType.IDENTIFIER).value
                target = PropertyAccess(target, prop)
            elif self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                target = IndexAccess(target, index)
            else:
                break

        if self.match(TokenType.IS):
            self.advance()
            if self.match(TokenType.ADD):
                self.advance()
                self.expect(TokenType.TO)
                url = self.expect(TokenType.STRING).value

                params = {}
                if self.match(TokenType.USING):
                    self.advance()
                    if self.match(TokenType.IDENTIFIER):
                        while self.match(TokenType.IDENTIFIER):
                            key = self.current_token().value
                            self.advance()
                            self.expect(TokenType.IS)
                            value = self.parse_expression()
                            params[key] = value
                            if not self.match(TokenType.IDENTIFIER):
                                break
                    elif self.match(TokenType.NEWLINE):
                        self.skip_newlines()
                        while not self.match(TokenType.END):
                            key = self.expect(TokenType.IDENTIFIER).value
                            self.expect(TokenType.IS)
                            value = self.parse_expression()
                            params[key] = value
                            self.skip_newlines()
                        self.expect(TokenType.END)

                value = PostRequest(url, params)
                return Assignment(target, value)
            elif self.match(TokenType.DICTIONARY):
                value = self.parse_dictionary_literal()
                return Assignment(target, value)
            elif self.match(TokenType.OBJECT):
                value = self.parse_object_literal()
                return Assignment(target, value)
            else:
                value = self.parse_expression()
                return Assignment(target, value)
        elif self.match(TokenType.BECOMES):
            self.advance()
            value = self.parse_expression()
            return Mutation(target, "becomes", value)
        elif self.match(TokenType.INCREASE):
            self.advance()
            self.expect(TokenType.BY)
            value = self.parse_expression()
            return Mutation(target, "increase", value)
        elif self.match(TokenType.DECREASE):
            self.advance()
            self.expect(TokenType.BY)
            value = self.parse_expression()
            return Mutation(target, "decrease", value)
        else:
            args = []
            while not self.match(TokenType.NEWLINE, TokenType.EOF, TokenType.END):
                if self.match(TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER, TokenType.TRUE,
                            TokenType.FALSE, TokenType.NOTHING, TokenType.PI, TokenType.LBRACKET, TokenType.NOT):
                    args.append(self.parse_expression())
                else:
                    break
            return FunctionCall(name, args)

    def parse_say(self) -> Statement:
        self.expect(TokenType.SAY)
        parts = [self.parse_expression()]

        while self.match(TokenType.AND):
            self.advance()
            parts.append(self.parse_expression())

        return SayStatement(parts)

    def parse_print(self) -> Statement:
        self.expect(TokenType.PRINT)
        expr = self.parse_expression()
        return PrintStatement(expr)

    def parse_clear(self) -> Statement:
        self.expect(TokenType.CLEAR)
        self.expect(TokenType.SCREEN)
        return ClearScreen()

    def parse_show_table(self) -> Statement:
        self.expect(TokenType.SHOW)
        self.expect(TokenType.TABLE)
        self.expect(TokenType.WITH)
        self.expect(TokenType.HEADERS)
        self.expect(TokenType.LBRACKET)

        headers = []
        if self.match(TokenType.STRING):
            headers.append(self.current_token().value)
            self.advance()
            while self.match(TokenType.COMMA):
                self.advance()
                headers.append(self.expect(TokenType.STRING).value)

        self.expect(TokenType.RBRACKET)
        self.expect(TokenType.AND)
        self.expect(TokenType.DATA)
        self.expect(TokenType.ROWS)
        rows = self.parse_expression()

        return ShowTable(headers, rows)

    def parse_ask(self) -> Statement:
        self.expect(TokenType.ASK)
        ask_type = "string"

        if self.match(TokenType.FOR):
            self.advance()
            if self.match(TokenType.NUMBER_TYPE):
                self.advance()
                ask_type = "number"
            else:
                ask_type = "string"
        elif self.match(TokenType.YES):
            self.advance()
            self.expect(TokenType.OR)
            self.expect(TokenType.NO)
            ask_type = "yes_or_no"

        prompt = self.expect(TokenType.STRING).value
        self.expect(TokenType.IS)
        var_name = self.expect(TokenType.IDENTIFIER).value

        return AskStatement(prompt, var_name, ask_type)

    def parse_if(self) -> Statement:
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.THEN)
        self.skip_newlines()

        then_block = []
        while not self.match(TokenType.OTHERWISE, TokenType.END):
            stmt = self.parse_statement()
            if stmt:
                then_block.append(stmt)
            self.skip_newlines()

        else_block = None
        if self.match(TokenType.OTHERWISE):
            self.advance()
            self.skip_newlines()
            else_block = []
            while not self.match(TokenType.END):
                stmt = self.parse_statement()
                if stmt:
                    else_block.append(stmt)
                self.skip_newlines()

        self.expect(TokenType.END)
        return IfStatement(condition, then_block, else_block)

    def parse_repeat(self) -> Statement:
        self.expect(TokenType.REPEAT)

        if self.match(TokenType.FOREVER):
            self.advance()
            self.skip_newlines()
            body = []
            while not self.match(TokenType.END):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                self.skip_newlines()
            self.expect(TokenType.END)
            return RepeatForever(body)
        elif self.match(TokenType.UNTIL):
            self.advance()
            condition = self.parse_expression()
            self.skip_newlines()
            body = []
            while not self.match(TokenType.END):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                self.skip_newlines()
            self.expect(TokenType.END)
            return RepeatUntil(condition, body)
        else:
            count = self.parse_expression()
            self.expect(TokenType.TIMES)
            self.skip_newlines()
            body = []
            while not self.match(TokenType.END):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                self.skip_newlines()
            self.expect(TokenType.END)
            return RepeatTimes(count, body)

    def parse_do_until(self) -> Statement:
        self.expect(TokenType.DO)
        self.skip_newlines()
        body = []
        while not self.match(TokenType.UNTIL):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        self.expect(TokenType.UNTIL)
        condition = self.parse_expression()
        return DoUntil(body, condition)

    def parse_function_def(self) -> Statement:
        self.expect(TokenType.DEFINE)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.WITH)

        params = []
        if self.match(TokenType.IDENTIFIER):
            params.append(self.current_token().value)
            self.advance()
            while self.match(TokenType.IDENTIFIER):
                params.append(self.current_token().value)
                self.advance()

        self.skip_newlines()
        body = []
        while not self.match(TokenType.END):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        self.expect(TokenType.END)

        return FunctionDef(name, params, body)

    def parse_return(self) -> Statement:
        self.expect(TokenType.RETURN)
        if not self.match(TokenType.NEWLINE, TokenType.END, TokenType.EOF):
            value = self.parse_expression()
            return ReturnStatement(value)
        return ReturnStatement(None)

    def parse_match(self) -> Statement:
        self.expect(TokenType.MATCH)
        expr = self.parse_expression()
        self.skip_newlines()

        cases = []
        while not self.match(TokenType.END):
            self.expect(TokenType.WHEN)
            start = self.parse_expression()
            if self.match(TokenType.TO):
                self.advance()
                end = self.parse_expression()
            else:
                end = start

            self.skip_newlines()
            body = []
            while not self.match(TokenType.WHEN, TokenType.END):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                self.skip_newlines()

            cases.append((start, end, body))

        self.expect(TokenType.END)
        return MatchStatement(expr, cases)

    def parse_list_add(self) -> Statement:
        self.expect(TokenType.ADD)
        value = self.parse_expression()
        self.expect(TokenType.TO)
        list_expr = self.parse_expression()
        return ListAdd(list_expr, value)

    def parse_list_remove(self) -> Statement:
        self.expect(TokenType.REMOVE)

        if self.match(TokenType.AT):
            self.advance()
            index = self.parse_expression()
            self.expect(TokenType.FROM)
            list_expr = self.parse_expression()
            return ListRemove(list_expr, index=index)
        else:
            value = self.parse_expression()
            self.expect(TokenType.FROM)
            list_expr = self.parse_expression()
            return ListRemove(list_expr, value=value)

    def parse_list_sort(self) -> Statement:
        self.expect(TokenType.SORT)
        list_expr = self.parse_expression()
        return ListSort(list_expr)

    def parse_list_reverse(self) -> Statement:
        self.expect(TokenType.REVERSE)
        list_expr = self.parse_expression()
        return ListReverse(list_expr)

    def parse_list_shuffle(self) -> Statement:
        self.expect(TokenType.SHUFFLE)
        list_expr = self.parse_expression()
        return ListShuffle(list_expr)

    def parse_find(self) -> Expression:
        self.expect(TokenType.FIND)
        value = self.parse_expression()
        self.expect(TokenType.IN)
        in_expr = self.parse_expression()
        return FindExpression(value, in_expr)

    def parse_filter(self) -> Expression:
        self.expect(TokenType.FILTER)
        list_expr = self.parse_expression()
        self.expect(TokenType.WHERE)
        condition = self.parse_expression()
        return FilterExpression(list_expr, condition)

    def parse_map(self) -> Expression:
        self.expect(TokenType.MAP)
        list_expr = self.parse_expression()
        self.expect(TokenType.USING)
        transform = self.parse_expression()
        return MapExpression(list_expr, transform)

    def parse_string_split(self) -> Expression:
        self.expect(TokenType.SPLIT)
        string = self.parse_expression()
        self.expect(TokenType.BY)
        delimiter = self.expect(TokenType.STRING).value
        return StringSplit(string, delimiter)

    def parse_string_join(self) -> Expression:
        self.expect(TokenType.JOIN)
        list_expr = self.parse_expression()
        self.expect(TokenType.WITH_JOIN)
        delimiter = self.expect(TokenType.STRING).value
        return StringJoin(list_expr, delimiter)

    def parse_string_replace(self) -> Expression:
        self.expect(TokenType.REPLACE)
        old = self.expect(TokenType.STRING).value
        self.expect(TokenType.WITH)
        new = self.expect(TokenType.STRING).value
        self.expect(TokenType.IN)
        string = self.parse_expression()
        return StringReplace(string, old, new)

    def parse_get_request(self) -> Expression:
        self.expect(TokenType.GET)
        url = self.expect(TokenType.STRING).value

        params = {}
        if self.match(TokenType.USING):
            self.advance()
            if self.match(TokenType.IDENTIFIER):
                while self.match(TokenType.IDENTIFIER):
                    key = self.current_token().value
                    self.advance()
                    self.expect(TokenType.IS)
                    value = self.parse_expression()
                    params[key] = value
                    if not self.match(TokenType.IDENTIFIER):
                        break
            elif self.match(TokenType.NEWLINE):
                self.skip_newlines()
                while not self.match(TokenType.END):
                    key = self.expect(TokenType.IDENTIFIER).value
                    self.expect(TokenType.IS)
                    value = self.parse_expression()
                    params[key] = value
                    self.skip_newlines()
                self.expect(TokenType.END)

        return GetRequest(url, params)

    def parse_post_request(self) -> Expression:
        pass

    def parse_write_file(self) -> Statement:
        self.expect(TokenType.WRITE)
        content = self.parse_expression()
        self.expect(TokenType.TO_FILE)
        self.expect(TokenType.FILE)
        filename = self.expect(TokenType.STRING).value
        return WriteFile(content, filename)

    def parse_read_file(self) -> Expression:
        self.expect(TokenType.READ)
        self.expect(TokenType.FILE)
        filename = self.expect(TokenType.STRING).value
        return ReadFile(filename)

    def parse_create_canvas(self) -> Expression:
        self.expect(TokenType.CREATE)
        self.expect(TokenType.CANVAS)
        width = self.parse_expression()
        self.expect(TokenType.BY)
        height = self.parse_expression()
        return CreateCanvas(width, height)

    def parse_draw(self) -> Statement:
        self.expect(TokenType.DRAW)

        if self.match(TokenType.CIRCLE):
            self.advance()
            self.expect(TokenType.AT)
            x = self.parse_expression()
            self.expect(TokenType.COMMA)
            y = self.parse_expression()
            self.expect(TokenType.WITH)
            self.expect(TokenType.SIZE)
            size = self.parse_expression()
            self.expect(TokenType.AND)
            self.expect(TokenType.COLOR)
            color = self.expect(TokenType.STRING).value
            return DrawCircle(x, y, size, color)
        elif self.match(TokenType.RECTANGLE):
            self.advance()
            self.expect(TokenType.FROM)
            x1 = self.parse_expression()
            self.expect(TokenType.COMMA)
            y1 = self.parse_expression()
            self.expect(TokenType.TO)
            x2 = self.parse_expression()
            self.expect(TokenType.COMMA)
            y2 = self.parse_expression()
            self.expect(TokenType.WITH)
            self.expect(TokenType.COLOR)
            color = self.expect(TokenType.STRING).value
            return DrawRectangle(x1, y1, x2, y2, color)
        elif self.match(TokenType.LINE):
            self.advance()
            self.expect(TokenType.FROM)
            x1 = self.parse_expression()
            self.expect(TokenType.COMMA)
            y1 = self.parse_expression()
            self.expect(TokenType.TO)
            x2 = self.parse_expression()
            self.expect(TokenType.COMMA)
            y2 = self.parse_expression()
            self.expect(TokenType.WITH)
            self.expect(TokenType.COLOR)
            color = self.expect(TokenType.STRING).value
            return DrawLine(x1, y1, x2, y2, color)
        elif self.match(TokenType.TEXT):
            self.advance()
            text = self.parse_expression()
            self.expect(TokenType.AT)
            x = self.parse_expression()
            self.expect(TokenType.COMMA)
            y = self.parse_expression()
            self.expect(TokenType.WITH)
            self.expect(TokenType.SIZE)
            size = self.parse_expression()
            self.expect(TokenType.AND)
            self.expect(TokenType.COLOR)
            color = self.expect(TokenType.STRING).value
            return DrawText(text, x, y, size, color)

    def parse_when_mouse(self) -> Statement:
        self.expect(TokenType.WHEN)
        self.expect(TokenType.MOUSE)
        self.expect(TokenType.CLICKS)
        self.expect(TokenType.ON)
        canvas = self.parse_expression()
        self.skip_newlines()
        body = []
        while not self.match(TokenType.END):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        self.expect(TokenType.END)
        return WhenMouseClicks(canvas, body)

    def parse_wait(self) -> Statement:
        self.expect(TokenType.WAIT)
        seconds = self.parse_expression()
        self.expect(TokenType.SECONDS)
        return WaitStatement(seconds)

    def parse_after(self) -> Statement:
        self.expect(TokenType.AFTER)
        seconds = self.parse_expression()
        self.expect(TokenType.SECONDS)
        self.expect(TokenType.DO)
        self.skip_newlines()
        body = []
        while not self.match(TokenType.END):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        self.expect(TokenType.END)
        return AfterStatement(seconds, body)

    def parse_every(self) -> Statement:
        self.expect(TokenType.EVERY)
        seconds = self.parse_expression()
        self.expect(TokenType.SECONDS)
        self.expect(TokenType.DO)
        self.skip_newlines()
        body = []
        while not self.match(TokenType.END):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        self.expect(TokenType.END)
        return EveryStatement(seconds, body)

    def parse_use(self) -> Statement:
        self.expect(TokenType.USE)
        if self.match(TokenType.PYTHON):
            self.advance()
            module_name = self.expect(TokenType.STRING).value
            alias = module_name.split('.')[-1]
            return UsePython(module_name, alias)
        else:
            package_name = self.expect(TokenType.STRING).value
            return UseStatement(package_name)

    def parse_install(self) -> Statement:
        self.expect(TokenType.INSTALL)
        package_name = self.expect(TokenType.STRING).value
        return InstallStatement(package_name)

    def parse_python_call(self) -> Expression:
        self.expect(TokenType.PYTHON)
        self.expect(TokenType.CALL)
        module_attr = self.expect(TokenType.STRING).value
        self.expect(TokenType.WITH)
        args = []
        args.append(self.parse_expression())
        while self.match(TokenType.COMMA):
            self.advance()
            args.append(self.parse_expression())
        return PythonCall(module_attr, args)

    def parse_server(self) -> Statement:
        self.expect(TokenType.SERVER)
        self.expect(TokenType.ON)
        self.expect(TokenType.PORT)
        port = self.parse_expression()
        self.skip_newlines()

        handlers = []
        while not self.match(TokenType.END):
            self.expect(TokenType.WHEN)
            method = "GET"
            if self.match(TokenType.GET):
                self.advance()
                method = "GET"
            elif self.match(TokenType.ADD):
                self.advance()
                method = "POST"

            path = self.expect(TokenType.STRING).value
            self.skip_newlines()
            body = []
            while not self.match(TokenType.WHEN, TokenType.END):
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                self.skip_newlines()
            handlers.append((method, path, body))

        self.expect(TokenType.END)
        return ServerBlock(port, handlers)

    def parse_job(self) -> Statement:
        self.expect(TokenType.JOB)
        name = self.expect(TokenType.STRING).value
        self.expect(TokenType.EVERY)
        seconds = self.parse_expression()
        self.expect(TokenType.SECONDS)
        self.expect(TokenType.DO)
        self.skip_newlines()
        body = []
        while not self.match(TokenType.END):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        self.expect(TokenType.END)
        return JobStatement(name, seconds, body)

    def parse_cron(self) -> Statement:
        self.expect(TokenType.CRON)
        schedule = self.expect(TokenType.STRING).value
        self.skip_newlines()
        body = []
        while not self.match(TokenType.END):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        self.expect(TokenType.END)
        return CronStatement(schedule, body)

