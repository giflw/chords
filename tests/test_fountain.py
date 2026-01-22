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

    def test_forced_scene_heading(self):
        text = """
```fountain
.SNIPER SCOPE POV
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="scene-heading">SNIPER SCOPE POV</div>', html)

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

    def test_forced_character(self):
        text = """
```fountain
@McCLANE
Yippie ki-yay!
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="character">McCLANE</div>', html)

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

    def test_forced_transition(self):
        text = """
```fountain
>Burn to White.
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="transition">Burn to White.</div>', html)

    def test_centered_text(self):
        text = """
```fountain
>THE END<
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="centered">THE END</div>', html)

    def test_lyrics(self):
        text = """
```fountain
~Willy Wonka! Willy Wonka!
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="lyrics">Willy Wonka! Willy Wonka!</div>', html)

    def test_emphasis(self):
        text = """
```fountain
This is *italic* and **bold** and _underlined_.
```
"""
        html = self.md.convert(text)
        self.assertIn('<em>italic</em>', html)
        self.assertIn('<strong>bold</strong>', html)
        self.assertIn('<u>underlined</u>', html)

    def test_dual_dialogue(self):
        text = """
```fountain
BRICK
Screw retirement.

STEEL ^
Screw retirement.
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="character">BRICK</div>', html)
        self.assertIn('<div class="character dual">STEEL</div>', html)

if __name__ == '__main__':
    unittest.main()
