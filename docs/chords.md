# Chord Sheets Format

**Extension:** `ChordSheetExtension`  
**Syntax:** ` ```chords `  
**Config Option:** `chords` (enabled by default)

## Overview

Chord sheets display chords positioned above lyrics, similar to traditional sheet music chord charts. The extension automatically detects chord lines and merges them with lyrics.

## Format Specification

### Basic Structure

```chords
[Section Name]
Chord_Line
Lyric_Line

Chord_Line
Lyric_Line
```

### Section Headers

Section headers are enclosed in square brackets:

```chords
[Verse 1]
[Chorus]
[Bridge]
[Intro]
[Outro]
```

### Chord Lines

A line is detected as a chord line if it contains primarily chord-like patterns:
- Contains uppercase letters (chord roots)
- Has spacing patterns typical of chords
- Contains common chord symbols: `m`, `maj`, `min`, `dim`, `aug`, `sus`, `7`, `9`, etc.

**Examples of valid chords:**
- `Am`, `G`, `C`, `D`
- `Am7`, `G7`, `Cmaj7`, `Dm9`
- `C/G`, `Am/E` (slash chords)
- `Fsus4`, `Bdim`, `Eaug`

### Chord Positioning

Chords are positioned above the lyrics based on their column position in the chord line:

```chords
Am      G       C       D
I am a boy with a toy
```

Result: `Am` appears above "I", `G` above "boy", `C` above "with", `D` above "toy"

### Inline Chord Syntax

You can also use `!!ChordName!!` for inline chord highlighting:

```markdown
Here are some chords: !!Am7!!, !!C/G!!, !!F#dim!!
```

### Tablature Integration

Tablature blocks can be embedded within chord sheets:

```chords
[Intro]
e|---0---2---3---|
B|---1---3---0---|
G|---0---2---0---|
D|---2---0---0---|
A|---3-------2---|
E|-----------3---|

[Verse]
G               D
The verse starts here
```

The extension automatically detects tab blocks by looking for:
- Lines with `|` characters
- Patterns like `e|`, `B|`, `G|`, `D|`, `A|`, `E|`
- High ratio of dashes and pipes
- Arrow symbols (`↓`, `↑`) for strumming patterns

## Features

### Transposition Controls

Each chord sheet includes interactive transposition controls:
- **+/-** buttons to transpose up/down by semitones
- **Key display** showing current transposition (e.g., "+2", "-1", "Original")
- Chords update in real-time

### Column Layout

Switch between 1, 2, or 3 column layouts:
- **1 column**: Standard single-column display
- **2 columns**: Content flows into 2 columns
- **3 columns**: Content flows into 3 columns

### Structured HTML Output

Chords are rendered with semantic HTML:

```html
<span class="chord">
  <span class="root">A</span>
  <span class="quality">m</span>
  <span class="bass">E</span>
</span>
```

This allows for precise CSS styling and JavaScript manipulation.

## Examples

### Simple Song

```chords
[Verse 1]
Am      G
I am a boy
C       D
I have a toy

[Chorus]
F         C
This is a song
      G
About chords
```

### With Section Labels

```chords
[Intro]
G  D  Em  C

[Verse 1]
G               D
The sun is shining bright
Em              C
Everything feels right

[Chorus]
G       D       Em      C
La la la la la la la
```

### With Tablature

```chords
[Intro - Fingerpicking]
e|---0-------0-------0-------0---|
B|-----1-------1-------1-------1-|
G|-------0-------0-------0-------0|
D|-2-------2-------2-------2-----|
A|-------------------------------|
E|-------------------------------|

[Verse]
Am              G
Gentle melody flows
```

## CSS Classes

- `.chords-sheet-container` - Main container
- `.chords-controls` - Transposition and layout controls
- `.chords-sheet` - Content area
- `.chord` - Individual chord
- `.chord .root` - Chord root note
- `.chord .quality` - Chord quality (m, maj, 7, etc.)
- `.chord .bass` - Bass note for slash chords
- `.sheet-section` - Section container
- `.tab-block` - Tablature block
- `.tab-svg` - SVG tablature rendering

## JavaScript Features

- **ChordTransposer** - Handles key transposition
- **ColumnLayoutManager** - Manages column layout switching

Both classes auto-initialize on page load for elements with class `.chords-sheet-container`.
