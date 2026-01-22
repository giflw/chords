import unittest
from markdown import Markdown
# We need to install the extension first or import assuming local path
from chordsmd import MyExtension

class TestBlocks(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[MyExtension()])

    def test_basic_block(self):
        text = """
```chords
Am      G
I am a boy
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="chords-sheet">', html)
        self.assertIn('<span class="chord">Am</span>I', html)
        # "boy" is split by G: "b<span...>G</span>oy"
        self.assertIn('b<span class="chord">G</span>oy', html)

    def test_section_header(self):
        text = """
```chords
[Chorus]
C
Oh happy day
```
"""
        html = self.md.convert(text)
        self.assertIn('<section class="sheet-section"><h3>Chorus</h3></section>', html)
        self.assertIn('<span class="chord">C</span>Oh', html)

    def test_orphan_chord_line(self):
        text = """
```chords
Am  G  C
```
"""
        html = self.md.convert(text)
        self.assertIn('<span class="chord">Am</span>', html)
        # Should be wrapped in p
        self.assertIn('<p>', html)

    def test_padding(self):
        text = """
```chords
        C
He
```
"""
        # C is at index 8. "He" is length 2.
        # Should result in "He      <span class="chord">C</span>"
        html = self.md.convert(text)
        self.assertIn('He      <span class="chord">C</span>', html)

if __name__ == '__main__':
    unittest.main()
