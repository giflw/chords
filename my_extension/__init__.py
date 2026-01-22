from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

# The pattern to match: !!text!!
# The capturing group (text) is group 2 because SimpleTagPattern uses a generic regex
PATTERN = r'!!(.*?)!!'

class MyExtension(Extension):
    def extendMarkdown(self, md):
        # Create an inline pattern that matches the pattern and wraps it in a span
        # The 'custom_highlight' is the key for the pattern registry
        # 'span' is the tag name
        # 'custom-highlight' is the class attribute
        pattern = SimpleTagPattern(PATTERN, 'span')
        # We need to set the class attribute on the element produced by SimpleTagPattern
        # However, SimpleTagPattern typically just creates the tag. 
        # Actually, looking at SimpleTagPattern source/docs: 
        # SimpleTagPattern(pattern, tag) returns an Element with that tag.
        # To add attributes like class, we might need a slightly more complex pattern or subclass.
        
        # Let's use a custom pattern to ensure we can set the class
        pass

# Re-implementing with a custom pattern to ensure we get the class attribute correct
from markdown.inlinepatterns import Pattern
from xml.etree import ElementTree

class HighlightPattern(Pattern):
    def handleMatch(self, m):
        el = ElementTree.Element('span')
        el.text = m.group(2)
        el.set('class', 'custom-highlight')
        return el

class MyExtension(Extension):
    def extendMarkdown(self, md):
        # Register the pattern
        # Priority 175 is standard for inline patterns, keeping it safe
        md.inlinePatterns.register(HighlightPattern(PATTERN, md), 'custom_highlight', 175)

def makeExtension(**kwargs):
    return MyExtension(**kwargs)
