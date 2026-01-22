import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class FountainPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*fountain[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

    def run(self, lines):
        text = "\n".join(lines)
        def replace(match):
            return self.render_fountain(match.group(1))
        return self.FENCED_BLOCK_RE.sub(replace, text).split('\n')

    def render_fountain(self, content):
        lines = content.strip().split('\n')
        html_parts = ['<div class="fountain-screenplay">']
        
        # Check for title page (must be at start)
        title_page_html = self.parse_title_page(lines)
        if title_page_html:
            html_parts.append(title_page_html)
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip empty lines (but preserve them as spacing)
            if not line.strip():
                html_parts.append('<div class="blank-line"></div>')
                i += 1
                continue
            
            # Page break (===)
            if re.match(r'^={3,}$', line.strip()):
                html_parts.append('<div class="page-break">* * *</div>')
                i += 1
                continue
            
            # Notes [[note]] - remove them
            line = re.sub(r'\[\[.*?\]\]', '', line)
            if not line.strip():
                i += 1
                continue
            
            # Centered text (>TEXT<)
            if line.strip().startswith('>') and line.strip().endswith('<'):
                text = line.strip()[1:-1].strip()
                html_parts.append(f'<div class="centered">{self.apply_emphasis(text)}</div>')
                i += 1
                continue
            
            # Lyrics (~text)
            if line.strip().startswith('~'):
                text = line.strip()[1:]
                html_parts.append(f'<div class="lyrics">{self.apply_emphasis(text)}</div>')
                i += 1
                continue
            
            # Forced transition (>text)
            if line.strip().startswith('>') and not line.strip().endswith('<'):
                text = line.strip()[1:]
                html_parts.append(f'<div class="transition">{self.apply_emphasis(text)}</div>')
                i += 1
                continue
            
            # Forced scene heading (.HEADING)
            if line.strip().startswith('.') and len(line.strip()) > 1 and line.strip()[1].isalnum():
                text = line.strip()[1:]  # Remove leading period
                # Remove scene numbers #1#
                text = re.sub(r'#[A-Za-z0-9\-\.]+#\s*$', '', text).strip()
                html_parts.append(f'<div class="scene-heading">{self.apply_emphasis(text)}</div>')
                i += 1
                continue
            
            # Scene Heading (INT./EXT. or with scene numbers)
            if self.is_scene_heading(line):
                text = line.strip()
                # Remove scene numbers
                text = re.sub(r'#[A-Za-z0-9\-\.]+#\s*$', '', text).strip()
                html_parts.append(f'<div class="scene-heading">{self.apply_emphasis(text)}</div>')
                i += 1
                continue
            
            # Transition (must check before character - ends with TO:)
            if self.is_transition(line):
                html_parts.append(f'<div class="transition">{self.apply_emphasis(line.strip())}</div>')
                i += 1
                continue
            
            # Forced character (@CHARACTER)
            if line.strip().startswith('@'):
                char_name = line.strip()[1:]  # Remove @
                is_dual = char_name.rstrip().endswith('^')
                if is_dual:
                    char_name = char_name.rstrip()[:-1].rstrip()  # Remove ^
                    html_parts.append(f'<div class="character dual">{self.escape_html(char_name)}</div>')
                else:
                    html_parts.append(f'<div class="character">{self.escape_html(char_name)}</div>')
                i += 1
                
                # Process dialogue
                dialogue_parts = self.process_dialogue(lines, i)
                html_parts.extend(dialogue_parts[0])
                i = dialogue_parts[1]
                continue
            
            # Character (ALL CAPS, possibly with extension in parentheses)
            if self.is_character(line):
                char_name = line.strip()
                is_dual = char_name.rstrip().endswith('^')
                if is_dual:
                    char_name = char_name.rstrip()[:-1].rstrip()  # Remove ^
                    html_parts.append(f'<div class="character dual">{self.escape_html(char_name)}</div>')
                else:
                    html_parts.append(f'<div class="character">{self.escape_html(char_name)}</div>')
                i += 1
                
                # Process dialogue
                dialogue_parts = self.process_dialogue(lines, i)
                html_parts.extend(dialogue_parts[0])
                i = dialogue_parts[1]
                continue
            
            # Action/Description (default)
            if line.strip():
                html_parts.append(f'<div class="action">{self.apply_emphasis(line)}</div>')
            
            i += 1
        
        html_parts.append('</div>')
        return "\n".join(html_parts)
    
    def parse_title_page(self, lines):
        """Parse title page if present at start"""
        title_parts = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Title page ends at first blank line
            if not line.strip():
                break
            # Check for key: value format
            if ':' in line and not line.strip().startswith(' '):
                key_match = re.match(r'^([^:]+):\s*(.*)$', line)
                if key_match:
                    key = key_match.group(1).strip()
                    value = key_match.group(2).strip()
                    title_parts.append(f'<div class="title-{key.lower().replace(" ", "-")}">{self.apply_emphasis(value)}</div>')
                    i += 1
                    continue
            # Not a title page
            break
        
        if title_parts:
            # Remove parsed lines from content
            del lines[:i+1]  # +1 to include blank line
            return '<div class="title-page">' + '\n'.join(title_parts) + '</div>'
        return None
    
    def process_dialogue(self, lines, start_idx):
        """Process dialogue and parentheticals after a character"""
        dialogue_parts = []
        i = start_idx
        
        while i < len(lines):
            next_line = lines[i].strip()
            if not next_line:
                break
            if self.is_parenthetical(next_line):
                dialogue_parts.append(f'<div class="parenthetical">{self.apply_emphasis(next_line)}</div>')
            elif not self.is_character(next_line) and not self.is_scene_heading(next_line) and not self.is_transition(next_line):
                dialogue_parts.append(f'<div class="dialogue">{self.apply_emphasis(next_line)}</div>')
            else:
                break
            i += 1
        
        return (dialogue_parts, i)
    
    def is_scene_heading(self, line):
        line = line.strip()
        # Standard INT./EXT.
        if re.match(r'^(INT|EXT|EST|INT\./EXT|INT/EXT|I/E)[\.\s]', line, re.IGNORECASE):
            return True
        return False
    
    def is_character(self, line):
        line = line.strip()
        if not line:
            return False
        # Remove dual dialogue marker
        if line.endswith('^'):
            line = line[:-1].rstrip()
        # Remove character extension (O.S.), (V.O.), etc.
        name = re.sub(r'\s*\(.*?\)\s*$', '', line)
        # Must be uppercase and contain at least one letter
        return name.isupper() and re.search(r'[A-Z]', name) and not self.is_scene_heading(line)
    
    def is_parenthetical(self, line):
        line = line.strip()
        return line.startswith('(') and line.endswith(')')
    
    def is_transition(self, line):
        line = line.strip()
        return line.endswith('TO:') and line.isupper()
    
    def apply_emphasis(self, text):
        """Apply Fountain emphasis: *italic*, **bold**, _underline_"""
        # Escape HTML first
        text = self.escape_html(text)
        
        # Bold italics ***text***
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        # Bold **text**
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic *text*
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Underline _text_
        text = re.sub(r'_(.+?)_', r'<u>\1</u>', text)
        
        return text
    
    def escape_html(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class FountainExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(FountainPreprocessor(md), 'fountain_block', 31)

def makeExtension(**kwargs):
    return FountainExtension(**kwargs)
