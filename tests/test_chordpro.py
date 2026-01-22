import unittest
from markdown import Markdown
from chordsmd.chordpro import ChordProExtension

class TestChordPro(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[ChordProExtension()])

    def test_title_and_subtitle(self):
        text = """
```chordpro
{title: Test Song}
{subtitle: A Great Tune}
```
"""
        html = self.md.convert(text)
        self.assertIn('<h1 class="song-title">Test Song</h1>', html)
        self.assertIn('<h2 class="song-subtitle">A Great Tune</h2>', html)

    def test_metadata_directives(self):
        text = """
```chordpro
{artist: John Doe}
{composer: Jane Smith}
{key: C}
{tempo: 120}
{capo: 2}
```
"""
        html = self.md.convert(text)
        self.assertIn('Artist: John Doe', html)
        self.assertIn('Composer: Jane Smith', html)
        self.assertIn('Key: C', html)
        self.assertIn('Tempo: 120', html)
        self.assertIn('Capo: 2', html)

    def test_inline_chords(self):
        text = """
```chordpro
[Am]This is a [G]line with [C]chords.
```
"""
        html = self.md.convert(text)
        self.assertIn('<span class="chord">Am</span>', html)
        self.assertIn('<span class="chord">G</span>', html)
        self.assertIn('<span class="chord">C</span>', html)
        self.assertIn('This is a', html)
        self.assertIn('line with', html)

    def test_chorus_environment(self):
        text = """
```chordpro
{start_of_chorus}
[F]Chorus [C]text
{end_of_chorus}
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="chorus">', html)
        self.assertIn('<div class="section-label">Chorus</div>', html)
        self.assertIn('</div>', html)

    def test_verse_environment(self):
        text = """
```chordpro
{start_of_verse}
[Am]Verse text
{end_of_verse}
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="verse">', html)
        self.assertIn('<div class="section-label">Verse</div>', html)

    def test_comment_directives(self):
        text = """
```chordpro
{comment: This is a comment}
{comment_italic: Italic comment}
{comment_box: Boxed comment}
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="comment">This is a comment</div>', html)
        self.assertIn('<div class="comment italic">Italic comment</div>', html)
        self.assertIn('<div class="comment-box">Boxed comment</div>', html)

    def test_tab_environment(self):
        text = """
```chordpro
{start_of_tab}
e|---0---
B|---1---
{end_of_tab}
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="tab-section">', html)
        self.assertIn('<pre class="tab-content">', html)
        self.assertIn('e|---0---', html)

    def test_grid_environment(self):
        text = """
```chordpro
{start_of_grid}
| Am | F | C | G |
{end_of_grid}
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="chord-grid">', html)
        self.assertIn('<span class="grid-chord">Am</span>', html)
        self.assertIn('<span class="grid-chord">F</span>', html)

    def test_short_directives(self):
        text = """
```chordpro
{t: Short Title}
{st: Short Subtitle}
{c: Short comment}
{soc}
Chorus
{eoc}
```
"""
        html = self.md.convert(text)
        self.assertIn('Short Title', html)
        self.assertIn('Short Subtitle', html)
        self.assertIn('Short comment', html)
        self.assertIn('<div class="chorus">', html)

if __name__ == '__main__':
    unittest.main()
