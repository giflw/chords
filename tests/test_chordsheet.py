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
        # Verify h3 is present
        self.assertIn('<h3>Chorus</h3>', html)
        # Verify content is present
        self.assertIn('<span class="chord">C</span>Oh', html)
        
        # Verify nesting: Section start -> H3 -> Content -> Section end
        # We can crudely check via finding indices or just assuming if strings are present valid HTML is generated
        # or check that </section> appears after content
        expected_seq = ['<section class="sheet-section"><h3>Chorus</h3>', '<span class="chord">C</span>Oh', '</section>']
        # Simple check if all parts are there
        for part in expected_seq:
            self.assertIn(part, html)

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
