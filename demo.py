from consoll import Consoll
import sys

class Cat():

    count = 0

    def meow(self, times=1):
        for time in range(int(times)):
            print "meow"
            self.count += 1

    def meow_count(self):
        print self.count

if __name__ == '__main__':

    my_cat = Cat()

    c = Consoll({ 'meow':       my_cat.meow,
                  'meow_count': my_cat.meow_count,
                  'exit':       sys.exit })
    c.start()
