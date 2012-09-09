import unittest
from .. import lmparser
from .. import tokenstream
from .. import lexertokens
from .. import lmast
from .. import lamarksyntaxerror

class TestLmParser(unittest.TestCase):
    def setUp(self):
        self.parser = lmparser.LmParser({})

    def test_empty(self):
        "Parse empty token stream"
        tok_stream = tokenstream.TokenStream([])
        self._compare_ast(
                self.parser.parse(tok_stream),
                lmast.Document([])
            )

    def test_markdown(self):
        "Just markdown"
        ast = self._make_ast([
            lexertokens.OTHER("markdown",0)])
        correct_ast = lmast.Document([lmast.Markdown("markdown",0)])
        self._compare_ast(ast, correct_ast)

    def test_latex(self):
        "One LaTeX node"
        ast = self._make_ast([
            lexertokens.BIN_START("{%latex%}",0),
            lexertokens.OTHER("a^2", 0),
            lexertokens.BIN_END("{%end%}",0)])
        correct_ast = lmast.Document(
                [lmast.BinTag(
                    [Str("a^2", 0)],
                    0,
                    "{%latex%}")
                ]
        )
        self._compare_ast(ast, correct_ast)

    def test_latex(self):
        "Empty LaTeX tag."
        ast = self._make_ast([
            lexertokens.BIN_START("{%latex%}",0),
            lexertokens.BIN_END("{%end%}",0)])
        correct_ast = lmast.Document([lmast.BinTag([], 0, "{%latex%}")])
        self._compare_ast(ast, correct_ast)

    def test_latex_no_match(self):
        "One BIN_START without BIN_END. Should throw error."
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
            ast = self._make_ast([
                lexertokens.BIN_START("{%latex%}",0),
                lexertokens.OTHER("a^2", 0)])

    def test_latex_invalid_nesting_bin_start(self):
        "Nested BIN_STARTS should throw syntax error."
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
            ast = self._make_ast([
                lexertokens.BIN_START("{%latex%}",0),
                lexertokens.BIN_START("{%latex%}",0)])

    def test_latex_invalid_consecutive_bin_end(self):
        "Consecutive BIN_END tags should raise syntax error."
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
            ast = self._make_ast([
                lexertokens.BIN_START("{%latex%}",0),
                lexertokens.BIN_END("{%end%}",0),
                lexertokens.BIN_END("{%end%}",0)])

    def test_latex_invalid_consecutive_bin_end_after_other(self):
        """Consecutive BIN_END tags should raise syntax error, even if separated
        by OTHER tag.
        """
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
            ast = self._make_ast([
                lexertokens.BIN_START("{%latex%}",0),
                lexertokens.BIN_END("{%end%}",0),
                lexertokens.OTHER("some latex", 0),
                lexertokens.BIN_END("{%end%}",0)])

    def test_escaped_bin_start(self):
        "Escaped BIN_START shouldn't start LaTeX section."
        ast = self._make_ast([
            lexertokens.ESCAPE("\\",0),
            lexertokens.BIN_START("{%latex%}",0)])
        correct_ast = lmast.Document([lmast.Markdown("{%latex%}", 0)])
        self._compare_ast(ast, correct_ast)

    def test_escaped_bin_end(self):
        "Escaped BIN_END shouldn't end LaTeX section."
        ast = self._make_ast([
            lexertokens.ESCAPE("\\",0),
            lexertokens.BIN_END("{%end%}",0)])
        correct_ast = lmast.Document([lmast.Markdown("{%end%}", 0)])
        self._compare_ast(ast, correct_ast)

    def test_escaped_bin_start_in_latex_section(self):
        "Escaped BIN_START in LaTeX section should be ignored."
        ast = self._make_ast([
            lexertokens.BIN_START("{%latex%}",0),
            lexertokens.ESCAPE("\\",0),
            lexertokens.BIN_START("{%latex%}",0),
            lexertokens.BIN_END("{%end%}",0)])
        correct_ast = lmast.Document(
                [
                    lmast.BinTag(
                        [lmast.Str("{%latex%}",0)],
                        0,
                        "{%latex%}")
                ]
        )
        self._compare_ast(ast, correct_ast)

    def test_escaped_bin_end_section_in_latex(self):
        "Escaped BIN_END in LaTeX section should be ignored."
        ast = self._make_ast([
            lexertokens.BIN_START("{%latex%}",0),
            lexertokens.ESCAPE("\\",0),
            lexertokens.BIN_END("{%end%}",0),
            lexertokens.BIN_END("{%end%}",0)])
        correct_ast = lmast.Document(
                [
                    lmast.BinTag(
                    [lmast.Str("{%end%}",0)],
                    0,
                    "{%latex%}")
                ]
        )
        self._compare_ast(ast, correct_ast)

    def test_escape_in_other_isnt_escape(self):
        "An escape tag before an OTHER isn't an escape."
        ast = self._make_ast([
            lexertokens.OTHER("Some Markdown",0),
            lexertokens.ESCAPE("\\",0),
            lexertokens.OTHER("Some more Markdown",0)
            ])
        correct_ast = lmast.Document(
                [
                    lmast.Markdown(
                    "Some Markdown\\Some more Markdown", 0)
                ]
        )
        self._compare_ast(ast, correct_ast)

    def test_nested_bin_tags1(self):
        """Test nested BinTags with an OTHER token in the inner BinTag"""
        ast = self._make_ast([
            lexertokens.BIN_START("{%latex%}", 0),
            lexertokens.BIN_START("{%latex%}", 1),
            lexertokens.OTHER("Some latex.", 1),
            lexertokens.BIN_END("{%end%}", 2),
            lexertokens.BIN_END("{%end%}", 3),
        ])
        correct_ast = lmast.Document(
                [lmast.BinTag(
                    [
                        lmast.BinTag(
                            [lmast.Str("Some latex.", 1)],
                            1, "{%latex%}"
                            )
                        ],
                    0, "{%latex%}"
                    )]
        )
        self._compare_ast(ast, correct_ast)

    def test_nested_bin_tags2(self):
        """Test nested BinTags with an OTHER token in the other and
           inner BinTags.
        """
        ast = self._make_ast([
            lexertokens.BIN_START("{%latex%}", 0),
            lexertokens.OTHER("Some latex.", 1),
            lexertokens.BIN_START("{%latex%}", 2),
            lexertokens.OTHER("Some latex.", 3),
            lexertokens.BIN_END("{%end%}", 4),
            lexertokens.BIN_END("{%end%}", 5),
        ])
        correct_ast = lmast.Document(
                [
                    lmast.BinTag(
                        [
                            lmast.Str("Some latex.", 1),
                            lmast.BinTag(
                                [lmast.Str("Some latex.", 3)],
                                2, "{%latex%}"
                                )
                        ],
                    0, "{%latex%}"
                    )
                ]
        )
        self._compare_ast(ast, correct_ast)

    def test_nested_unary_in_binary(self):
        """Test nesting of unary tag inside of binary tag."""
        ast = self._make_ast([
            lexertokens.BIN_START("{%latex%}", 0),
            lexertokens.UNARY_TAG("{%ref-footer%}", 1),
            lexertokens.BIN_END("{%end%}", 2),
        ])
        correct_ast = lmast.Document(
                [
                    lmast.BinTag(
                        [lmast.UnaryTag(1, "{%ref-footer%}")],
                        0,
                        "{%latex%}")
                ]
        )
        self._compare_ast(ast, correct_ast)

    def test_escaped_nested_unary_in_binary(self):
        """Test nesting of escaped unary tag inside of binary tag."""
        ast = self._make_ast([
            lexertokens.BIN_START("{%latex%}", 0),
            lexertokens.ESCAPE("\\", 1),
            lexertokens.UNARY_TAG("{%ref-footer%}", 1),
            lexertokens.BIN_END("{%end%}", 2),
        ])
        correct_ast = lmast.Document(
                [
                    lmast.BinTag(
                        [lmast.Str("{%ref-footer%}",1)],
                        0,
                        "{%latex%}"
                    )
                ]
        )
        self._compare_ast(ast, correct_ast)

    def test_escaped_last(self):
        """Make the last character the escape char"""
        ast = self._make_ast([
            lexertokens.ESCAPE("\\",0)
        ])
        correct_ast = lmast.Document([
            lmast.Markdown("\\",0)
        ])
        self._compare_ast(ast, correct_ast)

    def test_bin_tag_then_markdown(self):
        """Make the last character the escape char"""
        ast = self._make_ast([
            lexertokens.BIN_START("{%latex%}", 0),
            lexertokens.BIN_END("{%end%}", 2),
            lexertokens.ESCAPE("\\",3),
            lexertokens.OTHER("markdown",3)
        ])
        correct_ast = lmast.Document([
            lmast.BinTag([], 0, "{%latex%}"),
            lmast.Markdown("\markdown", 3)
        ])
        self._compare_ast(ast, correct_ast)

    def _compare_ast(self, left_ast, right_ast):
        """Asserts that two ASTs are equal by dumping their contents with
           the repr method, and comparing the resultant strings.
        """
        self.assertEqual(lmast.dump(left_ast), lmast.dump(right_ast))

    def _make_ast(self, token_list):
        """Parse a list of tokens using lmparser. Return the AST."""
        tok_stream = tokenstream.TokenStream(token_list)
        return self.parser.parse(tok_stream)

