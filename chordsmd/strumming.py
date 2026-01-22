import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class StrummingPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*strum(?:ming)?[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

    def run(self, lines):
        text = "\n".join(lines)
        def replace(match):
            return self.render_strumming(match.group(1))
        return self.FENCED_BLOCK_RE.sub(replace, text).split('\n')

    def render_strumming(self, content):
        lines = content.strip().split('\n')
        html_parts = ['<div class="strumming-pattern">']
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line has a label (e.g., "Verse: D DU UDU")
            if ':' in line:
                label, pattern = line.split(':', 1)
                html_parts.append(f'<div class="pattern-section">')
                html_parts.append(f'<div class="pattern-label">{self.escape_html(label.strip())}</div>')
                html_parts.append(self.parse_pattern(pattern.strip()))
                html_parts.append('</div>')
            else:
                # Just a pattern
                html_parts.append(self.parse_pattern(line))
        
        html_parts.append('</div>')
        return "\n".join(html_parts)
    
    def parse_pattern(self, pattern):
        """Parse strumming pattern and convert to visual representation"""
        # Pattern notation:
        # V or D or ↓ = downstroke (uppercase = strong beat)
        # v or d = downstroke (lowercase = weak beat)
        # A or ^ or U or ↑ = upstroke (uppercase = strong beat)
        # a or u = upstroke (lowercase = weak beat)
        # X or x = muted strum
        # - = rest/pause
        # | = bar line
        # ( ) = grouping
        # Numbers = beat numbers
        
        result = ['<div class="strum-sequence">']
        
        # Split by spaces but preserve grouping
        tokens = pattern.split()
        
        for token in tokens:
            if token == '|':
                result.append('<span class="bar-line">|</span>')
            elif token.isdigit():
                result.append(f'<span class="beat-number">{token}</span>')
            elif token in ['(', ')']:
                result.append(f'<span class="group-marker">{token}</span>')
            else:
                # Parse individual strokes
                result.append('<span class="stroke-group">')
                for char in token:
                    # Determine if strong beat (uppercase) or weak beat (lowercase)
                    is_strong = char.isupper() or char in ['↓', '↑']
                    
                    # Downstroke
                    if char in ['V', 'D', '↓']:
                        result.append('<span class="stroke down strong" title="Downstroke (strong)">↓</span>')
                    elif char in ['v', 'd']:
                        result.append('<span class="stroke down weak" title="Downstroke (weak)">↓</span>')
                    # Upstroke
                    elif char in ['A', '^', 'U', '↑']:
                        result.append('<span class="stroke up strong" title="Upstroke (strong)">↑</span>')
                    elif char in ['a', 'u']:
                        result.append('<span class="stroke up weak" title="Upstroke (weak)">↑</span>')
                    # Muted
                    elif char.upper() == 'X':
                        result.append('<span class="stroke muted" title="Muted">✕</span>')
                    # Rest
                    elif char == '-':
                        result.append('<span class="stroke rest" title="Rest">-</span>')
                result.append('</span>')
        
        result.append('</div>')
        return ''.join(result)
    
    def escape_html(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class StrummingExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(StrummingPreprocessor(md), 'strumming_block', 29)

def makeExtension(**kwargs):
    return StrummingExtension(**kwargs)
