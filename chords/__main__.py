import markdown
import sys

from chords.chords import ChordsMarkdownExtension

files = sys.argv[1:]
for file in files:
    with open(file, 'r') as input:
        html = markdown.markdown(input.read(), extensions=[ChordsMarkdownExtension()])
        with open(f"{file}.html", 'w') as output:
            output.write(html)
