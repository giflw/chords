import unittest
from markdown import Markdown
# We import by module name to test makeExtension
import chordsmd

class TestConfig(unittest.TestCase):
    def test_default_enabled(self):
        md = Markdown(extensions=['chordsmd'])
        
        # Test Chords
        html = md.convert("```chords\nAm\n```")
        self.assertIn('class="chords-sheet"', html)
        
        # Test Tabs
        html = md.convert("```tab\ne|---|\n```")
        self.assertIn('<svg', html)

    def test_disable_chords(self):
        # Disable chords
        configs = {
            'chordsmd': {
                'enable_chords': False
            }
        }
        md = Markdown(extensions=['chordsmd'], extension_configs=configs)
        
        text = "```chords\nAm\n```"
        html = md.convert(text)
        # Should NOT be processed as chords sheet, but as standard code block
        self.assertNotIn('class="chords-sheet"', html)
        self.assertIn('<code', html) # Standard markdown code block

    def test_disable_tabs(self):
        configs = {
            'chordsmd': {
                'enable_tabs': False
            }
        }
        md = Markdown(extensions=['chordsmd'], extension_configs=configs)
        
        text = "```tab\ne|---|\n```"
        html = md.convert(text)
        self.assertNotIn('<svg', html)
        self.assertIn('<code', html)

if __name__ == '__main__':
    unittest.main()
