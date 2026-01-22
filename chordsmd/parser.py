import re

# Regex breakdown:
# Group 1 (Root): [A-G] followed by optional # or b
# Group 2 (Quality): Any characters until the end or a slash
# Group 3 (Bass): Optional slash followed by a Root
CHORD_PATTERN = re.compile(r'^([A-G][#b]?)(.*?)(\/[A-G][#b]?)?$')

def parse_chord(text):
    """
    Parses a string to check if it's a valid musical chord.
    
    Args:
        text (str): The text to parse.
        
    Returns:
        dict: A dictionary with 'root', 'quality', and 'bass' if valid.
        None: If the text is not a valid chord.
    """
    # Simple heuristic to avoid false positives on common words
    # If it's too long or contains spaces, it's likely not a chord symbol
    if len(text) > 10 or ' ' in text:
        return None

    match = CHORD_PATTERN.match(text)
    if match:
        root, quality, bass_part = match.groups()
        
        # bass_part includes the slash, e.g. "/E"
        bass = bass_part[1:] if bass_part else None
        
        return {
            'root': root,
            'quality': quality,
            'bass': bass
        }
    return None
