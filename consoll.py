import termios, fcntl, sys, os
from collections import deque

class Consoll():

    cursor      = 0
    line        = ''
    history     = deque()
    history_pos = -1
    map_call        = {}

    header = ''
    prompt = ''

    def __init__(self, func_list):

        for item in func_list:
            if isinstance(item, tuple):
                self.map_call[item[0]] = item[1]
            else:
                self.map_call[item.__name__] = item

        self.map_call['history'] = self.list_history
        self.map_call['exit']    = sys.exit

    def start(self):

        # do a bunch of arcane stuff to set up the terminal
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        if self.header: print self.header

        # main keypress loop
        try:
            while 1:
                try:
                    c = sys.stdin.read(1)
                    if c == '0':
                        c = ''
                        self.history_back()
                    if c == '9':
                        c = ''
                        self.history_forward()
                    if c == '\n':
                        c = ''
                        self.enter()
                    if c == '\x7f':
                        self.backspace()
                        c = ''

                    sys.stdout.write(c)
                    self.cursor += 1
                    self.line  += c

                except IOError: pass

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
            self.history.appendleft(self.line)

    def history_back(self):
        entries = len(self.history)
        if entries == 0: return
        if entries - self.history_pos > 1:
            self.history_pos += 1
        self.write_line(self.history[self.history_pos])

    def history_forward(self):
        entries = len(self.history)
        if entries == 0: return
        if self.history_pos >= 0: self.history_pos -= 1
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
        if request == '': return
        cmd = ''
        args = []
        tokens = request.split(' ')
        cmd = tokens[0]
        if len(tokens) > 1: args = tokens[1:]

        try:
            self.map_call[cmd](*args)
        except KeyError:
            print "Error: method \'%s\' not defined" % (cmd)
            pass
