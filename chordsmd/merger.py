import re

def parse_chord_line(line):
    """
    Finds chords and their indices in a line.
    Returns a list of tuples: (index, chord_text)
    """
    chords = []
    # Find all non-whitespace sequences
    for match in re.finditer(r'\S+', line):
        # We can optionally validate if it looks like a chord here
        # For now, in a "Chord Line", everything is a chord
        chords.append((match.start(), match.group()))
    return chords

def merge_chords_and_lyrics(chord_line, lyric_line):
    """
    Merges a chord line into a lyric line by injecting spans.
    """
    if not chord_line:
        return lyric_line
    
    # If no lyrics, just return chords wrapped in spans, preserving spacing?
    # Actually, if no lyrics (instrumental), we might want to just output chords.
    # But usually instrumental lines are handled by the caller.
    if not lyric_line:
       lyric_line = ""

    chords = parse_chord_line(chord_line)
    
    # We construct the result by slicing the lyric line
    # We need to process from right to left to avoid index shifting
    # OR build a new string from left to right.
    
    # Let's build a list of segments
    # Actually, simple injection is easiest from back to front
    
    # Pad lyrics if chords go beyond
    last_chord_end = chords[-1][0] + len(chords[-1][1]) if chords else 0
    if len(lyric_line) < last_chord_end:
        lyric_line += " " * (last_chord_end - len(lyric_line))
        
    result = list(lyric_line)
    
    # Sort chords by index (should already be sorted but safe to ensure)
    # We process in reverse order to insert straightforwardly? 
    # No, effectively we want to insert at index I.
    # If we insert at index I, subsequent indices shift. 
    # So reverse order is best.
    
    for start_idx, chord_text in reversed(chords):
        # Insert span
        span = f'<span class="chord">{chord_text}</span>'
        
        # We assume start_idx is valid for the padded lyric_line
        # But wait, if we insert AT start_idx, it pushes the character at start_idx to the right.
        # This is correct: Chord "C" at index 5 over "Hello" at index 5 -> "Hello<span...>C</span>" NO.
        # Standard notation: Chord is *above* the character.
        # So it should be inserted *before* the character at that index.
        
        if start_idx >= len(result):
             # Should be covered by padding, but just in case append
             result.append(span)
        else:
            result.insert(start_idx, span)
            
    return "".join(result).rstrip()
