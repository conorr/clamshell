from collections import deque
from ast import literal_eval
import termios
import fcntl
import sys
import os


class Clamshell():

    cursor = 0
    line = ''
    history = deque()
    history_pos = -1
    map_call = {}

    header = ''
    prompt = ''

    def __init__(self, map):

        for func, ref in map.items():
            self.map_call[func] = ref

        self.map_call['history'] = self.list_history

    def add(self, item):
        """Add a function/reference item to the map"""
        self.map_call.update(item)

    def set_header(self, header):
        self.header = header

    def setup_terminal(self):
        # do a bunch of arcane stuff to set up the terminal
        self.fd = sys.stdin.fileno()
        self.oldterm = termios.tcgetattr(self.fd)
        newattr = termios.tcgetattr(self.fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.fd, termios.TCSANOW, newattr)
        self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

    def reset_terminal(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

    def start(self):
        """Start a terminal and process keystrokes"""

        self.setup_terminal();

        if self.header:
            print self.header

        escaped_chars = ''

        # main keypress loop
        try:
            while 1:
                try:

                    char = sys.stdin.read(1)

                    if escaped_chars:
                        escaped_chars += char
                        if len(escaped_chars) == 3:
                            if escaped_chars == '\x1b[A':
                                self.history_back()
                            elif escaped_chars == '\x1b[B':
                                self.history_forward()
                            escaped_chars = ''
                        char = ''

                    else:
                        if char == '\n':
                            self.enter()
                            char = ''
                        elif char == '\x7f':
                            self.backspace()
                            char = ''
                        elif char == '\x1b':
                            escaped_chars += '\x1b'
                            char = ''

                    sys.stdout.write(char)
                    self.cursor += 1
                    self.line += char

                except IOError:
                    pass
                except KeyboardInterrupt:
                    pass
                    sys.exit()

        finally:
            self.reset_terminal()

    def enter(self):
        """Process a line into a function call"""
        sys.stdout.write('\n' + self.prompt)
        self.add_to_history()
        request = self.line
        self.line = ''
        self.history_pos = -1
        call = self.parse(request)
        if call:
            self.execute(call)

    def execute(self, call):
        """Execute a function call"""
        cmd, args = call[0], call[1:]
        try:
            self.map_call[cmd](*args)
        except KeyError:
            pass
            print "Error: command \'%s\' not defined" % (cmd)

    def backspace(self):
        """Write a backspace"""
        sys.stdout.write('\b \b')
        self.line = self.line[0:-1]

    def reset_line(self):
        """Clear out the command line"""
        for i in range(self.cursor):
            self.backspace()
        self.cursor = 0
        self.line = ''

    def add_to_history(self):
        """Add the current line to history"""
        # only add non-empty lines
        if self.line != '':
            self.history.appendleft(self.line.strip())

    def history_back(self):
        """Go back one position in the command history"""
        entries = len(self.history)
        if entries == 0:
            return
        if entries - self.history_pos > 1:
            self.history_pos += 1
        self.write_line(self.history[self.history_pos])

    def history_forward(self):
        """Go forward one position in the command history"""
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
        """Write out a string on the command line"""
        self.reset_line()
        sys.stdout.write(s)
        self.cursor = len(s)
        self.line = s

    def list_history(self):
        for i, item in enumerate(self.history):
            print i, item

    def parse(self, request):
        """Parse a line of chars into a list of tokens"""

        if request == '':
            return

        token = ''
        tokens = []
        braced = None
        braced_args = []
        braces = {'{':'}', '[':']', '(':')'}

        def closing(brace):
            return braces[brace]

        for char in request:
            if char == ' ':
                if braced:
                    token += char
                else:
                    if len(token) > 0:
                        tokens.append(token)
                        token = ''
            else:
                if not braced and char in braces.keys():
                    braced = char
                    token += char
                elif braced and char == closing(braced):
                    braced = None
                    token += char
                    tokens.append(token)
                    braced_args.append(len(tokens) - 1)
                    token = ''
                else:
                    token += char

        # append token if there's still one there
        if len(token) > 0:
            tokens.append(token)

        # parse braced arguments into real Python objects
        for i in braced_args:
            try:
                tokens[i] = literal_eval(tokens[i])
            except:
                print "Syntax error in argument: {0}".format(tokens[i])
                return

        return tokens
