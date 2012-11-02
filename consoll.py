import termios, fcntl, sys, os
import curses
import time

class Consoll():

    lines = []
    cursor = 0
    line_pos = 0
    chars  = ''

    def start(self):

        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:
            while 1:
                try:
                    c = sys.stdin.read(1)
                    if c == '0':
                        c = ''
                        self.reset_line()
                        self.cycle_backlog()
                    if c == '\n':
                        sys.stdout.write('\n')
                        self.lines.insert(0, self.chars)
                        request = self.chars
                        self.chars = ''
                        c = ''
                        self.line_pos = 0
                        self.parse_request(request)
                    if c == '\x7f':
                        sys.stdout.write('\b \b')
                        self.chars = self.chars[0:-1]
                        c = ''

                    sys.stdout.write(c)
                    self.cursor += 1
                    self.chars  += c

                except IOError: pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
            print(self.lines)

    def reset_line(self):
        for i in range(self.cursor):
            # delete a character
            sys.stdout.write('\b \b')
        self.cursor = 0
        self.chars = ''

    def cycle_backlog(self):
        if len(self.lines) == 0: return

        sys.stdout.write(self.lines[self.line_pos])
        self.cursor = len(self.lines[self.line_pos])
        self.chars = self.lines[self.line_pos]
        if self.line_pos < len(self.lines) - 1:
            self.line_pos += 1

    def hello_world(self):
        print "hello world!"

    def parse_request(self, request):
        if request == '': return
        cmd = ''
        args = []
        tokens = request.split(' ')
        cmd = tokens[0]
        if len(tokens) > 1: args = tokens[1:]
        #print cmd, args

if __name__ == '__main__':

    c = Consoll()
    c.start()
