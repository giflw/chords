import markdown
from chordsmd import MyExtension
from chordsmd.chordpro import ChordProExtension

text = """
# Demo

This is a !!test!! of the extension.
It should highlight !!multiple!! words.

## Chords
Here are some chords: !!Am7!!, !!C/G!!, !!F#dim!!.

## Chord Sheet

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

## ChordPro Example

```chordpro
{title: ChordPro Song}
{st: Subtitle Here}

[Am]This is a [G]ChordPro [C]line.

{soc}
[F]Chorus [C]Text
{eoc}
```
"""

html = markdown.markdown(text, extensions=[MyExtension(), ChordProExtension()])
print(html)
