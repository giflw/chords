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
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Scene Heading (INT./EXT. or starts with .)
            if self.is_scene_heading(line):
                html_parts.append(f'<div class="scene-heading">{self.escape_html(line)}</div>')
                i += 1
                continue
            
            # Character (ALL CAPS, possibly with extension in parentheses)
            if self.is_character(line):
                char_name = line.strip()
                html_parts.append(f'<div class="character">{self.escape_html(char_name)}</div>')
                i += 1
                
                # Check for parenthetical and dialogue
                dialogue_parts = []
                while i < len(lines):
                    next_line = lines[i].strip()
                    if not next_line:
                        break
                    if self.is_parenthetical(next_line):
                        dialogue_parts.append(f'<div class="parenthetical">{self.escape_html(next_line)}</div>')
                    elif not self.is_character(next_line) and not self.is_scene_heading(next_line):
                        dialogue_parts.append(f'<div class="dialogue">{self.escape_html(next_line)}</div>')
                    else:
                        break
                    i += 1
                
                if dialogue_parts:
                    html_parts.extend(dialogue_parts)
                continue
            
            # Transition (ends with TO:)
            if self.is_transition(line):
                html_parts.append(f'<div class="transition">{self.escape_html(line)}</div>')
                i += 1
                continue
            
            # Action/Description
            if line.strip():
                html_parts.append(f'<div class="action">{self.escape_html(line)}</div>')
            else:
                html_parts.append('<div class="blank-line"></div>')
            
            i += 1
        
        html_parts.append('</div>')
        return "\n".join(html_parts)
    
    def is_scene_heading(self, line):
        line = line.strip()
        # Forced scene heading with .
        if line.startswith('.') and len(line) > 1:
            return True
        # Standard INT./EXT.
        if re.match(r'^(INT|EXT|EST|INT\./EXT|I/E)[\.\s]', line, re.IGNORECASE):
            return True
        return False
    
    def is_character(self, line):
        line = line.strip()
        if not line:
            return False
        # Character names are ALL CAPS (may have extension in parens)
        # Remove parenthetical extension for check
        name = re.sub(r'\s*\(.*?\)\s*$', '', line)
        return name.isupper() and len(name) > 0 and not self.is_scene_heading(line)
    
    def is_parenthetical(self, line):
        line = line.strip()
        return line.startswith('(') and line.endswith(')')
    
    def is_transition(self, line):
        line = line.strip()
        return line.endswith('TO:') and line.isupper()
    
    def escape_html(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class FountainExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(FountainPreprocessor(md), 'fountain_block', 31)

def makeExtension(**kwargs):
    return FountainExtension(**kwargs)
