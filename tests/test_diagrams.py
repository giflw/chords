import unittest
from markdown import Markdown
from chordsmd.diagrams import ChordDiagramExtension

class TestChordDiagrams(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[ChordDiagramExtension()])

    def test_basic_diagram(self):
        text = """
```chord diagrams
C = x 3 2 0 1 0
```
"""
        html = self.md.convert(text)
        self.assertIn('<div class="chord-diagrams">', html)
        self.assertIn('<div class="chord-name">C</div>', html)
        self.assertIn('id="chord-diagram-', html)

    def test_diagram_with_fingers(self):
        text = """
```chord diagrams
B = 2 0 4.1 4.2 4.3 0
```
"""
        html = self.md.convert(text)
        self.assertIn('B', html)
        self.assertIn('chord-diagram', html)

    def test_diagram_with_barre(self):
        text = """
```chord diagrams
B = 2 0 4.1 4.2 4.3 0 |2.1
```
"""
        html = self.md.convert(text)
        self.assertIn('B', html)
        self.assertIn('"barres"', html)  # Check JSON config

    def test_multiple_diagrams(self):
        text = """
```chord diagrams
C = x 3 2 0 1 0
G = 3 2 0 0 0 3
```
"""
        html = self.md.convert(text)
        self.assertIn('C', html)
        self.assertIn('G', html)
        self.assertIn('chord-diagram-1', html)
        self.assertIn('chord-diagram-2', html)

    def test_muted_strings(self):
        text = """
```chord diagrams
D = x x 0 2 3 2
```
"""
        html = self.md.convert(text)
        self.assertIn('D', html)
        self.assertIn('"x"', html)  # Muted string marker

    def test_enhanced_symbols(self):
        # Test X for muted and O/o for open
        text = """
```chord diagrams
C = X 3 2 o 1 O
```
"""
        html = self.md.convert(text)
        self.assertIn('"x"', html)  # X becomes x in JSON
        self.assertIn('0', html)    # o/O becomes 0 in JSON

if __name__ == '__main__':
    unittest.main()
