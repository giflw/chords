import unittest
from markdown import Markdown
from chordsmd.tabs import TabExtension

class TestTabs(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[TabExtension()])

    def test_basic_tab(self):
        text = """
```tab
e|---0---|
B|---1---|
G|---0---|
D|---2---|
A|---3---|
E|-------|
```
"""
        html = self.md.convert(text)
        self.assertIn('<svg', html)
        self.assertIn('<line', html)
        self.assertIn('e', html) # Label
        self.assertIn('>0<', html) # Note

    def test_bass_tab(self):
        text = """
```tab
G|-------
D|---5---
A|-------
E|-------
```
"""
        html = self.md.convert(text)
        self.assertIn('<svg', html)
        self.assertIn('G', html)
        # Should detect 4 strings
        # We can check if height is reasonably smaller
        
    def test_invalid_tab(self):
        text = """
```tab
Not a tab
Just text
```
"""
        html = self.md.convert(text)
        self.assertNotIn('<svg', html)
        self.assertIn('<pre>Not a tab', html)

if __name__ == '__main__':
    unittest.main()
