import termios
import fcntl
import sys
import os

ESC = '\x1b'
BACKSPACE = '\x7f'
NEWLINE = '\n'

class TerminalDriver():

    initialized = False

    buf = ''
    curs = -1

    def init(self):
        log('console started')
        # do a bunch of arcane stuff to set up the terminal
        if not self.initialized:
            self.fd = sys.stdin.fileno()
            self.oldterm = termios.tcgetattr(self.fd)
            newattr = termios.tcgetattr(self.fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(self.fd, termios.TCSANOW, newattr)
            self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)
            self.initialized = True

    def reset(self):
        log('resetting terminal')
        if self.initialized:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

    def write(self, string):
        sys.stdout.write(string)

    def write_line(self, string):
        sys.stdout.write(string + '\n')

    def read(self):
        """Listen for keystrokes and interpret them."""
        esc_mode = False
        esc_seq = ''
        csi_mode = False
        csi_seq = ''
        while True:
            try:

                char = sys.stdin.read(1)

                if csi_mode:
                    csi_seq += char
                    if ord(char) >= 64 and ord(char) <= 124:
                        self.map_csi_call(csi_seq)
                        csi_seq = ''
                        csi_mode = False
                        esc_mode = False
                elif esc_mode:
                    if char == '[':
                        csi_mode = True
                    else:
                        esc_mode = False
                else:
                    if char == ESC:
                        esc_mode = True
                    elif char == BACKSPACE:
                        self.backspace()
                    elif char == NEWLINE:
                        self.write(char)
                        self.parse_line(self.buf)
                        self.buf = ''
                        self.curs = -1
                    else:
                        log(str(ord(char)))
                        self.write(char)
                        self.buf += char
                        self.curs = len(self.buf)
                        self.trace()

            except IOError:
                pass
            except KeyboardInterrupt:
                self.reset()

    def map_csi_call(self, sequence):
        """Evaluate a CSI escape sequence."""
        log("csi call with sequence '{}'".format(sequence))
        # sequence will usually be one char, but it can be more.
        if sequence == 'A':
            self.clear_line()
        elif sequence == 'D': # left arrow
            self.write(ESC + '[' + 'D')
            self.curs -= 1
            self.trace()
        elif sequence == 'C': # right arrow
            if self.curs < len(self.buf):
                self.write(ESC + '[' + 'C')
                self.curs += 1
                self.trace()

    def parse_line(self, line):
        tokens = line.split(' ')
        cmd = tokens.pop()
        args = tokens
        if cmd == 'exit':
            sys.exit()
        log("would be calling: '{}' with args {}".format(cmd, args))

    def backspace(self):
        self.write('\b \b')
        self.buf = self.buf[0:-1]
        self.curs = len(self.buf)
        self.trace()

    def clear_line(self):
        log('clearing line')
        for char in self.buf:
            self.backspace()

    def trace(self):
        with open('log.txt', 'a') as f:
            s = "cursor: {} buf: '{}'".format(self.curs, self.buf)
            f.write(s + '\n')


def log(message):
    with open('log.txt', 'a') as f:
        f.write(message + '\n')

if __name__ == '__main__':

    term = TerminalDriver()
    term.init()

    try:
        term.write('hello\n')
        char = term.read()
        term.write(char)

    except:
        term.reset()
        raise
