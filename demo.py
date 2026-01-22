import markdown
from chordsmd import MyExtension

text = """
# Demo

This is a !!test!! of the extension.
It should highlight !!multiple!! words.

## Chords
Here are some chords: !!Am7!!, !!C/G!!, !!F#dim!!.
"""

html = markdown.markdown(text, extensions=[MyExtension()])
print(html)
