import unittest
from markdown import Markdown
from chordsmd.asciidoc import AsciidocExtension

class TestAsciidoc(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[AsciidocExtension()])

    def test_superscript(self):
        self.assertEqual(self.md.convert('E = mc^2^'), '<p>E = mc<sup>2</sup></p>')

    def test_subscript(self):
        self.assertEqual(self.md.convert('H~2~O'), '<p>H<sub>2</sub>O</p>')

    def test_monospace(self):
        self.assertEqual(self.md.convert('Use +git status+ to check.'), '<p>Use <code>git status</code> to check.</p>')

    def test_highlight(self):
        self.assertEqual(self.md.convert('This is #important# stuff.'), '<p>This is <mark>important</mark> stuff.</p>')

    def test_bold(self):
        self.assertEqual(self.md.convert('*bold*'), '<p><strong>bold</strong></p>')

    def test_italic(self):
        self.assertEqual(self.md.convert('_italic_'), '<p><em>italic</em></p>')

    def test_strikethrough(self):
        self.assertEqual(self.md.convert('[~]strikethrough[~]'), '<p><del>strikethrough</del></p>')

    def test_underline(self):
        self.assertEqual(self.md.convert('[_]underline[_]'), '<p><u>underline</u></p>')

    def test_quotes(self):
        self.assertEqual(self.md.convert('``double quotes\'\''), '<p><span>double quotes</span></p>')
        self.assertEqual(self.md.convert('`single quotes\''), '<p><span>single quotes</span></p>')

    def test_admonitions(self):
        html = self.md.convert('NOTE: This is a note.')
        self.assertIn('<div class="admonition note">', html)
        self.assertIn('<p class="admonition-title">NOTE</p>', html)
        
        html = self.md.convert('TIP: Keep it simple.')
        self.assertIn('<div class="admonition tip">', html)
        self.assertIn('TIP', html)

if __name__ == '__main__':
    unittest.main()
