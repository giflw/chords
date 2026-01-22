import unittest
import markdown
from my_extension import MyExtension

class TestMyExtension(unittest.TestCase):
    def test_highlight(self):
        text = "This is !!highlighted!! text."
        expected = '<p>This is <span class="custom-highlight">highlighted</span> text.</p>'
        html = markdown.markdown(text, extensions=[MyExtension()])
        self.assertEqual(html, expected)

    def test_multiple_highlights(self):
        text = "!!one!! and !!two!!"
        expected = '<p><span class="custom-highlight">one</span> and <span class="custom-highlight">two</span></p>'
        html = markdown.markdown(text, extensions=[MyExtension()])
        self.assertEqual(html, expected)

    def test_no_match(self):
        text = "This is normal text."
        expected = '<p>This is normal text.</p>'
        html = markdown.markdown(text, extensions=[MyExtension()])
        self.assertEqual(html, expected)

if __name__ == '__main__':
    unittest.main()
