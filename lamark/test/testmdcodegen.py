import unittest
from ..lmast import *
from ..mdcodegen import *

class DummyArgs(object):
    pass

class TestMdCodeGen(unittest.TestCase):
    def setUp(self):
        args = DummyArgs()
        args.o = '/dev/null'
        args.i = None
        args.debug = False
        self.gen = MdCodeGen(args)

    def _compare_ast(self, left_ast, right_ast):
        """Asserts that two ASTs are equal by dumping their contents with
           the repr method, and comparing the resultant strings.
        """
        self.assertEqual(lmast.dump(left_ast), lmast.dump(right_ast))

    def _gen_ast(self, ast):
        return self.gen.generate(ast)

    def _gen_and_compare(self, ast, correct_ast):
        self._compare_ast(
                self._gen_ast(ast),
                correct_ast)

    def test_empty_bintag_latex(self):
        self._gen_and_compare(
                Document([BinTag([], 0, "{%latex%}", [], {'func_name':'latex'})]),
                ""
        )

    def test_empty_bintag_ref(self):
        self._gen_and_compare(
                Document([BinTag([], 0, "{%ref%}", [], {'func_name':'ref'})]),
                "<sup>1</sup>"
        )
