# ChordsMD Cheat Sheet

Quick reference for all musical and screenplay notation formats supported by ChordsMD.

## 1. Chord Sheets (```chords)
Aligns chords above lyrics automatically.

```chords
[Chorus]
Am      G       C
I am a boy with a toy
```

- **Section Headers**: `[Chorus]`, `[Verse 1]`
- **Inline Chords**: `!!Am!!`
- **Embedding**: Use standard tab blocks inside chord sheets.

## 2. Tablature (```tab)
ASCII tabs rendered as SVG.

```tab
e|---0---|
B|---1---|
V   v A ^
```

- **Strokes**: `V`/`↓` (Strong Down), `v` (Weak Down), `A`/`↑`/`^` (Strong Up), `^` (Weak Up)
- **Techniques**: `h` (hammer), `p` (pull), `/` (slide up), `\` (slide down), `b` (bend), `v`/`~` (vibrato), `x` (mute)

## 3. ChordPro (```chordpro)
Structured lead sheet format.

```chordpro
{title: Song Name}
{start_of_chorus}
[Am]Lyric text here
{end_of_chorus}
```

- **Directives**: `{t}`, `{st}`, `{artist}`, `{key}`, `{capo}`
- **Environments**: `{soc}`, `{sov}`, `{sob}`, `{sog}`, `{sot}`
- **Comments**: `{c}`, `{ci}`, `{cb}`

## 4. Fountain Screenplay (```fountain)
Plain text screenwriting.

```fountain
INT. HOUSE - DAY
JOHN enters.

SARAH
(smiling)
Hello.
```

- **Scenes**: `INT.`, `EXT.`, `.HEADING`
- **Forced**: `@CHARACTER`, `>TRANSITION`
- **Special**: `^` (Dual), `~` (Lyrics), `>TEXT<` (Center), `===` (Page Break), `[[Note]]`

## 5. Strumming Patterns (```strum)
Visual rhythm guides.

```strum
Pattern: D du V au | D X V .
```

- **Notation**: `V`, `v`, `A`, `^` (High/Low Intensity Down/Up)
- **Mute/Pause**: `X` (Mute), `-` or `.` (Pause)
- **Grouping**: `( )`, `|` (Bar line), `1 2 3` (Beat numbers)

## 6. Chord Diagrams (```chord diagrams)
Fingering charts using `svguitar.js`.

```chord diagrams
C = x 3 2 0 1 0
B = 2.1 0 4.1 4.2 4.3 0 | 2.1
```

- **Definition**: `Name = String1 String2 ... | Barre`
- **Symbols**: `x`/`X` (Muted), `0`/`o`/`O` (Open)
- **Fingering**: `fret.finger` (e.g., `3.2`)

## 7. ABC Notation (```abc)
Standard musical stave notation.

```abc
X:1
T:Title
K:C
C D E F | G A B c
```

- **X**: Reference number
- **T**: Title
- **K**: Key
- **[A-G]**: Notes
