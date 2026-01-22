# ChordPro Format

**Extension:** `ChordProExtension`  
**Syntax:** ` ```chordpro `  
**Config Option:** `chordpro` (enabled by default)

## Overview

Complete implementation of the [ChordPro specification](https://www.chordpro.org/), a text-based format for lead sheets with chords and lyrics.

## Directive Reference

### Metadata Directives

Define song information and metadata.

| Directive | Short | Description | Example |
|-----------|-------|-------------|---------|
| `{title}` | `{t}` | Song title | `{title: Amazing Grace}` |
| `{subtitle}` | `{st}` | Subtitle | `{subtitle: Traditional Hymn}` |
| `{artist}` | - | Artist name | `{artist: John Newton}` |
| `{composer}` | - | Composer | `{composer: John Newton}` |
| `{lyricist}` | - | Lyricist | `{lyricist: John Newton}` |
| `{album}` | - | Album name | `{album: Hymns Collection}` |
| `{year}` | - | Year | `{year: 1779}` |
| `{key}` | - | Musical key | `{key: G}` |
| `{time}` | - | Time signature | `{time: 4/4}` |
| `{tempo}` | - | Tempo (BPM) | `{tempo: 90}` |
| `{capo}` | - | Capo position | `{capo: 2}` |

### Formatting Directives

Control text appearance and layout.

| Directive | Short | Description |
|-----------|-------|-------------|
| `{comment}` | `{c}` | Regular comment |
| `{comment_italic}` | `{ci}` | Italic comment |
| `{comment_box}` | `{cb}` | Boxed comment |
| `{highlight}` | - | Highlighted text |

**Examples:**
```chordpro
{comment: Play softly}
{comment_italic: With feeling}
{comment_box: Repeat 2x}
{highlight: Important section}
```

### Environment Directives

Define song sections with start/end pairs.

#### Chorus

```chordpro
{start_of_chorus}
[G]Amazing [D]grace, how [C]sweet the [G]sound
{end_of_chorus}
```

Short form: `{soc}` ... `{eoc}`

#### Verse

```chordpro
{start_of_verse}
[G]'Twas grace that [D]taught my [C]heart to [G]fear
{end_of_verse}
```

Short form: `{sov}` ... `{eov}`

#### Bridge

```chordpro
{start_of_bridge}
[Em]Through many [C]dangers, [G]toils and [D]snares
{end_of_bridge}
```

Short form: `{sob}` ... `{eob}`

#### Tab Section

```chordpro
{start_of_tab}
e|---0---2---3---|
B|---1---3---0---|
{end_of_tab}
```

Short form: `{sot}` ... `{eot}`

#### Chord Grid

```chordpro
{start_of_grid}
| G | D | Em | C |
| G | D | C  | G |
{end_of_grid}
```

Short form: `{sog}` ... `{eog}`

### Layout Directives

Control page layout and breaks.

| Directive | Short | Description |
|-----------|-------|-------------|
| `{column_break}` | `{colb}` | Force column break |
| `{new_page}` | `{np}` | Force page break |
| `{new_song}` | `{ns}` | Start new song |

## Inline Chords

Chords are placed inline with lyrics using square brackets:

```chordpro
[Am]This is a [G]line with [C]chords
```

The chords appear above the text at the position where they're inserted.

## Complete Example

```chordpro
{title: Amazing Grace}
{subtitle: Traditional Hymn}
{artist: John Newton}
{composer: John Newton}
{year: 1779}
{key: G}
{time: 3/4}
{tempo: 90}
{capo: 0}

{comment: Play gently}

{start_of_verse}
[G]Amazing [G7]grace, how [C]sweet the [G]sound
That saved a wretch like me
[G]I once was [G7]lost, but [C]now I'm [G]found
Was [D]blind, but [D7]now I [G]see
{end_of_verse}

{start_of_chorus}
'Twas [G]grace that [D]taught my [Em]heart to [C]fear
And [G]grace my [D]fears re[G]lieved
{end_of_chorus}

{comment_box: Repeat chorus 2x}

{start_of_bridge}
[Em]Through many [C]dangers, [G]toils and [D]snares
I [G]have al[C]ready [G]come
{end_of_bridge}
```

## CSS Classes

- `.chordpro-song` - Main container
- `.song-title` - Title (h1)
- `.song-subtitle` - Subtitle (h2)
- `.song-artist`, `.song-composer`, etc. - Metadata
- `.comment` - Regular comment
- `.comment.italic` - Italic comment
- `.comment-box` - Boxed comment
- `.highlight` - Highlighted text
- `.chorus`, `.verse`, `.bridge` - Section containers
- `.section-label` - Section label
- `.tab-section` - Tab container
- `.tab-content` - Tab content (pre)
- `.chord-grid` - Chord grid container
- `.grid-line` - Grid line
- `.grid-chord` - Individual chord in grid
- `.lyrics-line` - Line with lyrics
- `.lyrics-line .chord` - Inline chord
- `.column-break` - Column break marker
- `.page-break` - Page break marker

## Differences from Full Spec

This implementation includes the most commonly used ChordPro features. Not implemented:
- `{define}` chord diagrams (use separate diagram extension)
- `{transpose}` directive (use interactive controls)
- Conditional directives (`{if}`, `{endif}`)
- Font and color directives
- Custom metadata with `{meta}`
- Delegated environments (ABC, Lilypond, SVG)

For these features, use the appropriate ChordsMD extensions or external tools.
