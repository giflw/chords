import re
from markdown.preprocessors import Preprocessor
from .merger import merge_chords_and_lyrics

class ChordsBlockPreprocessor(Preprocessor):
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
        
        for raw_block in raw_blocks:
            lines = raw_block.strip('\n').split('\n')
            if not lines: continue
            
            # Check if this block STARTs with a header?
            # Or is the block JUST a header?
            # If the user writes:
            # [Chorus]
            # Am
            # Lyrics
            #
            # Is that one block? Yes.
            # We should peel off the header.
            
            idx = 0
            while idx < len(lines):
                line = lines[idx]
                header_match = self.SECTION_HEADER_RE.match(line.strip())
                if header_match:
                    title = header_match.group(1)
                    html_parts.append(f'<section class="sheet-section"><h3>{title}</h3></section>')
                    idx += 1
                    # If the rest of the block is empty, done with this block
                    continue
                
                # If not a header, the rest of this 'raw_block' is a paragraph
                # But wait, if we had a header, we closed it? 
                # <section><h3>Title</h3></section> is what we emit.
                # The lyrics follow.
                # Should we wrap the lyrics IN the section? 
                # Plan said: <section><h3>...</h3>... content ...</section>
                # But my implementation emitting closed sections: <section...></section>.
                # Let's fix that too.
                
                # Actually, simpler is to just emit the h3 and let the user structure it, 
                # or treat [Section] as a divider.
                # Let's keep emitting closed sections for the Header itself unless we want to wrap content.
                # Tests expect: <section ...><h3>Chorus</h3></section> and then content? 
                # Test says: assertIn('<section...>', html).
                
                # Let's treat the rest of lines as a paragraph
                remaining_lines = lines[idx:]
                if remaining_lines:
                    html_parts.append(self.process_paragraph(remaining_lines))
                break
                
        html_parts.append('</div>')
        return "\n".join(html_parts)

    def process_paragraph(self, lines):
        output_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            
            # Simple heuristic for now:
            # If line is mostly chords (check parser? or just spaces + capital letters?)
            # And next line exists.
            # Assume strict alternation? Pro users might just write chords.
            
            # IMPROVED HEURISTIC:
            # A chord line usually has strict spacing chars (space/tab) vs non-space ratio.
            # But let's check if the NEXT line is a "Lyric line".
            
            # Let's assume for this iteration:
            # Line 1: Chords
            # Line 2: Lyrics
            # Unless Line 1 doesn't look like chords.
            
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
        
        # If > 30% spaces, probable chord line? 
        # "I am a boy" has 3 spaces / 10 chars = 30%.
        # "Am    G"    has 4 spaces / 7 chars = 57%.
        
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
