import unittest
import lmparser
import tokenstream
import lexertokens
import lmast
import lamarksyntaxerror

class TestLmParser(unittest.TestCase):
    def setUp(self):
        self.parser = lmparser.LmParser({})

    def test_empty(self):
        "Parse empty token stream"
        tok_stream = tokenstream.TokenStream([])
        self.assertEqual(
                self.parser.parse(tok_stream),
                [])

    def test_markdown(self):
        "Just markdown"
        ast = self._make_ast([
            lexertokens.OTHER("markdown",0)])
        self._test_ast_node(
                ast[0],
                lmast.Markdown,
                "markdown",
                0)

    def test_latex(self):
        "One LaTeX node"
        ast = self._make_ast([
            lexertokens.LSTART("{%latex%}",0),
            lexertokens.OTHER("a^2", 0),
            lexertokens.LEND("{%end%}",0)])
        self._test_ast_node(
                ast[0],
                lmast.Latex,
                "a^2",
                0)

    def test_latex(self):
        "Empty LaTeX tag."
        ast = self._make_ast([
            lexertokens.LSTART("{%latex%}",0),
            lexertokens.LEND("{%end%}",0)])
        self._test_ast_node(
                ast[0],
                lmast.Latex,
                "",
                0)

    def test_latex_no_match(self):
        "One LSTART without LEND. Should throw error."
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
            ast = self._make_ast([
                lexertokens.LSTART("{%latex%}",0),
                lexertokens.OTHER("a^2", 0)])

    def test_latex_invalid_nesting_lstart(self):
        "Nested LSTARTS should throw syntax error."
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
            ast = self._make_ast([
                lexertokens.LSTART("{%latex%}",0),
                lexertokens.LSTART("{%latex%}",0)])

    def test_latex_invalid_consecutive_lend(self):
        "Consecutive LEND tags should raise syntax error."
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
            ast = self._make_ast([
                lexertokens.LSTART("{%latex%}",0),
                lexertokens.LEND("{%end%}",0),
                lexertokens.LEND("{%end%}",0)])

    def test_latex_invalid_consecutive_lend_after_other(self):
        """Consecutive LEND tags should raise syntax error, even if separated
        by OTHER tag.
        """
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
            ast = self._make_ast([
                lexertokens.LSTART("{%latex%}",0),
                lexertokens.LEND("{%end%}",0),
                lexertokens.OTHER("some latex", 0),
                lexertokens.LEND("{%end%}",0)])

    def test_escaped_lstart(self):
        "Escaped LSTART shouldn't start LaTeX section."
        ast = self._make_ast([
            lexertokens.ESCAPE("\\",0),
            lexertokens.LSTART("{%latex%}",0)])
        self._test_ast_node(
                ast[0],
                lmast.Markdown,
                "{%latex%}",
                0)

    def test_escaped_lend(self):
        "Escaped LEND shouldn't end LaTeX section."
        ast = self._make_ast([
            lexertokens.ESCAPE("\\",0),
            lexertokens.LEND("{%end%}",0)])
        self._test_ast_node(
                ast[0],
                lmast.Markdown,
                "{%end%}",
                0)

    def test_escaped_lstart_in_latex_section(self):
        "Escaped LSTART in LaTeX section should be ignored."
        ast = self._make_ast([
            lexertokens.LSTART("{%latex%}",0),
            lexertokens.ESCAPE("\\",0),
            lexertokens.LSTART("{%latex%}",0),
            lexertokens.LEND("{%end%}",0)])
        self._test_ast_node(
                ast[0],
                lmast.Latex,
                "{%latex%}",
                0)

    def test_escaped_lend_section_in_latex(self):
        "Escaped LEND in LaTeX section should be ignored."
        ast = self._make_ast([
            lexertokens.LSTART("{%latex%}",0),
            lexertokens.ESCAPE("\\",0),
            lexertokens.LEND("{%end%}",0),
            lexertokens.LEND("{%end%}",0)])
        self._test_ast_node(
                ast[0],
                lmast.Latex,
                "{%end%}",
                0)

    def test_escape_in_other_isnt_escape(self):
        "An escape tag before an OTHER isn't an escape."
        ast = self._make_ast([
            lexertokens.OTHER("Some Markdown",0),
            lexertokens.ESCAPE("\\",0),
            lexertokens.OTHER("Some more Markdown",0)
            ])
        self._test_ast_node(
                ast[0],
                lmast.Markdown,
                "Some Markdown\Some more Markdown",
                0)

    def test_consecutive_other_tag(self):
        "Consecutive OTHER tags should throw syntax error"
        with self.assertRaises(lamarksyntaxerror.LaMarkSyntaxError):
            ast = self._make_ast([
                lexertokens.OTHER("Some md",0),
                lexertokens.OTHER("Some more",0)
                ])

    def _test_ast_node(self, node, class_, string, lineno):
        self.assertIsInstance(
                node,
                class_)
        self.assertEqual(
                str(node),
                string)
        self.assertEqual(
                node.lineno,
                lineno)

    def _make_ast(self, token_list):
        tok_stream = tokenstream.TokenStream(token_list)
        return self.parser.parse(tok_stream)

