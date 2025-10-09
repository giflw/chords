import sys

import markdown

from chords.chordsmd import ChordsMarkdownExtension
from chords.text_formatting import TextFormattingMarkdownExtension

template = """
<html>
<head>
    <meta charset="utf-8" />
    <style>
        * {{
            break-inside: avoid;
        }}
        body {{
            column-count: 2;
            column-fill: auto;
        }}
        p {{
            break-before: avoid-column;
        }}
        h3 {{
            break-before: auto;
        }}
        h1, h2 {{
            column-span: all;
        }}
    </style>
</head>
<body>{}</body>
</html>
"""

files = sys.argv[1:]
if files:
    for file in files:
        with open(file, 'r', encoding="utf-8") as input:
            html = markdown.markdown(input.read(), extensions=[ChordsMarkdownExtension(), TextFormattingMarkdownExtension()])
            with open(f"{file}.html", 'w', encoding="utf-8") as output:
                output.write(template.format(html))
else:
    print("No files provided")
