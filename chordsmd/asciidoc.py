import re
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.preprocessors import Preprocessor

# Inline Patterns
SUPERSCRIPT_RE = r'(\^)([^\^]+)\^'
SUBSCRIPT_RE = r'((?<!\[)~)([^~]+)~'  # Avoid matching [~]
MONOSPACE_RE = r'(\+)([^\+]+)\+'
HIGHLIGHT_RE = r'((?<!\[)#)([^#]+)#'  # Avoid matching [#]
BOLD_RE = r'(\*)([^\*]+)\*'
ITALIC_RE = r'(_)([^_]+)_'
STRIKETHROUGH_RE = r'(\[~\])([^\[]+)\[~\]'
UNDERLINE_RE = r'(\[_\])([^\[]+)\[_\]'
DOUBLE_QUOTES_RE = r'(``)([^`\']+)\'\''
SINGLE_QUOTES_RE = r'(`)([^`\']+)\''

class AdmonitionPreprocessor(Preprocessor):
    """
    Render AsciiDoc-style admonitions:
    NOTE: This is a note.
    TIP: This is a tip.
    """
    ADMONITION_RE = re.compile(r'^(NOTE|TIP|IMPORTANT|WARNING|CAUTION):[ ]*(.*)$', re.IGNORECASE)

    def run(self, lines):
        new_lines = []
        for line in lines:
            match = self.ADMONITION_RE.match(line)
            if match:
                type_ = match.group(1).upper()
                content = match.group(2)
                # Convert to a div with a class
                new_lines.append(f'<div class="admonition {type_.lower()}">')
                new_lines.append(f'<p class="admonition-title">{type_}</p>')
                new_lines.append(f'<p>{content}</p>')
                new_lines.append('</div>')
            else:
                new_lines.append(line)
        return new_lines

class AsciidocExtension(Extension):
    def extendMarkdown(self, md):
        # Register inline patterns with high priority (Default Markdown emphasis is around 170, backticks 190)
        # We use 200+ to ensure we override them for these specific markers.
        md.inlinePatterns.register(SimpleTagInlineProcessor(SUPERSCRIPT_RE, 'sup'), 'superscript', 205)
        md.inlinePatterns.register(SimpleTagInlineProcessor(SUBSCRIPT_RE, 'sub'), 'subscript', 206)
        md.inlinePatterns.register(SimpleTagInlineProcessor(MONOSPACE_RE, 'code'), 'asciidoc_monospace', 207)
        md.inlinePatterns.register(SimpleTagInlineProcessor(HIGHLIGHT_RE, 'mark'), 'asciidoc_highlight', 208)
        md.inlinePatterns.register(SimpleTagInlineProcessor(BOLD_RE, 'strong'), 'asciidoc_bold', 209)
        md.inlinePatterns.register(SimpleTagInlineProcessor(ITALIC_RE, 'em'), 'asciidoc_italic', 211) # Swap priorities
        md.inlinePatterns.register(SimpleTagInlineProcessor(STRIKETHROUGH_RE, 'del'), 'asciidoc_strikethrough', 212)
        md.inlinePatterns.register(SimpleTagInlineProcessor(UNDERLINE_RE, 'u'), 'asciidoc_underline', 213)
        md.inlinePatterns.register(SimpleTagInlineProcessor(DOUBLE_QUOTES_RE, 'span'), 'asciidoc_double_quotes', 215) # Highest
        md.inlinePatterns.register(SimpleTagInlineProcessor(SINGLE_QUOTES_RE, 'span'), 'asciidoc_single_quotes', 210) # Lower
        
        # Note: double quotes in AsciiDoc usually render with specific entities, 
        # but SimpleTagInlineProcessor needs a tag. Let's use span for those for now.
        
        # Register preprocessor for admonitions
        md.preprocessors.register(AdmonitionPreprocessor(md), 'admonition', 25)

def makeExtension(**kwargs):
    return AsciidocExtension(**kwargs)
