import markdown
from chordsmd import ChordSheetExtension
from chordsmd.chordpro import ChordProExtension
from chordsmd.tabs import TabExtension
from chordsmd.abc import AbcExtension

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

## ABC Notation Example

```abc
X: 1
T: Scale
M: 4/4
L: 1/4
K: C
C, D, E, F,|G, A, B, C|D E F G|A B c d|e f g a|b c' d' e'|f' g' a' b'|]
```
"""

html_body = markdown.markdown(text, extensions=[ChordSheetExtension(), ChordProExtension(), TabExtension(), AbcExtension()])

final_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ChordsMD Demo</title>
    <link rel="stylesheet" href="assets/style/style.css">
    <script src="assets/vendor/abcjs-basic-min.js"></script>
    <script src="assets/js/transposer.js"></script>
    <script src="assets/js/column-layout.js"></script>
    <style>
        body {{ font-family: sans-serif; padding: 20px; max-width: 1200px; margin: 0 auto; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; }}
        .col-btn.active {{ background: #007bff !important; color: white; font-weight: bold; }}
        .abc-midi {{ margin-top: 10px; }}
    </style>
</head>
<body>
{html_body}
<pre id="source" style="display:none">{text}</pre>
</body>
</html>
"""

with open('demo.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated demo.html")
