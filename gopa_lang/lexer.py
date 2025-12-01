"""Lexer for Gopa - tokenizes English-like syntax."""

from typing import List, Optional
from .tokens import Token, TokenType


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def peek(self, n: int = 1) -> Optional[str]:
        if self.pos + n >= len(self.text):
            return None
        return self.text[self.pos + n]

    def advance(self):
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()

    def skip_comment(self):
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()

    def read_number(self) -> Token:
        start_pos = self.pos
        start_col = self.column
        has_dot = False

        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break
                has_dot = True
            self.advance()

        num_str = self.text[start_pos:self.pos]
        value = float(num_str) if has_dot else int(num_str)
        return Token(TokenType.NUMBER, value, self.line, start_col)

    def read_string(self) -> Token:
        start_col = self.column
        quote = self.current_char()
        self.advance()

        value = ""
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    value += '\n'
                elif self.current_char() == 't':
                    value += '\t'
                elif self.current_char() == '\\':
                    value += '\\'
                elif self.current_char() == quote:
                    value += quote
                else:
                    value += self.current_char()
            else:
                value += self.current_char()
            self.advance()

        if self.current_char() == quote:
            self.advance()

        return Token(TokenType.STRING, value, self.line, start_col)

    def read_identifier_or_keyword(self) -> Token:
        start_pos = self.pos
        start_col = self.column

        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            self.advance()

        word = self.text[start_pos:self.pos].lower()

        if word == "times":
            saved_pos = self.pos
            saved_col = self.column
            peek_char = self.current_char()
            if peek_char in (' ', '\n', None):
                lookback_start = max(0, start_pos - 20)
                context_before = self.text[lookback_start:start_pos].lower().strip()
                if context_before.endswith(('repeat', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                    if peek_char in (' ', '\n', None):
                        return Token(TokenType.TIMES, None, self.line, start_col)
            return Token(TokenType.TIMES_OP, None, self.line, start_col)

        if word == "does" and self.peek() == ' ':
            saved_pos = self.pos
            saved_col = self.column
            self.advance()
            if self.text[self.pos:self.pos+3].lower() == "not":
                self.pos += 3
                self.column += 3
                if self.text[self.pos:self.pos+1] == ' ':
                    self.pos += 1
                    self.column += 1
                    if self.text[self.pos:self.pos+5].lower() == "equal":
                        self.pos += 5
                        self.column += 5
                        return Token(TokenType.DOES_NOT_EQUAL, None, self.line, start_col)
            self.pos = saved_pos
            self.column = saved_col

        if word == "is" and self.current_char() == ' ':
            saved_pos = self.pos
            saved_col = self.column
            self.advance()
            next_word = ""
            while self.current_char() and (self.current_char().isalnum() or self.current_char() == ' '):
                if self.current_char() == ' ':
                    if next_word:
                        break
                    self.advance()
                    continue
                next_word += self.current_char()
                self.advance()

            if next_word == "greater":
                if self.text[self.pos:self.pos+5].lower() == " than":
                    self.pos += 5
                    self.column += 5
                    return Token(TokenType.IS_GREATER_THAN, None, self.line, start_col)
            elif next_word == "less":
                if self.text[self.pos:self.pos+5].lower() == " than":
                    self.pos += 5
                    self.column += 5
                    return Token(TokenType.IS_LESS_THAN, None, self.line, start_col)
            elif next_word == "at":
                if self.text[self.pos:self.pos+6].lower() == " least":
                    self.pos += 6
                    self.column += 6
                    return Token(TokenType.IS_AT_LEAST, None, self.line, start_col)
                elif self.text[self.pos:self.pos+4].lower() == " most":
                    self.pos += 4
                    self.column += 4
                    return Token(TokenType.IS_AT_MOST, None, self.line, start_col)

            self.pos = saved_pos
            self.column = saved_col

        if word == "divided" and self.current_char() == ' ':
            saved_pos = self.pos
            saved_col = self.column
            self.advance()
            if self.text[self.pos:self.pos+3].lower() == "by ":
                self.pos += 3
                self.column += 3
                return Token(TokenType.DIVIDED, None, self.line, start_col)
            self.pos = saved_pos
            self.column = saved_col

        keyword_map = {
            "is": TokenType.IS,
            "becomes": TokenType.BECOMES,
            "say": TokenType.SAY,
            "print": TokenType.PRINT,
            "clear": TokenType.CLEAR,
            "show": TokenType.SHOW,
            "ask": TokenType.ASK,
            "for": TokenType.FOR,
            "if": TokenType.IF,
            "then": TokenType.THEN,
            "otherwise": TokenType.OTHERWISE,
            "repeat": TokenType.REPEAT,
            "forever": TokenType.FOREVER,
            "times": TokenType.TIMES,
            "until": TokenType.UNTIL,
            "do": TokenType.DO,
            "break": TokenType.BREAK,
            "continue": TokenType.CONTINUE,
            "stop": TokenType.STOP,
            "define": TokenType.DEFINE,
            "with": TokenType.WITH,
            "return": TokenType.RETURN,
            "end": TokenType.END,
            "when": TokenType.WHEN,
            "match": TokenType.MATCH,
            "to": TokenType.TO,
            "add": TokenType.ADD,
            "remove": TokenType.REMOVE,
            "from": TokenType.FROM,
            "at": TokenType.AT,
            "sort": TokenType.SORT,
            "reverse": TokenType.REVERSE,
            "shuffle": TokenType.SHUFFLE,
            "find": TokenType.FIND,
            "in": TokenType.IN,
            "filter": TokenType.FILTER,
            "where": TokenType.WHERE,
            "map": TokenType.MAP,
            "using": TokenType.USING,
            "item": TokenType.ITEM,
            "dictionary": TokenType.DICTIONARY,
            "object": TokenType.OBJECT,
            "split": TokenType.SPLIT,
            "by": TokenType.BY,
            "join": TokenType.JOIN,
            "replace": TokenType.REPLACE,
            "get": TokenType.GET,
            "write": TokenType.WRITE,
            "read": TokenType.READ,
            "file": TokenType.FILE,
            "create": TokenType.CREATE,
            "canvas": TokenType.CANVAS,
            "draw": TokenType.DRAW,
            "circle": TokenType.CIRCLE,
            "rectangle": TokenType.RECTANGLE,
            "line": TokenType.LINE,
            "text": TokenType.TEXT,
            "color": TokenType.COLOR,
            "size": TokenType.SIZE,
            "mouse": TokenType.MOUSE,
            "clicks": TokenType.CLICKS,
            "on": TokenType.ON,
            "wait": TokenType.WAIT,
            "seconds": TokenType.SECONDS,
            "after": TokenType.AFTER,
            "every": TokenType.EVERY,
            "and": TokenType.AND,
            "or": TokenType.OR,
            "not": TokenType.NOT,
            "plus": TokenType.PLUS,
            "minus": TokenType.MINUS,
            "increase": TokenType.INCREASE,
            "decrease": TokenType.DECREASE,
            "yes": TokenType.YES,
            "no": TokenType.NO,
            "number": TokenType.NUMBER_TYPE,
            "screen": TokenType.SCREEN,
            "table": TokenType.TABLE,
            "headers": TokenType.HEADERS,
            "data": TokenType.DATA,
            "rows": TokenType.ROWS,
            "use": TokenType.USE,
            "install": TokenType.INSTALL,
            "python": TokenType.PYTHON,
            "call": TokenType.CALL,
            "server": TokenType.SERVER,
            "port": TokenType.PORT,
            "job": TokenType.JOB,
            "cron": TokenType.CRON,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "nothing": TokenType.NOTHING,
            "pi": TokenType.PI,
            "equals": TokenType.EQUALS,
        }

        if word in keyword_map:
            return Token(keyword_map[word], None, self.line, start_col)

        return Token(TokenType.IDENTIFIER, word, self.line, start_col)

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.text):
            self.skip_whitespace()

            if not self.current_char():
                break

            if self.current_char() == '#':
                self.skip_comment()
                continue

            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, None, self.line, self.column))
                self.advance()
                continue

            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue

            if self.current_char() in '"\'':
                self.tokens.append(self.read_string())
                continue

            if self.current_char() == '.':
                self.tokens.append(Token(TokenType.DOT, None, self.line, self.column))
                self.advance()
                continue

            if self.current_char() == '[':
                self.tokens.append(Token(TokenType.LBRACKET, None, self.line, self.column))
                self.advance()
                continue

            if self.current_char() == ']':
                self.tokens.append(Token(TokenType.RBRACKET, None, self.line, self.column))
                self.advance()
                continue

            if self.current_char() == ',':
                self.tokens.append(Token(TokenType.COMMA, None, self.line, self.column))
                self.advance()
                continue

            if self.current_char() == '=':
                self.advance()
                continue

            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier_or_keyword())
                continue

            self.advance()

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

