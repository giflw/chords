import unittest
from markdown import Markdown
from chordsmd.strumming import StrummingExtension

class TestStrumming(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[StrummingExtension()])

    def test_basic_pattern(self):
        text = """
```strum
D DU UDU
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="strumming-pattern">', html)
        self.assertIn('<div class="strum-sequence">', html)
        self.assertIn('↓', html)  # Downstroke
        self.assertIn('↑', html)  # Upstroke

    def test_labeled_pattern(self):
        text = """
```strum
Verse: D DU UDU
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="pattern-label">Verse</div>', html)
        self.assertIn('↓', html)

    def test_multiple_patterns(self):
        text = """
```strum
Verse: D DU UDU
Chorus: D D DU
```
"""
        html = self.md.convert(text)
        self.assertIn('Verse', html)
        self.assertIn('Chorus', html)

    def test_bar_lines(self):
        text = """
```strum
D DU | UDU D
```
"""
        html = self.md.convert(text)
        self.assertIn('<span class="bar-line">|</span>', html)

    def test_muted_strums(self):
        text = """
```strum
D X DU
```
"""
        html = self.md.convert(text)
        self.assertIn('✕', html)  # Muted symbol

    def test_rests(self):
        text = """
```strum
D - DU
```
"""
        html = self.md.convert(text)
        self.assertIn('<span class="stroke rest"', html)

    def test_beat_numbers(self):
        text = """
```strum
1 D 2 DU 3 UDU 4
```
"""
        html = self.md.convert(text)
        self.assertIn('<span class="beat-number">1</span>', html)
        self.assertIn('<span class="beat-number">4</span>', html)

    def test_arrow_notation(self):
        text = """
```strum
↓ ↓↑ ↑↓↑
```
"""
        html = self.md.convert(text)
        self.assertIn('↓', html)
        self.assertIn('↑', html)

if __name__ == '__main__':
    unittest.main()
