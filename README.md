# ChordsMD

A powerful and versatile Python Markdown extension for musical notation, screenplays, and more. 

Convert plain text into professional-grade chord sheets, tablature (SVG), ABC music scores, ChordPro lead sheets, Fountain screenplays, and guitar strumming patterns.

## Features

- **Chord Sheets**: Automatic merging of chords over lyrics with structured HTML rendering.
- **Tablature**: Dynamic SVG rendering of ASCII tabs with stroke notation support.
- **ABC Notation**: Standard music score rendering using `abcjs`.
- **ChordPro**: Full implementation of the ChordPro lead sheet specification.
- **Fountain**: Complete support for the Fountain screenplay format.
- **Strumming Patterns**: Visual representation of guitar strumming with strong/weak beat distinction.
- **Chord Diagrams**: Interactive guitar chord fingerings using `svguitar.js`.
- **Text Formatting**: AsciiDoc-like styles for superscript, subscript, monospace, and highlights.
- **Admonitions**: Styled boxes for NOTE, TIP, IMPORTANT, etc.

## Usage

### Installation

```bash
pip install chordsmd
```

### Basic Setup

```python
import markdown
from chordsmd import ChordsMDExtension

text = """
# My Song

```chords
[Verse 1]
G               D
The sun is shining bright
Em              C
Everything feels right
```
"""

html = markdown.markdown(text, extensions=[ChordsMDExtension()])
```

## Supported Formats

### 1. Chord Sheets (```chords)
Automatically aligns chords above lyrics.
- Supports section headers like `[Chorus]`.
- Interactive transposition and column layout controls.
- Detects and renders embedded tabs.

### 2. Tablature (```tab)
Converts ASCII tabs to clean SVG graphics.
- Supports standard guitar and bass notation.
- Advanced stroke notation: `V`, `v`, `A`, `^`, `↓`, `↑`.
- Inline techniques: hammer-ons (`h`), pull-offs (`p`), slides (`/`), etc.

### 3. ChordPro (```chordpro)
Full support for `{title}`, `{subtitle}`, `{start_of_chorus}`, and more.
- Inline chords: `[Am]Lyric text`.
- Metadata, formatting, and environment directives.

### 4. Fountain Screenplay (```fountain)
Write screenplays in plain text.
- Automatic detection of Scenes, Characters, Dialogue, and Actions.
- Forced elements (`.HEADING`, `@CHARACTER`, `>TRANSITION`).
- Dual dialogue, lyrics, and title pages.

### 5. Strumming Patterns (```strum)
Visual color-coded strumming guides.
- Strong/Weak beat distinction.
- Symbols: `V`, `v`, `A`, `^`, `X`, `-`, `.`, `|`.

### 6. Chord Diagrams (```chord diagrams)
Renders fingering charts using `svguitar.js`.
- Custom notation: `Name = positions | barres`.
- Example: `C = X 3 2 o 1 O`.

### 7. Text Formatting & Admonitions
AsciiDoc-like shorthands for advanced text styles.
- **Superscript**: `^super^` -> <sup>super</sup>
- **Subscript**: `~sub~` -> <sub>sub</sub>
- **Monospace**: `+code+` -> `code`
- **Highlight**: `#mark#` -> <mark>mark</mark>
- **Admonitions**: `NOTE:`, `TIP:`, `WARNING:`, etc. at line start.

## Configuration

Enable or disable specific features:

```python
md = markdown.Markdown(extensions=[
    ChordsMDExtension(
        chords=True,      # Chord sheets
        tabs=True,        # Tablature
        abc=True,         # ABC notation
        chordpro=True,    # ChordPro format
        fountain=True,    # Fountain screenplays
        strumming=True,   # Strumming patterns
        diagrams=True     # Chord diagrams
    )
])
```

## Documentation

Detailed specifications for each format can be found in the `docs/` directory:

- [Chord Sheets](docs/chords.md)
- [Tablature](docs/tabs.md)
- [ChordPro](docs/chordpro.md)
- [Fountain](docs/fountain.md)
- [Strumming Patterns](docs/strumming.md)
- [Chord Diagrams](docs/diagrams.md)

## Development & Testing

Run the full test suite (62+ tests):
```bash
pytest tests/
```

Generate a visual demonstration:
```bash
python demo.py
```

---
*Last Updated: 2026-01-22*
