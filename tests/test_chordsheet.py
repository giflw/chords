import unittest
from markdown import Markdown
from chordsmd.chordsheet import ChordSheetExtension

class TestChordsSheet(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[ChordSheetExtension()])

    def test_basic_block(self):
        text = """
```chords
Am      G
I am a boy
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="chords-sheet-container">', html)
        self.assertIn('<div class="chords-controls"', html)
        self.assertIn('<div class="chords-sheet">', html)
        self.assertIn('<span class="chord"><span class="root">A</span><span class="quality">m</span></span>I', html)
        # "boy" is split by G: "b<span...>G</span>oy"
        self.assertIn('b<span class="chord"><span class="root">G</span></span>oy', html)

    def test_section_header(self):
        text = """
```chords
[Chorus]
C
Oh happy day
```
"""
        html = self.md.convert(text)
        # Verify h3 is present
        self.assertIn('<h3>Chorus</h3>', html)
        # Verify content is present
        self.assertIn('<span class="chord"><span class="root">C</span></span>Oh', html)
        
        # Verify nesting
        expected_seq = ['<section class="sheet-section"><h3>Chorus</h3>', '<span class="chord"><span class="root">C</span></span>Oh', '</section>']
        for part in expected_seq:
            self.assertIn(part, html)

    def test_orphan_chord_line(self):
        text = """
```chords
Am  G  C
```
"""
        html = self.md.convert(text)
        self.assertIn('<span class="chord"><span class="root">A</span><span class="quality">m</span></span>', html)
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
        # The merger pads "He" to reach index 8, then inserts the chord
        # Result: "He      " + chord + remaining = chord appears at position 8
        html = self.md.convert(text)
        # The chord should appear in the output, wrapped properly
        self.assertIn('<span class="chord"><span class="root">C</span></span>', html)
        self.assertIn('He', html)

if __name__ == '__main__':
    unittest.main()
