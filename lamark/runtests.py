import unittest
from test import testlmlexer
from test import testlmparser

suite = unittest.TestLoader().loadTestsFromTestCase(testlmlexer.testLmLexer)
unittest.TextTestRunner(verbosity=2).run(suite)
suite = unittest.TestLoader().loadTestsFromTestCase(testlmparser.TestLmParser)
unittest.TextTestRunner(verbosity=2).run(suite)
