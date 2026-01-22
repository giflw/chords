import unittest
from markdown import Markdown
from chordsmd.fountain import FountainExtension

class TestFountain(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[FountainExtension()])

    def test_scene_heading(self):
        text = """
```fountain
INT. COFFEE SHOP - DAY
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="fountain-screenplay">', html)
        self.assertIn('<div class="scene-heading">INT. COFFEE SHOP - DAY</div>', html)

    def test_character_and_dialogue(self):
        text = """
```fountain
JOHN
Hello there.
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="character">JOHN</div>', html)
        self.assertIn('<div class="dialogue">Hello there.</div>', html)

    def test_parenthetical(self):
        text = """
```fountain
SARAH
(smiling)
You're late.
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="character">SARAH</div>', html)
        self.assertIn('<div class="parenthetical">(smiling)</div>', html)
        self.assertIn('<div class="dialogue">You\'re late.</div>', html)

    def test_transition(self):
        text = """
```fountain
FADE TO:
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="transition">FADE TO:</div>', html)

if __name__ == '__main__':
    unittest.main()
