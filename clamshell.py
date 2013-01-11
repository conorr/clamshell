from ast import literal_eval
import termios
import fcntl
import sys
import os
from collections import deque


class Clamshell():

    cursor = 0
    line = ''
    history = deque()
    history_pos = -1
    map_call = {}
    escaped = 0

    header = ''
    prompt = ''

    def __init__(self, map):

        for func, ref in map.items():
            self.map_call[func] = ref

        self.map_call['history'] = self.list_history

    def add(self, item):
        self.map_call.update(item)

    def start(self):

        # do a bunch of arcane stuff to set up the terminal
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        if self.header:
            print self.header

        # main keypress loop
        try:
            while 1:
                try:
                    c = sys.stdin.read(1)

                    if c == '\x1b':
                        self.escaped = 1
                        c = ''
                    if c == '[' and self.escaped == 1:
                        self.escaped = 2
                        c = ''
                    if c == 'A' and self.escaped == 2:
                        c = ''
                        self.escaped = 0
                        self.history_back()
                    if c == 'B' and self.escaped == 2:
                        c = ''
                        self.escaped = 0
                        self.history_forward()
                    if c == 'D' and self.escaped == 2:
                        c = ''
                    if c == 'C' and self.escaped == 2:
                        c = ''
                    if c == '\n':
                        c = ''
                        self.enter()
                    if c == '\x7f':
                        self.backspace()
                        c = ''

                    sys.stdout.write(c)
                    self.cursor += 1
                    self.line  += c

                except IOError:
                    pass

        finally:

            # reset the terminal
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    def enter(self):
        sys.stdout.write('\n' + self.prompt)
        self.add_to_history()
        request = self.line
        self.line = ''
        self.history_pos = -1
        self.parse_request(request)

    def backspace(self):
        sys.stdout.write('\b \b')
        self.line = self.line[0:-1]

    def reset_line(self):
        for i in range(self.cursor):
            self.backspace()
        self.cursor = 0
        self.line = ''

    def add_to_history(self):
        # only add non-empty lines
        if self.line != '':
            self.history.appendleft(self.line.strip())

    def history_back(self):
        entries = len(self.history)
        if entries == 0:
            return
        if entries - self.history_pos > 1:
            self.history_pos += 1
        self.write_line(self.history[self.history_pos])

    def history_forward(self):
        entries = len(self.history)
        if entries == 0:
            return
        if self.history_pos >= 0:
            self.history_pos -= 1
        if self.history_pos < 0:
            self.reset_line()
            return
        self.write_line(self.history[self.history_pos])

    def write_line(self, s):
        self.reset_line()
        sys.stdout.write(s)
        self.cursor = len(s)
        self.line = s

    def list_history(self):
        for i, item in enumerate(self.history):
            print i, item

    def parse_request(self, request):
        if request == '':
            return
        cmd = ''
        args = []
        token = ''
        tokens = []
        braced = False
        braced_args = []

        for char in request:
            if char == ' ':
                if braced is True:
                    token += char
                else:
                    if len(token) > 0:
                        tokens.append(token)
                        token = ''
            else:
                if char == '{':
                    braced = True
                    token += char
                elif char == '}':
                    braced = False
                    token += char
                    tokens.append(token)
                    braced_args.append(len(tokens) - 1)
                    token = ''
                else:
                    token += char

        # append token if there's still one there
        if len(token) > 0:
            tokens.append(token)

        for i in braced_args:
            try:
                tokens[i] = literal_eval(tokens[i])
            except:
                print "Syntax error in argument: {0}".format(tokens[i])
                return

        cmd = tokens[0]
        if len(tokens) > 1:
            args = tokens[1:]

        try:
            self.map_call[cmd](*args)
        except KeyError:
            print "Error: command \'%s\' not defined" % (cmd)
            pass
