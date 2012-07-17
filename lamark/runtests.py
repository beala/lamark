import unittest
from test import testlmlexer

suite = unittest.TestLoader().loadTestsFromTestCase(testlmlexer.testLmLexer)
unittest.TextTestRunner(verbosity=2).run(suite)
