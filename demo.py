import markdown
from my_extension import MyExtension

text = """
# Demo

This is a !!test!! of the extension.
It should highlight !!multiple!! words.
"""

html = markdown.markdown(text, extensions=[MyExtension()])
print(html)
