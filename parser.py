from ast import literal_eval
import sys

def parse(expr):
    tokens = parse_into_tokens(expr)
    evaluated_tokens = []
    for token in tokens:
        if is_evaluatable(token):
            evaluated_token = try_compile(token)
            evaluated_tokens.append(evaluated_token)
        else:
            evaluated_tokens.append(token)

    return evaluated_tokens

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
            return tokens

def break_off_token(expr):
    breakchar = ' '
    for i, char in enumerate(expr):
        if i == 0:
            if char == '{':
                breakchar = '}'
            elif char == '[':
                breakchar = ']'

        if char == breakchar:
            if breakchar == ' ':
                return (expr[:i], expr[i+1:])
            else:
                return (expr[:i+1], expr[i+2:])

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
    tokens = parse('{"x": 2}foo [1, 2, 3] foo bar')
    print tokens
    print [type(token) for token in tokens]
