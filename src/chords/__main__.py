import sys

import markdown

from src.chords.chordsmd import ChordsMarkdownExtension
from src.chords.text_formatting import TextFormattingMarkdownExtension
from src.chords.mkcomments import CommentsExtension

template = """
<html class="debug">
<head>
    <meta charset="utf-8" />
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap');
        
        * {{
            break-inside: avoid;
        }}
        body {{
            column-count: 2;
            column-fill: auto;
            
            font-family: "Roboto", sans-serif;
            font-optical-sizing: auto;
            font-weight: 500;
            font-style: normal;
            font-variation-settings: "wdth" 100;
        }}
        code {{
            font-family: "Roboto Mono", monospace;
            font-optical-sizing: auto;
            font-weight: 500;
            font-style: normal;
        }}
        
        p {{
            break-before: avoid-column;
        }}
        h3 {{
            break-before: auto;
        }}
        .debug h3 {{
            border: 1px solid blue;
        }}
        h3+p, p+p {{
            break-before: avoid;
        }}
        .debug h3+p, .debug p+p {{
            border: 1px solid red;
        }}
        h1, h2 {{
            column-span: all;
        }}

        hr, hr+p {{
            display: none;
        }}
        .debug hr, .debug hr+p {{
            border: 1px solid green;
            display: block !important;
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
            html = markdown.markdown(input.read(), extensions=[ChordsMarkdownExtension(), TextFormattingMarkdownExtension(), CommentsExtension()])
            with open(f"{file}.html", 'w', encoding="utf-8") as output:
                output.write(template.format(html))
                print(f"Done processing {file} to {output.name}")
else:
    print("No files provided")
