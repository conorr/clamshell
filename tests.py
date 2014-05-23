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
        ('foo {\'x\': 2}', ('foo', [{'x': 2}])),
    ]

    def test_parser(self):
        for expression, expectation in self.parser_tests:
            result = parser.parse(expression)
            self.assertEqual(result, expectation)

    def test_parseerror(self):

        tests = [
            '{\'x\' 2}',
            '[1 2, 3]',
            '(\'foo\', \'bar\''
        ]

        for expression in tests:
            error = None
            try:
                parser.try_compile(expression)
            except Exception as e:
                error = e
            self.assertIsNotNone(error)
            self.assertIsInstance(error, parser.ParseError)

if __name__ == '__main__':
    unittest.main()
