# Chord Diagrams Format

**Extension:** `ChordDiagramExtension`  
**Syntax:** ` ```chord diagrams `  
**Config Option:** `diagrams` (enabled by default)

## Overview

Interactive chord diagrams using [svguitar.js](https://github.com/omnibrain/svguitar) library. Displays guitar chord fingerings with fret positions, finger numbers, and barres.

## Notation Format

```
ChordName = positions |barres
```

### Components

1. **Chord Name**: Any text (e.g., `C`, `Am7`, `Gmaj7`)
2. **Equals sign**: Separator
3. **Positions**: Space-separated string positions (6th to 1st string)
4. **Pipe symbol** `|`: Optional barre separator
5. **Barres**: Space-separated barre definitions

## Position Notation

Positions are listed from **6th string (low E)** to **1st string (high E)**.

### Format Options

| Format | Meaning | Example |
|--------|---------|---------|
| `fret` | Fret number only | `3` |
| `fret.finger` | Fret and finger number | `3.2` |
| `0`, `o`, `O` | Open string | `0`, `o` |
| `x`, `X` or `-` | Muted string | `x`, `X` |

### Finger Numbers

- `1` = Index finger
- `2` = Middle finger
- `3` = Ring finger
- `4` = Pinky finger

## Barre Notation

After the `|` symbol, define barres as `fret.finger`:

```
|2.1
```

This creates a barre at fret 2 using finger 1 (index).

## Examples

### Simple Chords (No Fingers)

```chord diagrams
C = x 3 2 0 1 0
G = 3 2 0 0 0 3
D = x x 0 2 3 2
A = x 0 2 2 2 0
E = 0 2 2 1 0 0
```

### With Finger Numbers

```chord diagrams
C = x 3.3 2.2 0 1.1 0
G = 3.2 2.1 0 0 0 3.3
Am = x 0 2.2 2.3 1.1 0
Em = 0 2.2 2.3 0 0 0
```

### With Barres

```chord diagrams
F = 1.1 3.3 3.4 2.2 1.1 1.1 |1.1
Bm = x 2.1 4.3 4.4 3.2 2.1 |2.1
B = 2 0 4.1 4.2 4.3 0 |2.1
```

### Complex Chords

```chord diagrams
Cmaj7 = x 3.3 2.2 0 0 0
Am7 = x 0 2.2 0 1.1 0
Dm9 = x x 0 2.1 1.0 0
G7 = 3.3 2.2 0 0 0 1.1
```

## String Order Reference

```
Position: 1   2   3   4   5   6
String:   E   A   D   G   B   e
          6th 5th 4th 3rd 2nd 1st
          Low             High
```

## Detailed Example

### B Major Chord

```chord diagrams
B = 2 0 4.1 4.2 4.3 0 |2.1
```

**Breakdown:**
- **String 6 (low E)**: Fret 2
- **String 5 (A)**: Open (0)
- **String 4 (D)**: Fret 4, finger 1
- **String 3 (G)**: Fret 4, finger 2
- **String 2 (B)**: Fret 4, finger 3
- **String 1 (high E)**: Open (0)
- **Barre**: Fret 2, finger 1 (across strings 6-1)

### F Major Chord

```chord diagrams
F = 1.1 3.3 3.4 2.2 1.1 1.1 |1.1
```

**Breakdown:**
- All strings at fret 1 with finger 1 (barre)
- Additional fingers at frets 2, 3, 3
- Full barre across all 6 strings

## Multiple Diagrams

Display multiple chords in one block:

```chord diagrams
C = x 3 2 0 1 0
Am = x 0 2 2 1 0
F = 1 3 3 2 1 1 |1.1
G = 3 2 0 0 0 3
```

Diagrams are displayed in a flex layout with proper spacing.

## SVG Output

Each diagram is rendered as an SVG with:
- **6 strings** (horizontal lines)
- **5 frets** (vertical lines)
- **Fret markers** (dots)
- **Finger numbers** (inside dots)
- **Muted strings** (X above nut)
- **Open strings** (O above nut)
- **Barres** (curved lines)

### Styling

- Background: White
- Strings/frets: Dark gray (#333)
- Dots: Black with white numbers
- Muted: Red X
- Open: Green O

## CSS Classes

- `.chord-diagrams` - Main container (flex layout)
- `.chord-diagram-container` - Individual diagram container
- `.chord-name` - Chord name label
- `.chord-diagram-svg` - SVG container

## JavaScript Integration

Diagrams are generated using svguitar.js:

```javascript
const chart = new svguitar.SVGuitarChord("#chord-diagram-1");
chart.configure({
  strings: 6,
  frets: 5,
  position: 1,
  style: { /* styling options */ }
});
chart.chord({ chord: positions, barres: barres }).draw();
```

## Common Chord Library

### Open Chords

```chord diagrams
C = x 3 2 0 1 0
D = x x 0 2 3 2
E = 0 2 2 1 0 0
G = 3 2 0 0 0 3
A = x 0 2 2 2 0
```

### Minor Chords

```chord diagrams
Am = x 0 2 2 1 0
Dm = x x 0 2 3 1
Em = 0 2 2 0 0 0
```

### Seventh Chords

```chord diagrams
C7 = x 3 2 3 1 0
D7 = x x 0 2 1 2
E7 = 0 2 0 1 0 0
G7 = 3 2 0 0 0 1
A7 = x 0 2 0 2 0
```

### Barre Chords

```chord diagrams
F = 1 3 3 2 1 1 |1.1
Bm = x 2 4 4 3 2 |2.1
Cm = x 3 5 5 4 3 |3.1
```

## Tips

1. **Muted strings**: Use `x`, `X` or `-` for strings not played
2. **Open strings**: Use `0`, `o` or `O` for open strings
3. **Finger numbers**: Add `.1`, `.2`, `.3`, `.4` after fret for fingering
4. **Barres**: Always specify after `|` for proper rendering
5. **Multiple diagrams**: List one per line in the same block
6. **Comments**: Use `#` at line start for comments (ignored)

## Requirements

- **svguitar.js** library must be loaded
- Library location: `assets/vendor/svguitar.umd.js`
- Auto-loaded in demo.html
