import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class ChordProPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*chordpro[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

    def run(self, lines):
        text = "\n".join(lines)
        def replace(match):
            return self.render_chordpro(match.group(1))
        return self.FENCED_BLOCK_RE.sub(replace, text).split('\n')

    def render_chordpro(self, content):
        lines = content.strip().split('\n')
        html_parts = ['<div class="chordpro-song">']
        
        # Metadata storage
        metadata = {}
        in_chorus = False
        in_verse = False
        in_bridge = False
        in_tab = False
        in_grid = False
        in_comment_box = False
        
        for line in lines:
            line = line.rstrip()
            
            # Skip empty lines
            if not line.strip():
                html_parts.append('<div class="blank-line"></div>')
                continue
            
            # Directives {directive} or {directive: value}
            directive_match = re.match(r'^\{([^:}]+)(?::\s*(.+))?\}$', line.strip())
            if directive_match:
                directive = directive_match.group(1).strip().lower()
                value = directive_match.group(2).strip() if directive_match.group(2) else None
                
                # Metadata directives
                if directive in ['title', 't']:
                    metadata['title'] = value
                    html_parts.append(f'<h1 class="song-title">{self.escape_html(value)}</h1>')
                elif directive in ['subtitle', 'st']:
                    html_parts.append(f'<h2 class="song-subtitle">{self.escape_html(value)}</h2>')
                elif directive in ['artist']:
                    metadata['artist'] = value
                    html_parts.append(f'<div class="song-artist">Artist: {self.escape_html(value)}</div>')
                elif directive in ['composer']:
                    metadata['composer'] = value
                    html_parts.append(f'<div class="song-composer">Composer: {self.escape_html(value)}</div>')
                elif directive in ['lyricist']:
                    metadata['lyricist'] = value
                    html_parts.append(f'<div class="song-lyricist">Lyricist: {self.escape_html(value)}</div>')
                elif directive in ['album']:
                    metadata['album'] = value
                    html_parts.append(f'<div class="song-album">Album: {self.escape_html(value)}</div>')
                elif directive in ['year']:
                    metadata['year'] = value
                    html_parts.append(f'<div class="song-year">Year: {self.escape_html(value)}</div>')
                elif directive in ['key']:
                    metadata['key'] = value
                    html_parts.append(f'<div class="song-key">Key: {self.escape_html(value)}</div>')
                elif directive in ['time']:
                    metadata['time'] = value
                    html_parts.append(f'<div class="song-time">Time: {self.escape_html(value)}</div>')
                elif directive in ['tempo']:
                    metadata['tempo'] = value
                    html_parts.append(f'<div class="song-tempo">Tempo: {self.escape_html(value)}</div>')
                elif directive in ['capo']:
                    metadata['capo'] = value
                    html_parts.append(f'<div class="song-capo">Capo: {self.escape_html(value)}</div>')
                
                # Formatting directives
                elif directive in ['comment', 'c']:
                    html_parts.append(f'<div class="comment">{self.escape_html(value)}</div>')
                elif directive in ['comment_italic', 'ci']:
                    html_parts.append(f'<div class="comment italic">{self.escape_html(value)}</div>')
                elif directive in ['comment_box', 'cb']:
                    html_parts.append(f'<div class="comment-box">{self.escape_html(value)}</div>')
                elif directive in ['highlight']:
                    html_parts.append(f'<div class="highlight">{self.escape_html(value)}</div>')
                
                # Environment directives - Start
                elif directive in ['start_of_chorus', 'soc']:
                    in_chorus = True
                    label = value if value else 'Chorus'
                    html_parts.append(f'<div class="chorus"><div class="section-label">{self.escape_html(label)}</div>')
                elif directive in ['start_of_verse', 'sov']:
                    in_verse = True
                    label = value if value else 'Verse'
                    html_parts.append(f'<div class="verse"><div class="section-label">{self.escape_html(label)}</div>')
                elif directive in ['start_of_bridge', 'sob']:
                    in_bridge = True
                    label = value if value else 'Bridge'
                    html_parts.append(f'<div class="bridge"><div class="section-label">{self.escape_html(label)}</div>')
                elif directive in ['start_of_tab', 'sot']:
                    in_tab = True
                    html_parts.append('<div class="tab-section"><pre class="tab-content">')
                elif directive in ['start_of_grid', 'sog']:
                    in_grid = True
                    html_parts.append('<div class="chord-grid">')
                
                # Environment directives - End
                elif directive in ['end_of_chorus', 'eoc']:
                    in_chorus = False
                    html_parts.append('</div>')
                elif directive in ['end_of_verse', 'eov']:
                    in_verse = False
                    html_parts.append('</div>')
                elif directive in ['end_of_bridge', 'eob']:
                    in_bridge = False
                    html_parts.append('</div>')
                elif directive in ['end_of_tab', 'eot']:
                    in_tab = False
                    html_parts.append('</pre></div>')
                elif directive in ['end_of_grid', 'eog']:
                    in_grid = False
                    html_parts.append('</div>')
                
                # Column break
                elif directive in ['column_break', 'colb']:
                    html_parts.append('<div class="column-break"></div>')
                
                # New page
                elif directive in ['new_page', 'np']:
                    html_parts.append('<div class="page-break">• • •</div>')
                
                # New song
                elif directive in ['new_song', 'ns']:
                    html_parts.append('</div><div class="chordpro-song">')
                
                continue
            
            # Handle content based on current environment
            if in_tab:
                # Tab content - preserve as-is
                html_parts.append(self.escape_html(line))
            elif in_grid:
                # Chord grid - parse as chord symbols
                html_parts.append(f'<div class="grid-line">{self.parse_grid_line(line)}</div>')
            else:
                # Regular line with possible inline chords [C]text
                html_parts.append(f'<div class="lyrics-line">{self.parse_inline_chords(line)}</div>')
        
        # Close any open environments
        if in_chorus or in_verse or in_bridge:
            html_parts.append('</div>')
        if in_tab:
            html_parts.append('</pre></div>')
        if in_grid:
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        return "\n".join(html_parts)
    
    def parse_inline_chords(self, line):
        """Parse inline chords [Am]text and convert to HTML"""
        result = []
        last_pos = 0
        
        for match in re.finditer(r'\[([^\]]+)\]', line):
            # Add text before chord
            if match.start() > last_pos:
                result.append(self.escape_html(line[last_pos:match.start()]))
            
            # Add chord
            chord = match.group(1)
            result.append(f'<span class="chord">{self.escape_html(chord)}</span>')
            last_pos = match.end()
        
        # Add remaining text
        if last_pos < len(line):
            result.append(self.escape_html(line[last_pos:]))
        
        return ''.join(result)
    
    def parse_grid_line(self, line):
        """Parse chord grid line (chords separated by spaces/bars)"""
        # Split by | or whitespace, filter empty
        chords = [c.strip() for c in re.split(r'[\|\s]+', line) if c.strip()]
        return ' '.join(f'<span class="grid-chord">{self.escape_html(c)}</span>' for c in chords)
    
    def escape_html(self, text):
        if not text:
            return ''
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class ChordProExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(ChordProPreprocessor(md), 'chordpro_block', 30)

def makeExtension(**kwargs):
    return ChordProExtension(**kwargs)
