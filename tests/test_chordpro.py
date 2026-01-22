import unittest
from markdown import Markdown
from chordsmd.chordpro import ChordProExtension

class TestChordPro(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[ChordProExtension()])

    def test_title_directive(self):
        text = """
```chordpro
{title: Amazing Grace}
```
"""
        html = self.md.convert(text)
        self.assertIn('<h1>Amazing Grace</h1>', html)

    def test_inline_chords(self):
        text = """
```chordpro
[C]Amazing [F]Grace
```
"""
        html = self.md.convert(text)
        self.assertIn('<span class="chord">C</span>Amazing', html)
        self.assertIn('<span class="chord">F</span>Grace', html)

    def test_chorus_section(self):
        text = """
```chordpro
{soc}
[C]Chorus
{eoc}
```
"""
        html = self.md.convert(text)
        self.assertIn('<section class="chorus">', html)
        self.assertIn('</section>', html)

if __name__ == '__main__':
    unittest.main()
