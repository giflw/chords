import unittest
from markdown import Markdown
from chordsmd.abc import AbcExtension

class TestAbc(unittest.TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[AbcExtension()])

    def test_abc_rendering(self):
        text = """
```abc
X:1
T:Cool Song
K:C
CDEF|GABc|
```
"""
        html = self.md.convert(text)
        self.assertIn('class="abc-container"', html)
        self.assertIn('id="score-', html)
        self.assertIn('ABCJS.renderAbc', html)
        self.assertIn('T:Cool Song', html)

if __name__ == '__main__':
    unittest.main()
