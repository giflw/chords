import re
from .parser import parse_chord
from xml.etree import ElementTree

def parse_chord_line(line):
    """
    Finds chords and their indices in a line.
    Returns a list of tuples: (index, chord_text)
    """
    chords = []
    # Find all non-whitespace sequences
    for match in re.finditer(r'\S+', line):
        chords.append((match.start(), match.group()))
    return chords

def render_chord_span(chord_text):
    data = parse_chord(chord_text)
    if data:
        # Build structured span
        # <span class="chord"><span class="root">...</span>...</span>
        inner = f'<span class="root">{data["root"]}</span>'
        if data['quality']:
            inner += f'<span class="quality">{data["quality"]}</span>'
        if data['bass']:
            inner += f'<span class="bass">/{data["bass"]}</span>'
        return f'<span class="chord">{inner}</span>'
    else:
        # Raw span
        return f'<span class="chord">{chord_text}</span>'

def merge_chords_and_lyrics(chord_line, lyric_line):
    """
    Merges a chord line into a lyric line by injecting spans.
    """
    if not chord_line:
        return lyric_line
    
    if not lyric_line:
       lyric_line = ""

    chords = parse_chord_line(chord_line)
    
    # Pad lyrics if chords go beyond
    last_chord_end = chords[-1][0] + len(chords[-1][1]) if chords else 0
    if len(lyric_line) < last_chord_end:
        lyric_line += " " * (last_chord_end - len(lyric_line))
        
    result = list(lyric_line)
    
    for start_idx, chord_text in reversed(chords):
        # Insert span
        span = render_chord_span(chord_text)
        
        if start_idx >= len(result):
             result.append(span)
        else:
            result.insert(start_idx, span)
            
    return "".join(result).rstrip()
