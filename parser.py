from ast import literal_eval
import sys

def ParseError(Exception):
    def __init__(self, message):
        self.message = message

def parse(expr):
    """Parses an expression into a command and an argument vector."""
    expr = expr.strip()
    tokens = parse_into_tokens(expr)
    tokens = map(evaluate_token, tokens)
    if len(tokens) == 0:
        return (None, [])
    cmd = tokens.pop(0)
    argv = []
    if len(tokens):
        argv = tokens
    return (cmd, argv)

def is_float_like(string):
    return '.' in string

def evaluate_token(token):
    if is_evaluatable(token):
        return try_compile(token)
    if is_float_like(token):
        try:
            token = float(token)
            return token
        except ValueError:
            pass
    try:
        token = int(token)
    except ValueError:
        pass
    return token

def try_compile(token):
    """Attempts to evaluate a string into a dict, list, or tuple."""
    try:
        token = literal_eval(token)
    except:
        print 'Error parsing token: ' + token
        sys.exit()
    return token

def parse_into_tokens(expr):
    tokens = []
    while True:
        (token, expr) = break_off_token(expr)
        if token:
            tokens.append(token)
        else:
            tokens.append(expr)
            return tokens

def break_off_token(expr):
    complements = {'{': '}', '[':']', '(':')'}
    opening = None
    for i, char in enumerate(expr):
        if i == 0:
            if char in complements.keys():
                opening = char
            elif char == ' ':
                return (None, expr)
        if char == ' ':
            last_char = expr[i - 1]
            if opening:
                if last_char is complements[opening]:
                    return (expr[:i], expr[i + 1:])
            else:
                return (expr[:i], expr[i + 1:])
    return (None, expr)

def is_evaluatable(string):
    if len(string) <= 1:
        return False
    head = string[0]
    tail = string[-1]
    if head == '{' and tail == '}':
        return True
    elif head == '[' and tail == ']':
        return True
    else:
        return False

if __name__ == '__main__':
    tokens = parse('{"x": 2} foo [1, 2, 3] foo bar')
    print tokens
    print [type(token) for token in tokens]
