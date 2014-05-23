import unittest
import parser

class ParserTests(unittest.TestCase):

    def setUp(self):
        pass

    parser_tests = [
        ('', (None, [])),
        ('    ', (None, [])),
        ('foo', ('foo', [])),
        ('foo ', ('foo', [])),
        (' foo  ', ('foo', [])),
        ('foo bar', ('foo', ['bar'])),
        ('foo bar apple', ('foo', ['bar', 'apple'])),
        (' foo   bar  apple     orange ', ('foo', ['bar', 'apple', 'orange'])),
        ('foo 2', ('foo', [2])),
        ('foo 2 bar', ('foo', [2, 'bar'])),
        ('foo 2.0', ('foo', [float(2.0)])),
        ('foo 2.0 ', ('foo', [float(2.0)])),
        ('apple [\'foo\', \'bar\']', ('apple', [['foo', 'bar']])),
    ]

    def test_parser(self):
        for expression, expectation in self.parser_tests:
            result = parser.parse(expression)
            self.assertEqual(result, expectation)

if __name__ == '__main__':
    unittest.main()
