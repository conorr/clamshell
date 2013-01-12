from clamshell import Clamshell
import unittest


class TestClass():

    def say_hello(self):
        return "hello"


class ClamshellTests(unittest.TestCase):

    def setUp(self):
        self.cat = TestClass()
        self.shell = Clamshell({'hello': self.cat.say_hello})

    def test_string_parsing(self):
        tokens = self.shell.parse('a b c')
        self.assertEqual(tokens, ['a', 'b', 'c'])
        tokens = self.shell.parse('aa bb c dddd')
        self.assertEqual(tokens, ['aa', 'bb', 'c', 'dddd'])

    def test_hash_parsing(self):
        tokens = self.shell.parse("get /endpoint {'max_records': 5}")
        self.assertEqual(tokens, ['get', '/endpoint', {'max_records': 5}])
        tokens = self.shell.parse("get {'f1': 'b1', 'f2': 'b2'} thing")
        self.assertEqual(tokens, ['get', {'f1':'b1','f2':'b2'}, 'thing'])

if __name__ == '__main__':
    unittest.main()
