import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from xml.sax.saxutils import escape

class TabPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*tab[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

    def run(self, lines):
        text = "\n".join(lines)
        def replace(match):
            return self.render_tab_svg(match.group(1))
        return self.FENCED_BLOCK_RE.sub(replace, text).split('\n')

    def render_tab_svg(self, ascii_tab):
        lines = ascii_tab.strip().split('\n')
        
        # Filter valid tab lines (heuristic: starts with label + separator or just separator)
        # e.g. "e|---", "G|---", "|---", "----"
        tab_lines = []
        labels = []
        content_lines = []
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Simple heuristic: must contain at least 3 dashes/pipes
            if line.count('-') + line.count('|') < 3:
                continue
                
            # Extract label
            # Find first occurrence of '|' or '-'
            match = re.search(r'[\|\-]', line)
            if match:
                idx = match.start()
                label = line[:idx].strip()
                content = line[idx:]
                labels.append(label)
                content_lines.append(content)
                tab_lines.append(line)
        
        if not tab_lines:
            return '<pre>' + escape(ascii_tab) + '</pre>'

        num_strings = len(tab_lines)
        max_len = max(len(c) for c in content_lines)
        
        # SVG Dimensions
        char_width = 9  # Monospace char width approx
        line_height = 20
        start_x = 40 # Space for labels
        width = start_x + (max_len * char_width) + 20
        height = (num_strings + 1) * line_height
        
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" class="tab-svg" viewBox="0 0 {width} {height}" width="100%" style="font-family: monospace; font-size: 14px; background: white;">'
        ]
        
        # Draw Strings
        for i in range(num_strings):
            y = (i + 1) * line_height
            # Label
            svg_parts.append(f'<text x="5" y="{y+4}" fill="#000" style="font-weight:bold">{escape(labels[i])}</text>')
            # Line
            svg_parts.append(f'<line x1="{start_x}" y1="{y}" x2="{width-10}" y2="{y}" stroke="#999" stroke-width="1" />')
            
            # Content
            content = content_lines[i]
            for char_idx, char in enumerate(content):
                cx = start_x + (char_idx * char_width)
                
                if char.isdigit():
                    # Draw number with background rect to mask line
                    svg_parts.append(f'<rect x="{cx-2}" y="{y-8}" width="{char_width}" height="16" fill="white" />')
                    svg_parts.append(f'<text x="{cx+2}" y="{y+4}" fill="#000">{char}</text>')
                elif char == '|':
                    svg_parts.append(f'<line x1="{cx+4}" y1="{y-line_height/2}" x2="{cx+4}" y2="{y+line_height/2}" stroke="#000" stroke-width="1.5" />')
                elif char in ('h', 'p', '/', '\\', 'x'):
                    # Articulations
                     svg_parts.append(f'<rect x="{cx-2}" y="{y-8}" width="{char_width}" height="16" fill="white" />')
                     svg_parts.append(f'<text x="{cx+2}" y="{y+4}" fill="#000" style="font-size: 10px;">{escape(char)}</text>')
        
        # Connect vertical bars across strings?
        # A proper renderer would find columns of '|' and draw a single long line.
        # For now, individual segments work visually if aligned.
        
        svg_parts.append('</svg>')
        return "".join(svg_parts)

class TabExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(TabPreprocessor(md), 'tab_block', 32)

def makeExtension(**kwargs):
    return TabExtension(**kwargs)
