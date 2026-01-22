from chordsmd.blocks import ChordsBlockPreprocessor
from chordsmd.merger import merge_chords_and_lyrics
from chordsmd.parser import parse_chord

# Mock Preprocessor to run process_chords_content
class MockMD:
    pass

prep = ChordsBlockPreprocessor(MockMD())

print("--- Test Merger Basic ---")
chord_line = "Am      G"
lyric_line = "I am a boy"
merged = merge_chords_and_lyrics(chord_line, lyric_line)
print(f"Chord: '{chord_line}'")
print(f"Lyric: '{lyric_line}'")
print(f"Merged: '{merged}'")
expected = '<span class="chord">Am</span>I am a b<span class="chord">G</span>oy'
print(f"Match expected? {expected in merged}")

print("\n--- Test Merger Padding ---")
chord_line = "        C"
lyric_line = "He"
merged = merge_chords_and_lyrics(chord_line, lyric_line)
print(f"Chord: '{chord_line}'")
print(f"Lyric: '{lyric_line}'")
print(f"Merged: '{merged}'")
expected = 'He      <span class="chord">C</span>'
print(f"Match expected? {merged == expected}")
print(f"Expected: '{expected}'")

print("\n--- Test Processor ---")
text = """
Am      G
I am a boy
"""
html = prep.process_chords_content(text)
print(f"HTML Output:\n{html}")
