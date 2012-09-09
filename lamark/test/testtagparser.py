import unittest

from .. import tagparser
from .. import lmast
from .. import lamarksyntaxerror

class TestTagParser(unittest.TestCase):
    def setUp(self):
        self.parser = tagparser.TagParser({})

    def _compare_ast(self, left_ast, right_ast):
        self.assertEqual(
                lmast.dump(left_ast),
                lmast.dump(right_ast)
        )

    def test_empty(self):
        "Empty AST"
        ast = self.parser.parse(lmast.Document([]))
        self._compare_ast(
                ast,
                lmast.Document([]))

    def test_just_markdown(self):
        "Markdown tag"
        mk_tag = lmast.Document([lmast.Markdown("markdown", 0)])
        ast = self.parser.parse(mk_tag)
        self._compare_ast(
                ast,
                lmast.Document([lmast.Markdown("markdown", 0)])
        )

    def test_latex_no_args(self):
        "LaTeX tag with no args"
        ast = lmast.Document([lmast.BinTag([], 0, "{%latex%}")])
        ast = self.parser.parse(ast)
        self._compare_ast(
                ast,
                lmast.Document([
                    lmast.BinTag(
                        [],
                        0,
                        "{%latex%}",
                        [],
                        {'func_name':'latex'}
                    )
                ])
        )


    def test_latex_one_positional_arg(self):
        "LaTeX tag with one positional args"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{%latex "/img"%}'
                )
        ])
        ast = self.parser.parse(lt_tag)
        self.assertEqual(ast.doc[0].args, ["/img"])
        self.assertEqual(ast.doc[0].kwargs, {'func_name':'latex'})

    def test_latex_two_positional_arg(self):
        "LaTeX tag with 2 positional args"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{%latex "/img" "alt"%}'
                )
        ])
        ast = self.parser.parse(lt_tag)
        self.assertEqual(ast.doc[0].args, ["/img", "alt"])
        self.assertEqual(ast.doc[0].kwargs, {'func_name':'latex'})

    def test_nested_binary_tag(self):
        lt_tag = lmast.BinTag(
                [lmast.BinTag([], 0, '{%latex "/media"%}')],
                0,
                '{%latex "/img"%}',
                )
        ast = self.parser.parse(lmast.Document([lt_tag]))
        correct_ast = lmast.Document([
            lmast.BinTag(
                [lmast.BinTag([], 0, '{%latex "/media"%}', ["/media"], {'func_name':'latex'})],
                0,
                '{%latex "/img"%}',
                ["/img"],
                {'func_name':'latex'}
                )
        ])
        self._compare_ast(ast, correct_ast)

    def test_latex_three_positional_arg(self):
        "LaTeX tag with 3 positional args"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{%latex "/img" "alt" "1000"%}'
                )
        ])
        ast = self.parser.parse(lt_tag)
        self.assertEqual(ast.doc[0].args, ["/img", "alt", "1000"])
        self.assertEqual(ast.doc[0].kwargs, {'func_name':'latex'})

    def test_latex_four_positional_arg(self):
        "LaTeX tag with 4 positional args"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{%latex "/img" "alt" "1000" "name"%}'
                )
        ])
        ast = self.parser.parse(lt_tag)
        self.assertEqual(ast.doc[0].args, ["/img", "alt", "1000", "name"])
        self.assertEqual(ast.doc[0].kwargs, {'func_name':'latex'})

    def test_latex_one_kwarg(self):
        "LaTeX tag with one kwarg"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{%latex imgName="name"%}'
                )
        ])
        ast = self.parser.parse(lt_tag)
        self.assertEqual(ast.doc[0].args, [])
        self.assertEqual(ast.doc[0].kwargs, {'func_name':'latex',
            'imgName':'name'})

    def test_latex_two_kwargs(self):
        "LaTeX tag with two kwarg"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{%latex imgName="name" alt="alt"%}'
                )
        ])
        ast = self.parser.parse(lt_tag)
        self.assertEqual(ast.doc[0].args, [])
        self.assertEqual(ast.doc[0].kwargs, {'func_name':'latex',
            'imgName':'name',
            'alt':'alt'})

    def test_latex_url_tag(self):
        "LaTeX tag with two kwarg"
        lt_tag = lmast.Document([lmast.BinTag(
            "",
            0,
            '{%latex "http://example.com"%}'
            )
        ])
        ast = self.parser.parse(lt_tag)
        self.assertEqual(ast.doc[0].args, ["http://example.com"])
        self.assertEqual(ast.doc[0].kwargs, {'func_name':'latex'})

    def test_unexpected_assign(self):
        "Start with assign token should throw syntax error"
        lt_tag = lmast.Document([
            lmast.BinTag(
                "",
                0,
                '{% =%}'
            )
        ])
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse(lt_tag)

    def test_malformed_tag1(self):
        "Invalid char '&'"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{% &&&& %}'
                )
        ])
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse(lt_tag)

    def test_malformed_tag2(self):
        "Missing quote"
        ast = lmast.Document([
            lmast.BinTag(
                "",
                0,
                '{% latex imgName="bad name %}'
            )
        ])
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse(ast)

    def test_malformed_tag3(self):
        "Missing quote"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{% latex "bad name %}'
                )
        ])
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse(lt_tag)

    def test_malformed_tag4(self):
        "Missing quote"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{% latex bad name" %}'
                )
        ])
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse(lt_tag)

    def test_malformed_tag5(self):
        "Missing quote"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{% latex bad name%}'
                )
        ])
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse(lt_tag)

    def test_malformed_tag6(self):
        "Missing quote"
        lt_tag = lmast.Document([lmast.BinTag(
                "",
                0,
                '{% latex imgName=bad name%}'
                )
        ])
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
           ast = self.parser.parse(lt_tag)
