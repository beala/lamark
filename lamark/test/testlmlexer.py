import unittest
from .. import lmlexer
from .. import lexertokens

class testLmLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = lmlexer.LmLexer({})
        #self.p = matex.MdParser(None)

    def test_empty(self):
        "Empty string returns empty token stream"
        tok_stream = self.lexer.lex("")
        with self.assertRaises(StopIteration):
            iter(tok_stream).next()

    def test_other_tok(self):
        "String without LaMark tag returns OTHER tag"
        tok_stream = self.lexer.lex("text")
        other_tok = iter(tok_stream).next()
        self.assertIsInstance(
                other_tok,
                lexertokens.OTHER)
        self.assertEqual(
                str(other_tok),
                "text")

    def test_bin_start_tok(self):
        "Test one BIN_START Tag"
        tok_stream = self.lexer.lex("{%latex%}")
        bin_start_tok = iter(tok_stream).next()
        self.assertIsInstance(
                bin_start_tok,
                lexertokens.BIN_START)
        self.assertEqual(
                str(bin_start_tok),
                "{%latex%}")

    def test_bin_start_ref_tok(self):
        "Test one BIN_START ref Tag"
        tok_stream = self.lexer.lex("{%ref%}")
        bin_start_tok = iter(tok_stream).next()
        self.assertIsInstance(
                bin_start_tok,
                lexertokens.BIN_START)
        self.assertEqual(
                str(bin_start_tok),
                "{%ref%}")

    def test_bin_end_tok(self):
        "Test one BIN_END Tag"
        tok_stream = self.lexer.lex("{%end%}")
        bin_end_tok = iter(tok_stream).next()
        self.assertIsInstance(
                bin_end_tok,
                lexertokens.BIN_END)
        self.assertEqual(
                str(bin_end_tok),
                "{%end%}")

    def test_bin_start_bin_end(self):
        "BIN_START Followed by BIN_END"
        tok_stream = self.lexer.lex(
                "{%latex%}{%end%}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
                bin_start_tok,
                lexertokens.BIN_START)
        self.assertEqual(
                str(bin_start_tok),
                "{%latex%}")
        bin_end_tok = tok_iter.next()
        self.assertIsInstance(
                bin_end_tok,
                lexertokens.BIN_END)
        self.assertEqual(
                str(bin_end_tok),
                "{%end%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_bin_start_ref_bin_end(self):
        "RSTART Followed by REND"
        tok_stream = self.lexer.lex(
                "{%ref%}{%end%}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
                bin_start_tok,
                lexertokens.BIN_START)
        self.assertEqual(
                str(bin_start_tok),
                "{%ref%}")
        bin_end_tok = tok_iter.next()
        self.assertIsInstance(
                bin_end_tok,
                lexertokens.BIN_END)
        self.assertEqual(
                str(bin_end_tok),
                "{%end%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_bin_start_other_bin_end(self):
        "BIN_START followed by OTHER followed by BIN_END"
        tok_stream = self.lexer.lex(
                "{%latex%}other{%end%}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
                bin_start_tok,
                lexertokens.BIN_START)
        self.assertEqual(
                str(bin_start_tok),
                "{%latex%}")
        other_tok = tok_iter.next()
        self.assertIsInstance(
                other_tok,
                lexertokens.OTHER)
        self.assertEqual(
                str(other_tok),
                "other")
        bin_end_tok = tok_iter.next()
        self.assertIsInstance(
                bin_end_tok,
                lexertokens.BIN_END)
        self.assertEqual(
                str(bin_end_tok),
                "{%end%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_rstart_other_rend(self):
        "BIN_START followed by OTHER followed by BIN_END"
        tok_stream = self.lexer.lex(
                "{%ref%}other{%end%}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
                bin_start_tok,
                lexertokens.BIN_START)
        self.assertEqual(
                str(bin_start_tok),
                "{%ref%}")
        other_tok = tok_iter.next()
        self.assertIsInstance(
                other_tok,
                lexertokens.OTHER)
        self.assertEqual(
                str(other_tok),
                "other")
        bin_end_tok = tok_iter.next()
        self.assertIsInstance(
                bin_end_tok,
                lexertokens.BIN_END)
        self.assertEqual(
                str(bin_end_tok),
                "{%end%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_escape(self):
        "Backlash produces ESCAPE tok"
        tok_stream = self.lexer.lex(
                "\\")
        escape_tok = iter(tok_stream).next()
        self.assertIsInstance(
                escape_tok,
                lexertokens.ESCAPE)
        self.assertEqual(
                str(escape_tok),
                "\\")

    def test_escape_bin_start(self):
        "ESCAPE followed by BIN_START"
        tok_stream = self.lexer.lex(
                "\\{%latex%}")
        tok_iter = iter(tok_stream)
        escape_tok = tok_iter.next()
        self.assertIsInstance(
                escape_tok,
                lexertokens.ESCAPE)
        self.assertEqual(
                str(escape_tok),
                "\\")
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
            bin_start_tok,
            lexertokens.BIN_START)
        self.assertEqual(
            str(bin_start_tok),
            "{%latex%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_escape_rstart(self):
        "ESCAPE followed by BIN_START"
        tok_stream = self.lexer.lex(
                "\\{%ref%}")
        tok_iter = iter(tok_stream)
        escape_tok = tok_iter.next()
        self.assertIsInstance(
                escape_tok,
                lexertokens.ESCAPE)
        self.assertEqual(
                str(escape_tok),
                "\\")
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
            bin_start_tok,
            lexertokens.BIN_START)
        self.assertEqual(
            str(bin_start_tok),
            "{%ref%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_escape_bin_end(self):
        "ESCAPE followed by BIN_END"
        tok_stream = self.lexer.lex(
                "\\{%end%}")
        tok_iter = iter(tok_stream)
        escape_tok = tok_iter.next()
        self.assertIsInstance(
                escape_tok,
                lexertokens.ESCAPE)
        self.assertEqual(
                str(escape_tok),
                "\\")
        bin_end_tok = tok_iter.next()
        self.assertIsInstance(
                bin_end_tok,
                lexertokens.BIN_END)
        self.assertEqual(
                str(bin_end_tok),
                "{%end%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_bin_end_whitespace_1(self):
        "Whitespace before BIN_START"
        tok_stream = self.lexer.lex(
                "{%   latex%}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
            bin_start_tok,
            lexertokens.BIN_START)
        self.assertEqual(
            str(bin_start_tok),
            "{%   latex%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_bin_end_whitespace_2(self):
        "Whitespace after BIN_START"
        tok_stream = self.lexer.lex(
                "{%   latex    %}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
            bin_start_tok,
            lexertokens.BIN_START)
        self.assertEqual(
            str(bin_start_tok),
            "{%   latex    %}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_bin_start_keywork_args(self):
        "Basic keyword arg"
        tok_stream = self.lexer.lex(
                "{%latex arg=\"value\"%}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
            bin_start_tok,
            lexertokens.BIN_START)
        self.assertEqual(
            str(bin_start_tok),
            "{%latex arg=\"value\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_bin_start_positional_args(self):
        "Basic positional arg"
        tok_stream = self.lexer.lex(
                "{%latex \"value\"%}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
            bin_start_tok,
            lexertokens.BIN_START)
        self.assertEqual(
            str(bin_start_tok),
            "{%latex \"value\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_bin_start_positional_keyword_args(self):
        "Basic positional AND keyword arg"
        tok_stream = self.lexer.lex(
                "{%latex \"value\" arg=\"value\"%}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
            bin_start_tok,
            lexertokens.BIN_START)
        self.assertEqual(
            str(bin_start_tok),
            "{%latex \"value\" arg=\"value\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_bin_start_url_positional_keyword_args(self):
        "Test complex arg value (url with hyphen)"
        tok_stream = self.lexer.lex(
                "{%latex \"http://example-com.com\" arg=\"http://example-com.com\"%}")
        tok_iter = iter(tok_stream)
        bin_start_tok = tok_iter.next()
        self.assertIsInstance(
            bin_start_tok,
            lexertokens.BIN_START)
        self.assertEqual(
            str(bin_start_tok),
                "{%latex \"http://example-com.com\" arg=\"http://example-com.com\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_other_func_name(self):
        "Should ignore func names that aren't in tag_plugins"
        tok_stream = self.lexer.lex(
                "{%func \"value\" arg=\"value\"%}")
        tok_iter = iter(tok_stream)
        other_tok = tok_iter.next()
        self.assertIsInstance(
            other_tok,
            lexertokens.OTHER)
        self.assertEqual(
            str(other_tok),
            "{%func \"value\" arg=\"value\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_newline_other(self):
        "If OTHER begins on newline, say it starts on next line."
        tok_stream = self.lexer.lex(
                "\nMarkdown")
        tok_iter = iter(tok_stream)
        other_tok = tok_iter.next()
        self.assertIsInstance(
                other_tok,
                lexertokens.OTHER)
        self.assertEqual(
                str(other_tok),
                "\nMarkdown")
        self.assertEqual(
                other_tok.lineno,
                2)
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_latex_newline_other(self):
        "If OTHER begins on newline, say it starts on next line."
        tok_stream = self.lexer.lex(
                "{%latex%}{%end%}\nMarkdown")
        tok_iter = iter(tok_stream)
        tok_iter.next()
        tok_iter.next()
        other_tok = tok_iter.next()
        self.assertIsInstance(
                other_tok,
                lexertokens.OTHER)
        self.assertEqual(
                str(other_tok),
                "\nMarkdown")
        self.assertEqual(
                other_tok.lineno,
                2)
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_latex_newline_other(self):
        "OTHER's lineno should be on last preceding newline."
        tok_stream = self.lexer.lex(
                "\n\n\nMarkdown")
        tok_iter = iter(tok_stream)
        other_tok = tok_iter.next()
        self.assertIsInstance(
                other_tok,
                lexertokens.OTHER)
        self.assertEqual(
                str(other_tok),
                "\n\n\nMarkdown")
        self.assertEqual(
                other_tok.lineno,
                4)
        with self.assertRaises(StopIteration):
            tok_iter.next()
