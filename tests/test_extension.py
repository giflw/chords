import unittest
import markdown
from chordsmd import MyExtension

class TestMyExtension(unittest.TestCase):
    def test_highlight(self):
        # "highlighted" is not a valid chord (starts with 'h'), so it should fallback to custom-highlight
        text = "This is !!highlighted!! text."
        expected = '<p>This is <span class="custom-highlight">highlighted</span> text.</p>'
        html = markdown.markdown(text, extensions=[MyExtension()])
        self.assertEqual(html, expected)

    def test_chord_rendering(self):
        text = "Play !!Cmaj7!! now"
        # We expect parsed chord structure
        expected = '<p>Play <span class="chord"><span class="root">C</span><span class="quality">maj7</span></span> now</p>'
        html = markdown.markdown(text, extensions=[MyExtension()])
        self.assertEqual(html, expected)

    def test_no_match(self):
        text = "This is normal text."
        expected = '<p>This is normal text.</p>'
        html = markdown.markdown(text, extensions=[MyExtension()])
        self.assertEqual(html, expected)

if __name__ == '__main__':
    unittest.main()
