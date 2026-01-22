import re
import json
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class ChordDiagramPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*chord(?:s)?[ ]*diagram(?:s)?[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

    def __init__(self, md):
        super().__init__(md)
        self.diagram_counter = 0

    def run(self, lines):
        text = "\n".join(lines)
        def replace(match):
            return self.render_diagrams(match.group(1))
        return self.FENCED_BLOCK_RE.sub(replace, text).split('\n')

    def render_diagrams(self, content):
        lines = content.strip().split('\n')
        html_parts = ['<div class="chord-diagrams">']
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse notation: "ChordName = positions |barres"
            if '=' not in line:
                continue
            
            chord_name, definition = line.split('=', 1)
            chord_name = chord_name.strip()
            definition = definition.strip()
            
            # Save raw definition for display
            raw_definition = definition
            
            # Split barres if present
            barres = []
            if '|' in definition:
                positions_part, barres_part = definition.split('|', 1)
                # Parse barres: "2.1" means fret 2, finger 1
                for barre in barres_part.strip().split():
                    if '.' in barre:
                        fret, finger = barre.split('.')
                        barres.append({
                            'fret': int(fret),
                            'fromString': 6,  # 6th string
                            'toString': 1,    # 1st string
                            'finger': int(finger) if finger.isdigit() else None
                        })
            else:
                positions_part = definition
            
            # Parse positions: "2 0 4.1 4.2 4.3 0"
            # Format: fret or fret.finger or x/-
            # User input is usually: 6th string (low E) to 1st string (high E)
            # svguitar expects: [string_number, fret, finger]
            # where string 6 is left (lowest) and 1 is right (highest)
            # So we map index 0 -> string 6, index 1 -> string 5, etc.
            positions_str = positions_part.strip().split()
            positions = []
            
            for i, pos in enumerate(positions_str):
                string_num = 6 - i # Map 0->6, 1->5, 2->4, 3->3, 4->2, 5->1
                if string_num < 1: continue # Support max 6 strings
                
                pos = pos.strip()
                if pos.lower() in ['x', '-']:
                    # Muted string
                    positions.append([string_num, 'x'])
                elif pos.lower() in ['0', 'o']:
                    # Open string
                    positions.append([string_num, 0])
                elif '.' in pos:
                    # fret.finger
                    fret, finger = pos.split('.')
                    positions.append([string_num, int(fret), int(finger) if finger.isdigit() else None])
                else:
                    # Just fret number
                    positions.append([string_num, int(pos)])
            
            # Generate unique ID for this diagram
            self.diagram_counter += 1
            container_id = f'chord-diagram-{self.diagram_counter}'
            
            # Create chord configuration
            chord_config = {
                'fingers': positions,
                'barres': barres if barres else []
            }
            
            html_parts.append(f'<div class="chord-diagram-container">')
            html_parts.append(f'<div class="chord-name">{self.escape_html(chord_name)} <span class="chord-notation">({self.escape_html(raw_definition)})</span></div>')
            html_parts.append(f'<div id="{container_id}" class="chord-diagram-svg" style="max-height: 200px; max-width: 150px;"></div>')
            html_parts.append(f'<script>')
            html_parts.append(f'(function() {{')
            html_parts.append(f'  const init = function() {{')
            html_parts.append(f'    if (typeof svguitar === "undefined") {{')
            html_parts.append(f'      console.error("svguitar library not loaded");')
            html_parts.append(f'      return;')
            html_parts.append(f'    }}')
            html_parts.append(f'    const chart = new svguitar.SVGuitarChord("#{container_id}");')
            html_parts.append(f'    chart.configure({{')
            html_parts.append(f'      strings: 6,')
            html_parts.append(f'      frets: 5,')
            html_parts.append(f'      position: 1,')
            html_parts.append(f'      backgroundColor: "white",')
            html_parts.append(f'      strokeColor: "#333",')
            html_parts.append(f'      textColor: "#333",')
            html_parts.append(f'      stringColor: "#333",')
            html_parts.append(f'      fretColor: "#333"')
            html_parts.append(f'    }});')
            html_parts.append(f'    chart.chord({json.dumps(chord_config)}).draw();')
            html_parts.append(f'  }};')
            html_parts.append(f'  if (document.readyState === "loading") {{')
            html_parts.append(f'    document.addEventListener("DOMContentLoaded", init);')
            html_parts.append(f'  }} else {{')
            html_parts.append(f'    init();')
            html_parts.append(f'  }}')
            html_parts.append(f'}})();')
            html_parts.append(f'</script>')
            html_parts.append(f'</div>')
        
        html_parts.append('</div>')
        return "\n".join(html_parts)
    
    def escape_html(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class ChordDiagramExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(ChordDiagramPreprocessor(md), 'chord_diagram_block', 28)

def makeExtension(**kwargs):
    return ChordDiagramExtension(**kwargs)
