# ABC Notation Spec

**Extension:** `AbcExtension`  
**Syntax:** ` ```abc `  
**Config Option:** `abc` (enabled by default)

## Overview

ABC notation is a shorthand form of musical notation for computers. ChordsMD uses [abcjs](https://abcjs.net/) to render ABC notation into high-quality musical scores and provides interactive MIDI playback.

## Basic Structure

An ABC block typically starts with headers followed by the music notation:

```abc
X: 1
T: Title
M: 4/4
L: 1/4
K: C
C D E F | G A B c |
```

### Common Headers

| Header | Meaning | Example |
|--------|---------|---------|
| `X:` | Reference number (required) | `X: 1` |
| `T:` | Title | `T: Simple Scale` |
| `M:` | Meter / Time Signature | `M: 4/4` |
| `L:` | Default Note Length | `L: 1/8` |
| `K:` | Key Signature | `K: G` |
| `Q:` | Tempo | `Q: 1/4=120` |

## Guitar-Specific Usage

### Scales

```abc
X: 1
T: G Major Scale
M: 4/4
L: 1/8
K: G
G, A, B, C | D E F G | A B c d | e f g a | b c' d' e' | f' g' a' b' |
```

### Melodies

```abc
X: 1
T: Ode to Joy
M: 4/4
L: 1/4
K: C
E E F G | G F E D | C C D E | E>D D2 |
```

## Advanced Features

### Chords

Add chords above the staff using double quotes:

```abc
X: 1
M: 4/4
K: C
"C"E E F G | "G"G F E D | "C"C C D E | "G"D D "C"C2 |
```

### Multiple Voices

```abc
X: 1
T: Two Voices
M: 4/4
K: C
V: 1
c d e f | g a b c' |
V: 2
C, D, E, F, | G, A, B, C |
```

## Interactive Player

The ABC blocks in ChordsMD automatically include a MIDI player interface that allows you to:
- Play the notation
- Adjust tempo (using `Q:` header or player UI)
- Listen to specific sections

## Requirements

- **abcjs** library must be loaded
- Library location: `assets/vendor/abcjs-basic-min.js`
- The MkDocs plugin handles this automatically for documentation sites.

## Styling

The rendered score follows the default styling of `abcjs`. In ChordsMD, it is centered within the content area and responsive to container width.
