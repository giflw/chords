import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import Pattern
from xml.etree import ElementTree
from .merger import merge_chords_and_lyrics
from .parser import parse_chord

# Pattern for inline chords via !!Chord!! syntax
INLINE_CHORD_PATTERN = r'!!(.*?)!!'

class InlineChordPattern(Pattern):
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

class ChordSheetPreprocessor(Preprocessor):
    """
    Finds fenced code blocks with language 'chords' and processes them.
    """
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*chords[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )
    
    SECTION_HEADER_RE = re.compile(r'^\[(.*?)\]$')

    def run(self, lines):
        text = "\n".join(lines)
        
        def replace(match):
            content = match.group(1)
            return self.process_chords_content(content)
            
        new_text = self.FENCED_BLOCK_RE.sub(replace, text)
        return new_text.split("\n")

    def process_chords_content(self, text):
        # Improved processing: iterate through lines and grouping
        html_parts = ['<div class="chords-sheet">']
        
        # logical blocks (separated by empty lines in source)
        raw_blocks = re.split(r'\n\s*\n', text.strip('\n'))
        
        section_open = False
        
        for raw_block in raw_blocks:
            lines = raw_block.strip('\n').split('\n')
            if not lines: continue
            
            idx = 0
            while idx < len(lines):
                line = lines[idx]
                header_match = self.SECTION_HEADER_RE.match(line.strip())
                if header_match:
                    # If we had a section open, close it
                    if section_open:
                        html_parts.append('</section>')
                    
                    title = header_match.group(1)
                    html_parts.append(f'<section class="sheet-section"><h3>{title}</h3>')
                    section_open = True
                    idx += 1
                    # Continue to look for content in *this* block (e.g. [Chorus]\nAm...)
                    continue
                
                # Content
                # If we have content but NO section open, should we open a default one?
                # Or just append as direct child of chords-sheet?
                # Usually better to append as direct child if implicit.
                
                remaining_lines = lines[idx:]
                if remaining_lines:
                    html_parts.append(self.process_paragraph(remaining_lines))
                # Consumed rest of block
                break
        
        # Close any lingering section
        if section_open:
            html_parts.append('</section>')
            
        html_parts.append('</div>')
        return "\n".join(html_parts)

    def process_paragraph(self, lines):
        output_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            
            if self.is_chord_line(line):
                # Check next line
                if i + 1 < len(lines) and not self.is_chord_line(lines[i+1]):
                    # Merge
                    merged = merge_chords_and_lyrics(line, lines[i+1])
                    output_lines.append(merged)
                    i += 2
                else:
                    # Orphan chord line
                    merged = merge_chords_and_lyrics(line, "")
                    output_lines.append(merged)
                    i += 1
            else:
                # Lyric line without chords
                output_lines.append(line)
                i += 1
                
        return '<p>' + '<br>\n'.join(output_lines) + '</p>'

    def is_chord_line(self, line):
        # Heuristic:
        # 1. Contains at least one chord-like token.
        # 2. Contains mostly spaces or chord chars.
        
        # Very simple check: mostly spaces
        if not line.strip():
            return False
            
        # Count spaces
        spaces = line.count(' ')
        total = len(line)
        if total == 0: return False
        
        # Better: Check tokens.
        tokens = line.split()
        possible_chords = 0
        from .parser import parse_chord
        for token in tokens:
            # Check if it matches our chord regex from parser logic
            if parse_chord(token):
                possible_chords += 1
                
        if len(tokens) > 0 and (possible_chords / len(tokens)) > 0.8:
            return True
            
        return False

class ChordSheetExtension(Extension):
    def extendMarkdown(self, md):
        # Register the pattern
        md.inlinePatterns.register(InlineChordPattern(INLINE_CHORD_PATTERN, md), 'inline_chord', 175)
        # Register Preprocessor
        md.preprocessors.register(ChordSheetPreprocessor(md), 'chords_block', 30)

def makeExtension(**kwargs):
    return ChordSheetExtension(**kwargs)
