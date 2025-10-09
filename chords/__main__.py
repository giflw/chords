import sys

import markdown

from chordsmd import ChordsMarkdownExtension

files = sys.argv[1:]
if files:
    for file in files:
        with open(file, 'r') as input:
            html = markdown.markdown(input.read(), extensions=[ChordsMarkdownExtension()])
            with open(f"{file}.html", 'w') as output:
                output.write(html)
else:
    print("No files provided")
