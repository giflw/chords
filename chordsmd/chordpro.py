import re
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
from xml.etree import ElementTree

# Directive Pattern: {title: Syntax} or {soc}
# Matches {key} or {key: value}
DIRECTIVE_RE = re.compile(r'^{(.*?)(?::\s*(.*))?}$')

# Inline Chord Pattern: [Am]
CHORD_PATTERN = r'\[([A-G][#b]?(?:m|min|maj|dim|aug|sus|[0-9])*(?:\/[A-G][#b]?)?)\]'

class ChordProPattern(Pattern):
    def handleMatch(self, m):
        chord_text = m.group(2)
        el = ElementTree.Element('span')
        el.set('class', 'chord')
        el.text = chord_text
        return el

class ChordProBlockProcessor(BlockProcessor):
    def test(self, parent, block):
        # We handle EVERYTHING in chordpro mode?
        # Or should we only handle blocks that look like ChordPro?
        # Typically ChordPro files are purely ChordPro.
        # But here we are making an extension to Markdown.
        # So we should probably delimit ChordPro blocks?
        # Usage:
        # ```chordpro
        # {t: Title}
        # [C]Hello
        # ```
        # OR we can just support the inline syntax globally? 
        # The prompt said "add new extension entrypoint".
        # If user loads `chordsmd.chordpro` extension, maybe they expect the whole file to be treated as such?
        # But Markdown is Markdown.
        # Let's assume we want a Fenced Code Block for ChordPro too, OR inline support.
        # Standard ChordPro in Markdown is usually a code block.
        # Let's implement a Preprocessor for ```chordpro blocks, similar to our `chords` block.
        return False # We use Preprocessor instead

from markdown.preprocessors import Preprocessor

class ChordProPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*chordpro[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

    def run(self, lines):
        text = "\n".join(lines)
        def replace(match):
            return self.process_chordpro(match.group(1))
        return self.FENCED_BLOCK_RE.sub(replace, text).split('\n')

    def process_chordpro(self, text):
        lines = text.strip().split('\n')
        html_parts = ['<div class="chordpro-sheet">']
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Directives
            d_match = DIRECTIVE_RE.match(line)
            if d_match:
                key = d_match.group(1).lower()
                val = d_match.group(2)
                
                if key in ('t', 'title'):
                    html_parts.append(f'<h1>{val}</h1>')
                elif key in ('st', 'subtitle'):
                    html_parts.append(f'<h2>{val}</h2>')
                elif key == 'soc':
                    html_parts.append('<section class="chorus">')
                elif key == 'eoc':
                    html_parts.append('</section>')
                # Ignore others or handle them
                continue
            
            # Lyrics with chords
            # We can use the Pattern we defined? 
            # Or manually replace [Chord] -> <span...
            # Since we are in a Preprocessor, we are generating raw HTML that Markdown might re-process?
            # Or we return a placeholder?
            # If we return HTML, we should stash it?
            # For simplicity, let's manually transform [Chord] to <span class="chord">Chord</span>
            # and wrap line in <p> or <div class="line">.
            
            # Simple regex replacement for [Chord]
            processed_line = re.sub(
                CHORD_PATTERN,
                r'<span class="chord">\1</span>',
                line
            )
            html_parts.append(f'<p class="chordpro-line">{processed_line}</p>')
            
        html_parts.append('</div>')
        return "\n".join(html_parts)

class ChordProExtension(Extension):
    def extendMarkdown(self, md):
        # Register Preprocessor for ```chordpro blocks
        md.preprocessors.register(ChordProPreprocessor(md), 'chordpro_block', 31)
        
        # We could also add inline pattern for global [Chord] support if desired,
        # but Plan specified fenced blocks implicitly by reusing `blocks` logic/css.
        # Actually Plan said "Inline Chords... range [Chord]".
        # And "Use same CSS".
        pass

def makeExtension(**kwargs):
    return ChordProExtension(**kwargs)
