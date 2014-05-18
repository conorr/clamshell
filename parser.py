from ast import literal_eval
import sys

def parse(expr):
    tokens = parse_into_tokens(expr)
    evaluated_tokens = []
    for token in tokens:
        if is_evaluatable(token):
            evaluated_token = evaluate(token)
            evaluated_tokens.append(evaluated_token)
        else:
            evaluated_tokens.append(token)

    return evaluated_tokens

def evaluate(token):
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

def break_off_token(string):
    breakchar = ' '
    for i, char in enumerate(string):
        if i == 0:
            if char == '{':
                breakchar = '}'
            elif char == '[':
                breakchar = ']'

        if char == breakchar:
            if breakchar == ' ':
                return (string[:i], string[i+1:])
            else:
                return (string[:i+1], string[i+2:])

    return (None, string)

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
