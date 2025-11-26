import os
import sys

import markdown

from src.giflwmd.chordsmd import ChordsMarkdownExtension
from src.giflwmd.fountain import FountainMarkdownExtension
from src.giflwmd.mkcomments import CommentsExtension
from src.giflwmd.text_formatting import TextFormattingMarkdownExtension

MODES = {
    "chords": ChordsMarkdownExtension(),
    "text_formating": TextFormattingMarkdownExtension(),
    "comments": CommentsExtension(),
    "fountain": FountainMarkdownExtension()
}

mode = sys.argv[1]
files = sys.argv[2:]

extension = MODES[mode]

if files:
    with open(os.path.join(os.path.dirname(__file__), "templates", f"{mode}.html"), "r") as file:
        template = file.read()
    for file in files:
        with open(file, 'r', encoding="utf-8") as input:
            html = markdown.markdown(
                input.read(),
                extensions=[extension]
            )
            with open(f"{file}.html", 'w', encoding="utf-8") as output:
                output.write(template % html)
                print(f"Done processing {file} to {output.name}")
else:
    print("No files provided")
