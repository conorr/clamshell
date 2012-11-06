from consoll import Consoll

class Cat():

    def meow(self):
        print "meow"

    def add(self, a, b):
        print int(a) + int(b)

if __name__ == '__main__':

    my_cat = Cat()

    c = Consoll([ my_cat.meow,
                  ('woof', my_cat.meow),
                  my_cat.add ])
    c.start()
