import termios, fcntl, sys, os
import curses
import time

class Consoll():

    lines = []
    cursor = 0
    chars  = ''

    def get_char(self):

        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:
            #escaped1 = False
            #escaped2 = False
            while 1:
                try:
                    c = sys.stdin.read(1)
                    if c == '0':
                        c = ''
                        self.reset_line()
                        if len(self.lines) > 0:
                            sys.stdout.write(self.lines[0])
                            cursor = len(self.lines[0])
                            chars = self.lines[0]
                    if c == '\n':
                        self.lines.append(self.chars)

                    #if c == '\x1b':
                        #escaped1 = True
                    #if escaped1 == True and c == '[':
                        #escaped2 = True
                    #if escaped2 == True and c == 'A':
                        #sys.stdout.write('\b\ \b\b');
                        #escaped1 = False
                        #escaped2 = False

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
        pos = 0
        if len(self.lines) > 0:
            yield self.lines[0]
        pos += 1

if __name__ == '__main__':

    i = Consoll()
    i.get_char()
