import unittest
import matex

LSTART = "@la"
LEND   = "@"

class test_parser(unittest.TestCase):
    def setUp(self):
        self.p = matex.MdParser(None)

    def test_empty(self):
        res = self.p.parse("")
        self.assertEqual(len(res), 0)

    def test_all_md(self):
        res = self.p.parse("Some *markdown.*")
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], matex.Markdown)
        self.assertEqual(res[0].string, "Some *markdown.*")

    def test_all_latex(self):
        res = self.p.parse(LSTART + " LATEX " + LEND)
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], matex.Latex)
        self.assertEqual(res[0].string, " LATEX ")
