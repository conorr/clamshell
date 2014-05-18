from ast import literal_eval
import sys

def parse(expression):
    tokens = parse_into_tokens(expression)
    evaluated_tokens = []
    for token in tokens:
        if is_evaluatable(token):
            try:
                evaluated_token = literal_eval(token)
            except:
                raise Exception('Error parsing token: ' + token)
            evaluated_tokens.append(evaluated_token)
        else:
            evaluated_tokens.append(token)

    return evaluated_tokens

def parse_into_tokens(expression):
    tokens = []
    while True:
        (token, expression) = break_off_token(expression)
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
    tokens = parse('{"x": 2} foo [1, 2, 3] foo bar')
    print tokens
    print [type(token) for token in tokens]
