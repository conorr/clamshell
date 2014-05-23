import unittest
import parser

class ParserTests(unittest.TestCase):

    def setUp(self):
        pass

    parser_tests = [
        ('foo bar', ('foo', ['bar'])),
        ('foo bar apple', ('foo', ['bar', 'apple'])),
        ('foo 2', ('foo', [2])),
        ('foo 2 bar', ('foo', [2, 'bar'])),
        ('apple [\'foo\', \'bar\']', ('apple', [['foo', 'bar']])),
    ]

    def test_parser(self):
        for expr, expectation in self.parser_tests:
            result = parser.parse(expr)
            self.assertEqual(result, expectation)

if __name__ == '__main__':
    unittest.main()
