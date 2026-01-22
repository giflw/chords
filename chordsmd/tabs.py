import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from xml.sax.saxutils import escape

class TabPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*tab[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

def render_tab_svg(ascii_tab):
    lines = ascii_tab.strip().split('\n')
    
    # Pass 1: Find valid tab lines and determine the "anchor" column (where content starts)
    # We look for lines with dividers like '|' or '-'
    tab_lines_indices = []
    anchor_indices = []
    
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line: continue
        
        # Heuristic for Standard Tab Line: contains at least 3 dashes or pipes
        if line.count('-') + line.count('|') >= 3:
            match = re.search(r'[\|\-]', line)
            if match:
                anchor_indices.append(match.start())
                tab_lines_indices.append(i)
    
    if not anchor_indices:
        # Fallback for completely weird blocks
        return '<pre>' + escape(ascii_tab) + '</pre>'
        
    # Use the most common anchor index or the minimum? 
    # Usually they line up. Let's use the mode or first.
    from statistics import mode
    try:
        anchor_idx = mode(anchor_indices)
    except:
        anchor_idx = anchor_indices[0] if anchor_indices else 0

    # Pass 2: Process All Lines relative to anchor
    # We include:
    # 1. Identified Tab Lines
    # 2. "Arrow" lines (contain ↓)
    # 3. Maybe others?
    
    final_rows = []
    
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line: continue
        
        is_tab = i in tab_lines_indices
        is_arrow = not is_tab and any(c in '↓↑VvA^' for c in line)
        
        if not (is_tab or is_arrow):
            continue
            
        # Extract Label and Content
        # Content starts at anchor_idx
        if len(line) > anchor_idx:
            content = line[anchor_idx:]
            label = line[:anchor_idx].strip()
        else:
            content = ""
            label = line.strip()
            
        final_rows.append({
            'type': 'tab' if is_tab else 'arrow',
            'label': label,
            'content': content
        })
        
    if not final_rows:
        return '<pre>' + escape(ascii_tab) + '</pre>'

    num_strings = len(final_rows)
    max_len = max(len(r['content']) for r in final_rows) if final_rows else 0
    
    # SVG Dimensions
    char_width = 9 
    line_height = 20
    start_x = 40 
    width = start_x + (max_len * char_width) + 20
    height = (num_strings + 1) * line_height
    
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" class="tab-svg" viewBox="0 0 {width} {height}" width="100%" style="font-family: monospace; font-size: 14px; background: white;">'
    ]
    
    for i, row in enumerate(final_rows):
        y = (i + 1) * line_height
        
        if row['type'] == 'tab':
            # Label
            svg_parts.append(f'<text x="5" y="{y+4}" fill="#000" style="font-weight:bold">{escape(row["label"])}</text>')
            # Line
            svg_parts.append(f'<line x1="{start_x}" y1="{y}" x2="{width-10}" y2="{y}" stroke="#999" stroke-width="1" />')
        else:
            # Arrow Line - No Line, No Label usually
            pass

        # Content
        content = row['content']
        for char_idx, char in enumerate(content):
            cx = start_x + (char_idx * char_width)
            
            if char == ' ': continue
            
            if char.isdigit():
                svg_parts.append(f'<rect x="{cx-2}" y="{y-8}" width="{char_width}" height="16" fill="white" />')
                svg_parts.append(f'<text x="{cx+2}" y="{y+4}" fill="#000">{char}</text>')
            elif char == '|':
                svg_parts.append(f'<line x1="{cx+4}" y1="{y-line_height/2}" x2="{cx+4}" y2="{y+line_height/2}" stroke="#000" stroke-width="1.5" />')
            elif char in ('h', 'p', '/', '\\', 'x'):
                 svg_parts.append(f'<rect x="{cx-2}" y="{y-8}" width="{char_width}" height="16" fill="white" />')
                 svg_parts.append(f'<text x="{cx+2}" y="{y+4}" fill="#000" style="font-size: 10px;">{escape(char)}</text>')
            elif char in ('↓', '↑', 'V', 'v', 'A', '^'):
                 is_down = char in ('↓', 'V', 'v')
                 is_strong = char in ('↓', 'V', 'A', '↑')
                 color = "#2196f3" if is_down else "#f44336" # Use consistent colors with strumming
                 weight = "bold" if is_strong else "normal"
                 opacity = "1" if is_strong else "0.7"
                 font_size = "14px" if is_strong else "12px"
                 arrow_char = '↓' if is_down else '↑'
                 svg_parts.append(f'<text x="{cx+2}" y="{y+4}" fill="{color}" style="font-weight:{weight}; opacity:{opacity}; font-size:{font_size};">{arrow_char}</text>')
    
    # Connect vertical bars across strings?
    # A proper renderer would find columns of '|' and draw a single long line.
    # For now, individual segments work visually if aligned.
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

class TabPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*tab[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

    def run(self, lines):
        text = "\n".join(lines)
        def replace(match):
            return render_tab_svg(match.group(1))
        return self.FENCED_BLOCK_RE.sub(replace, text).split('\n')

class TabExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(TabPreprocessor(md), 'tab_block', 32)

def makeExtension(**kwargs):
    return TabExtension(**kwargs)
