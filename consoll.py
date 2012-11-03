import termios, fcntl, sys, os

class Consoll():

    history = []
    cursor = 0
    history_pos = -1
    line  = ''

    def start(self):

        # do a bunch of arcane stuff to set up the terminal
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

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
        sys.stdout.write('\n')
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
        # don't add an empty line
        if self.line != '':
            self.history.insert(0, self.line)

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

    def hello_world(self):
        print "hello world!"

    def list_history(self):
        print self.history

    def parse_request(self, request):
        if request == '': return
        cmd = ''
        args = []
        tokens = request.split(' ')
        cmd = tokens[0]
        if len(tokens) > 1: args = tokens[1:]
        #print cmd, args

        map = {
               'hello': self.hello_world,
               'exit': sys.exit,
               'history': self.list_history
              }

        if cmd in map.keys():
            map[cmd]()

if __name__ == '__main__':

    c = Consoll()
    c.start()
