# Strumming Patterns Format

**Extension:** `StrummingExtension`  
**Syntax:** ` ```strum ` or ` ```strumming `  
**Config Option:** `strumming` (enabled by default)

## Overview

Visual representation of guitar strumming patterns with strong/weak beat distinction, color-coded strokes, and rhythm markers.

## Notation Reference

### Downstrokes

| Symbol | Type | Visual | Color | Size |
|--------|------|--------|-------|------|
| `V`, `D`, `↓` | Strong | ↓ | Blue | 28px, bold |
| `v`, `d` | Weak | ↓ | Blue | 20px, normal |

### Upstrokes

| Symbol | Type | Visual | Color | Size |
|--------|------|--------|-------|------|
| `A`, `^`, `U`, `↑` | Strong | ↑ | Red | 28px, bold |
| `a`, `u` | Weak | ↑ | Red | 20px, normal |

### Other Symbols

| Symbol | Meaning | Visual |
|--------|---------|--------|
| `X`, `x` | Muted strum | ✕ (gray) |
| `-`, `.` | Rest/pause | - (light gray) |
| `|` | Bar line | \| (dark gray) |
| `1`, `2`, `3`, `4` | Beat numbers | Superscript |
| `(`, `)` | Grouping | Markers |

## Strong vs. Weak Beats

**Strong beats** (uppercase letters):
- Emphasized with bold weight
- Larger size (28px)
- Scaled up (1.1x)
- Represent primary beats (1 and 3 in 4/4 time)

**Weak beats** (lowercase letters):
- Normal weight
- Smaller size (20px)
- 70% opacity
- Represent secondary beats (2 and 4 in 4/4 time)

## Pattern Syntax

### Basic Pattern

```strum
D DU UDU
```

Result: Down, Down-Up, Up-Down-Up

### Labeled Patterns

```strum
Verse: D du V au
Chorus: V V Au au
Bridge: D . du . V . au .
```

Labels appear as section headers above patterns.

### With Bar Lines

```strum
D du | V au | D du | V au
```

Bar lines visually separate measures.

### With Beat Numbers

```strum
1 D 2 du 3 V 4 au
```

Beat numbers appear as superscript above the pattern.

### With Grouping

```strum
(D du) (V au) (D du) (V au)
```

Parentheses group related strokes.

### With Rests

```strum
D - du - V - au -
D . du . V . au .
```

Both `-` and `.` represent rests/pauses.

### With Muted Strums

```strum
D X du X V X au X
```

`X` represents muted/percussive strums.

## Complete Examples

### Folk Strum

```strum
Verse: D du V du
Chorus: D du V au
```

### Reggae Strum

```strum
Pattern: - au - au - au - au
```

### Rock Strum

```strum
Verse: D - du V du
Chorus: D du V du D du V du
```

### Complex Pattern with All Features

```strum
Intro: 1 D 2 . 3 V 4 .

Verse: D du V au | D du V au | D X V X | D du V au

Chorus: (D D) (V V) | (Au au) (Au au)

Bridge: D . du . | V . au . | X X X X | D - - -
```

## Visual Output

Patterns are rendered with:
- **Color-coded strokes**: Blue (down), Red (up), Gray (muted)
- **Size variation**: Strong beats larger than weak beats
- **Tooltips**: Hover over strokes for descriptions
- **Responsive layout**: Flexbox with proper spacing
- **Clean typography**: Sans-serif font, clear symbols

## CSS Classes

- `.strumming-pattern` - Main container
- `.pattern-section` - Section with label
- `.pattern-label` - Section label text
- `.strum-sequence` - Stroke sequence container
- `.stroke-group` - Group of strokes
- `.stroke` - Individual stroke
- `.stroke.down` - Downstroke
- `.stroke.up` - Upstroke
- `.stroke.strong` - Strong beat
- `.stroke.weak` - Weak beat
- `.stroke.muted` - Muted strum
- `.stroke.rest` - Rest/pause
- `.bar-line` - Bar line separator
- `.beat-number` - Beat number
- `.group-marker` - Grouping parenthesis

## Usage Tips

1. **Use uppercase for strong beats**: `D`, `V`, `A`, `U` for beats 1 and 3
2. **Use lowercase for weak beats**: `d`, `v`, `a`, `u` for beats 2 and 4
3. **Add bar lines for clarity**: Separate measures with `|`
4. **Label sections**: Use `Section: pattern` format
5. **Include beat numbers**: Help learners count: `1 D 2 du 3 V 4 au`
6. **Group related strokes**: Use `()` for visual grouping
7. **Mark rests clearly**: Use `-` or `.` for silent beats

## Common Patterns

### Basic Downstrokes

```strum
D D D D
```

### Down-Up Pattern

```strum
D du D du
```

### Folk/Country

```strum
D du V du
```

### Reggae

```strum
- au - au
```

### Rock/Pop

```strum
D du V du D du V du
```

### Calypso

```strum
D - du V - au
```

### Waltz (3/4)

```strum
D du du
```
