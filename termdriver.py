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

    def __init__(self, prompt='> ', header=None):
        self.header = header
        self.prompt = prompt

    @property
    def header(self, header):
        self.header = header

    @property
    def prompt(self, prompt):
        self.prompt = prompt

    def init(self):
        """Does a bunch of arcane stuff to set up the terminal."""
        log('console started')
        if not self.initialized:
            self.fd = sys.stdin.fileno()
            self.oldterm = termios.tcgetattr(self.fd)
            newattr = termios.tcgetattr(self.fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(self.fd, termios.TCSANOW, newattr)
            self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

            if self.header:
                self.write(self.header + NEWLINE)
            self.write(self.prompt)

            self.initialized = True

    def reset(self):
        """Resets the terminal to the state it was in before it was
        initialized."""
        log('resetting terminal')
        if self.initialized:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

    def write(self, string):
        """Writes a string to the terminal."""
        sys.stdout.write(string)

    def write_line(self, string):
        """Writes a string to the terminal and a newline."""
        sys.stdout.write(string + '\n')

    def start(self):
        """Listens for keystrokes and takes action based on them."""
        self.init()
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
                        self.return_()
                    else:
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
            if self.curs > 0:
                self.write(ESC + '[' + 'D')
                self.curs -= 1
                self.trace()
        elif sequence == 'C': # right arrow
            if self.curs < len(self.buf):
                self.write(ESC + '[' + 'C')
                self.curs += 1
                self.trace()

    def return_(self):
        self.write(NEWLINE)
        self.parse_line(self.buf)
        self.buf = ''
        self.curs = -1
        self.write(self.prompt)

    def parse_line(self, line):
        if self.buf:
            tokens = line.split(' ')
            cmd = tokens.pop(0)
            args = ' '.join(tokens)
            if cmd:
                log("would be calling: '{}' with args '{}'".format(cmd, args))
                if cmd == 'exit':
                    self.exit()
                else:
                    self.write_line("Error: unknown command '{}'".format(cmd))

    def backspace(self):
        if self.curs > 0:
            self.write('\b \b')
            self.buf = self.buf[0:-1]
            self.curs = len(self.buf)
            self.trace()

    def clear_line(self):
        log('clearing line')
        for char in self.buf:
            self.backspace()

    def exit(self):
        self.reset()
        sys.exit()

    def trace(self):
        with open('log.txt', 'a') as f:
            s = "cursor: {} buf: '{}'".format(self.curs, self.buf)
            f.write(s + '\n')


def log(message):
    with open('log.txt', 'a') as f:
        f.write(message + '\n')

if __name__ == '__main__':
    term = TerminalDriver()
    term.header = 'Welcome to Clamshell!'
    term.prompt = '$ '
    term.start()
