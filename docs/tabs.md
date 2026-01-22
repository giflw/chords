# Tablature Format

**Extension:** `TabExtension`  
**Syntax:** ` ```tab `  
**Config Option:** `tabs` (enabled by default)

## Overview

ASCII tablature notation for guitar, bass, and other stringed instruments, rendered as SVG for clean, scalable display.

## Format Specification

### Standard Guitar Tablature

Six strings from high E (top) to low E (bottom):

```tab
e|---0---2---3---|
B|---1---3---0---|
G|---0---2---0---|
D|---2---0---0---|
A|---3-------2---|
E|-----------3---|
```

### Bass Tablature

Four strings:

```tab
G|----------------|
D|---5---7---5----|
A|----------------|
E|---5-------5----|
```

### String Labels

Supported string labels:
- **Guitar**: `e`, `B`, `G`, `D`, `A`, `E`
- **Bass**: `G`, `D`, `A`, `E`
- **7-string**: `e`, `B`, `G`, `D`, `A`, `E`, `B` (low)
- **Custom**: Any single character followed by `|`

### Fret Numbers

- **Single digit**: `0-9`
- **Double digit**: `10`, `12`, `15`, etc.
- **Hammer-on/Pull-off**: `5h7`, `7p5`
- **Slide**: `5/7`, `7\5`
- **Bend**: `7b9`
- **Vibrato**: `7~`

### Special Symbols

- `-` - No note played
- `|` - Bar line
- `x` - Muted/dead note
- `h` - Hammer-on
- `p` - Pull-off
- `/` - Slide up
- `\` - Slide down
- `b` - Bend
- `~` - Vibrato

### Strumming Arrows

```tab
e|---0---2---3---|
B|---1---3---0---|
G|---0---2---0---|
D|---2---0---0---|
A|---3-------2---|
E|-----------3---|
  ↓   ↓ ↑ ↓   ↓ ↑
```

- `↓` - Downstroke
- `↑` - Upstroke

## Rendering

Tablature is rendered as SVG with:
- **Monospace font** for alignment
- **String lines** in gray
- **Fret numbers** in black
- **Arrows** in blue (down) and red (up)
- **Automatic sizing** based on content

### SVG Features

- Clean, scalable graphics
- Proper character spacing
- Aligned string lines
- Color-coded elements

## Examples

### Simple Riff

```tab
e|----------------|
B|----------------|
G|----------------|
D|---5---7---5----|
A|---5---7---5----|
E|---3---5---3----|
```

### With Techniques

```tab
e|---12h14p12-----|
B|-------------15-|
G|----------------|
D|---0h2p0--------|
A|----------------|
E|----------------|
```

### With Strumming Pattern

```tab
e|---0---0---0---0---|
B|---1---1---1---1---|
G|---0---0---0---0---|
D|---2---2---2---2---|
A|---3---3---3---3---|
E|-------------------|
  ↓   ↓ ↑ ↑ ↓ ↑
```

### Bass Line

```tab
G|----------------|
D|---5---5---7----|
A|----------------|
E|---5-------5----|
```

## CSS Classes

- `.tab-svg` - SVG container
- `.tab-block` - Tab block wrapper

## Technical Details

### Detection Algorithm

A block is identified as tablature if:
1. Contains `|` characters
2. Has string labels (e.g., `e|`, `B|`)
3. High ratio of dashes and pipes (>60%)
4. Contains arrow symbols (`↓`, `↑`)

### Rendering Process

1. Parse each line to extract string label and content
2. Identify anchor column (most common non-dash character position)
3. Calculate SVG dimensions based on content
4. Render string lines, fret numbers, and symbols
5. Add strumming arrows if present

### SVG Output

```svg
<svg class="tab-svg" width="..." height="...">
  <text class="tab-string-label">e</text>
  <line class="tab-string-line" .../>
  <text class="tab-fret">0</text>
  <text class="tab-arrow down">↓</text>
</svg>
```
