from consoll import Consoll

class Cat():

    def meow():
        print "meow"

    def add(a, b):
        print int(a) + int(b)

if __name__ == '__main__':

    c = Consoll(Cat)
    c.start()
