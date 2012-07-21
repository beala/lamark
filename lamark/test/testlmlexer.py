import unittest
import lmlexer
import lexertokens

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

    def test_lstart_tok(self):
        "Test one LSTART Tag"
        tok_stream = self.lexer.lex("{%latex%}")
        lstart_tok = iter(tok_stream).next()
        self.assertIsInstance(
                lstart_tok,
                lexertokens.LSTART)
        self.assertEqual(
                str(lstart_tok),
                "{%latex%}")

    def test_lend_tok(self):
        "Test one LSTART Tag"
        tok_stream = self.lexer.lex("{%end%}")
        lend_tok = iter(tok_stream).next()
        self.assertIsInstance(
                lend_tok,
                lexertokens.LEND)
        self.assertEqual(
                str(lend_tok),
                "{%end%}")

    def test_lstart_lend(self):
        "LSTART Followed by LEND"
        tok_stream = self.lexer.lex(
                "{%latex%}{%end%}")
        tok_iter = iter(tok_stream)
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
                lstart_tok,
                lexertokens.LSTART)
        self.assertEqual(
                str(lstart_tok),
                "{%latex%}")
        lend_tok = tok_iter.next()
        self.assertIsInstance(
                lend_tok,
                lexertokens.LEND)
        self.assertEqual(
                str(lend_tok),
                "{%end%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_lstart_other_lend(self):
        "LSTART followed by OTHER followed by LEND"
        tok_stream = self.lexer.lex(
                "{%latex%}other{%end%}")
        tok_iter = iter(tok_stream)
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
                lstart_tok,
                lexertokens.LSTART)
        self.assertEqual(
                str(lstart_tok),
                "{%latex%}")
        other_tok = tok_iter.next()
        self.assertIsInstance(
                other_tok,
                lexertokens.OTHER)
        self.assertEqual(
                str(other_tok),
                "other")
        lend_tok = tok_iter.next()
        self.assertIsInstance(
                lend_tok,
                lexertokens.LEND)
        self.assertEqual(
                str(lend_tok),
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

    def test_escape_lstart(self):
        "ESCAPE followed by LSTART"
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
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
            lstart_tok,
            lexertokens.LSTART)
        self.assertEqual(
            str(lstart_tok),
            "{%latex%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_escape_lend(self):
        "ESCAPE followed by LEND"
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
        lend_tok = tok_iter.next()
        self.assertIsInstance(
                lend_tok,
                lexertokens.LEND)
        self.assertEqual(
                str(lend_tok),
                "{%end%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_lend_whitespace_1(self):
        "Whitespace before LSTART"
        tok_stream = self.lexer.lex(
                "{%   latex%}")
        tok_iter = iter(tok_stream)
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
            lstart_tok,
            lexertokens.LSTART)
        self.assertEqual(
            str(lstart_tok),
            "{%   latex%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_lend_whitespace_2(self):
        "Whitespace after LSTART"
        tok_stream = self.lexer.lex(
                "{%   latex    %}")
        tok_iter = iter(tok_stream)
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
            lstart_tok,
            lexertokens.LSTART)
        self.assertEqual(
            str(lstart_tok),
            "{%   latex    %}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_lstart_keywork_args(self):
        "Basic keyword arg"
        tok_stream = self.lexer.lex(
                "{%latex arg=\"value\"%}")
        tok_iter = iter(tok_stream)
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
            lstart_tok,
            lexertokens.LSTART)
        self.assertEqual(
            str(lstart_tok),
            "{%latex arg=\"value\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_lstart_positional_args(self):
        "Basic positional arg"
        tok_stream = self.lexer.lex(
                "{%latex \"value\"%}")
        tok_iter = iter(tok_stream)
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
            lstart_tok,
            lexertokens.LSTART)
        self.assertEqual(
            str(lstart_tok),
            "{%latex \"value\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_lstart_positional_keyword_args(self):
        "Basic positional AND keyword arg"
        tok_stream = self.lexer.lex(
                "{%latex \"value\" arg=\"value\"%}")
        tok_iter = iter(tok_stream)
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
            lstart_tok,
            lexertokens.LSTART)
        self.assertEqual(
            str(lstart_tok),
            "{%latex \"value\" arg=\"value\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_lstart_url_positional_keyword_args(self):
        "Test complex arg value (url with hyphen)"
        tok_stream = self.lexer.lex(
                "{%latex \"http://example-com.com\" arg=\"http://example-com.com\"%}")
        tok_iter = iter(tok_stream)
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
            lstart_tok,
            lexertokens.LSTART)
        self.assertEqual(
            str(lstart_tok),
                "{%latex \"http://example-com.com\" arg=\"http://example-com.com\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

    def test_other_func_name(self):
        "Should accept function names other than 'latex'"
        tok_stream = self.lexer.lex(
                "{%func \"value\" arg=\"value\"%}")
        tok_iter = iter(tok_stream)
        lstart_tok = tok_iter.next()
        self.assertIsInstance(
            lstart_tok,
            lexertokens.LSTART)
        self.assertEqual(
            str(lstart_tok),
            "{%func \"value\" arg=\"value\"%}")
        with self.assertRaises(StopIteration):
            tok_iter.next()

