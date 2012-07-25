import unittest

from .. import tagparser
from .. import lmast
from .. import lamarksyntaxerror

class TestTagParser(unittest.TestCase):
    def setUp(self):
        self.parser = tagparser.TagParser({})

    def test_empty(self):
        "Empty AST"
        ast = self.parser.parse([])
        self.assertEqual(ast, [])

    def test_just_markdown(self):
        "Markdown tag"
        mk_tag = lmast.Markdown("markdown", 0)
        ast = self.parser.parse([mk_tag])
        self.assertEqual(ast, [mk_tag])

    def test_latex_no_args(self):
         "LaTeX tag with no args"
         lt_tag = lmast.Latex(
                 "",
                 0,
                 "{%latex%}"
                 )
         ast = self.parser.parse([lt_tag])
         self.assertEqual(ast[0].args, [])
         self.assertEqual(ast[0].kwargs, {'func_name':'latex'})

    def test_latex_one_positional_arg(self):
         "LaTeX tag with one positional args"
         lt_tag = lmast.Latex(
                 "",
                 0,
                 '{%latex "/img"%}'
                 )
         ast = self.parser.parse([lt_tag])
         self.assertEqual(ast[0].args, ["/img"])
         self.assertEqual(ast[0].kwargs, {'func_name':'latex'})

    def test_latex_two_positional_arg(self):
         "LaTeX tag with 2 positional args"
         lt_tag = lmast.Latex(
                 "",
                 0,
                 '{%latex "/img" "alt"%}'
                 )
         ast = self.parser.parse([lt_tag])
         self.assertEqual(ast[0].args, ["/img", "alt"])
         self.assertEqual(ast[0].kwargs, {'func_name':'latex'})

    def test_latex_three_positional_arg(self):
         "LaTeX tag with 3 positional args"
         lt_tag = lmast.Latex(
                 "",
                 0,
                 '{%latex "/img" "alt" "1000"%}'
                 )
         ast = self.parser.parse([lt_tag])
         self.assertEqual(ast[0].args, ["/img", "alt", "1000"])
         self.assertEqual(ast[0].kwargs, {'func_name':'latex'})

    def test_latex_four_positional_arg(self):
         "LaTeX tag with 4 positional args"
         lt_tag = lmast.Latex(
                 "",
                 0,
                 '{%latex "/img" "alt" "1000" "name"%}'
                 )
         ast = self.parser.parse([lt_tag])
         self.assertEqual(ast[0].args, ["/img", "alt", "1000", "name"])
         self.assertEqual(ast[0].kwargs, {'func_name':'latex'})

    def test_latex_one_kwarg(self):
         "LaTeX tag with one kwarg"
         lt_tag = lmast.Latex(
                 "",
                 0,
                 '{%latex imgName="name"%}'
                 )
         ast = self.parser.parse([lt_tag])
         self.assertEqual(ast[0].args, [])
         self.assertEqual(ast[0].kwargs, {'func_name':'latex',
             'imgName':'name'})

    def test_latex_two_kwargs(self):
         "LaTeX tag with two kwarg"
         lt_tag = lmast.Latex(
                 "",
                 0,
                 '{%latex imgName="name" alt="alt"%}'
                 )
         ast = self.parser.parse([lt_tag])
         self.assertEqual(ast[0].args, [])
         self.assertEqual(ast[0].kwargs, {'func_name':'latex',
             'imgName':'name',
             'alt':'alt'})

    def test_latex_url_tag(self):
         "LaTeX tag with two kwarg"
         lt_tag = lmast.Latex(
                 "",
                 0,
                 '{%latex "http://example.com"%}'
                 )
         ast = self.parser.parse([lt_tag])
         self.assertEqual(ast[0].args, ["http://example.com"])
         self.assertEqual(ast[0].kwargs, {'func_name':'latex'})

    def test_unexpected_assign(self):
        "Start with assign token should throw syntax error"
        lt_tag = lmast.Latex(
                "",
                0,
                '{% =%}'
                )
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse([lt_tag])

    def test_malformed_tag1(self):
        "Invalid char '&'"
        lt_tag = lmast.Latex(
                "",
                0,
                '{% &&&& %}'
                )
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse([lt_tag])

    def test_malformed_tag2(self):
        "Missing quote"
        lt_tag = lmast.Latex(
                "",
                0,
                '{% latex imgName="bad name %}'
                )
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse([lt_tag])

    def test_malformed_tag3(self):
        "Missing quote"
        lt_tag = lmast.Latex(
                "",
                0,
                '{% latex "bad name %}'
                )
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse([lt_tag])

    def test_malformed_tag4(self):
        "Missing quote"
        lt_tag = lmast.Latex(
                "",
                0,
                '{% latex bad name" %}'
                )
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse([lt_tag])

    def test_malformed_tag5(self):
        "Missing quote"
        lt_tag = lmast.Latex(
                "",
                0,
                '{% latex bad name%}'
                )
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse([lt_tag])

    def test_malformed_tag6(self):
        "Missing quote"
        lt_tag = lmast.Latex(
                "",
                0,
                '{% latex imgName=bad name%}'
                )
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse([lt_tag])
