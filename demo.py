import markdown
from chordsmd import MyExtension
from chordsmd.chordpro import ChordProExtension
from chordsmd.tabs import TabExtension

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

## Tablature Example

```tab
e|---------0-----------|
B|-------1---1---------|
G|-----0-------0-------|
D|---2-----------2-----|
A|-3-------------------|
E|---------------------|
```
"""

html_body = markdown.markdown(text, extensions=[MyExtension(), ChordProExtension(), TabExtension()])

final_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ChordsMD Demo</title>
    <link rel="stylesheet" href="style.css">
    <style>
        body {{ font-family: sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open('demo.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated demo.html")
