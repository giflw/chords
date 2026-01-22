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

from chordsmd.parser import parse_chord

class HighlightPattern(Pattern):
    def handleMatch(self, m):
        text = m.group(2)
        chord_data = parse_chord(text)
        
        if chord_data:
            el = ElementTree.Element('span')
            el.set('class', 'chord')
            
            root_el = ElementTree.SubElement(el, 'span')
            root_el.set('class', 'root')
            root_el.text = chord_data['root']
            
            if chord_data['quality']:
                qual_el = ElementTree.SubElement(el, 'span')
                qual_el.set('class', 'quality')
                qual_el.text = chord_data['quality']
                
            if chord_data['bass']:
                bass_el = ElementTree.SubElement(el, 'span')
                bass_el.set('class', 'bass')
                # Conventionally display standard slash for bass
                bass_el.text = '/' + chord_data['bass']
                
            return el
        else:
            # Fallback for non-chord text
            el = ElementTree.Element('span')
            el.text = text
            el.set('class', 'custom-highlight')
            return el

from chordsmd.blocks import ChordsBlockPreprocessor

class MyExtension(Extension):
    def extendMarkdown(self, md):
        # Register the pattern
        # Priority 175 is standard for inline patterns, keeping it safe
        md.inlinePatterns.register(HighlightPattern(PATTERN, md), 'custom_highlight', 175)
        
        # Register Preprocessor
        # Priority > 30 to run before standard block parsing?
        # Fenced code blocks are usually handled by Preprocessors.
        # We need to run before the standard Fenced Code Block preprocessor if we want to hijack it?
        # Standard 'fenced_code_block' is priority 25 (in Preprocessors).
        # We'll use 30 to catch it first.
        md.preprocessors.register(ChordsBlockPreprocessor(md), 'chords_block', 30)

def makeExtension(**kwargs):
    return MyExtension(**kwargs)
