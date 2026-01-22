# ChordsMD

This is a refreshing extension for Python Markdown that converts `!!text!!` into `<span class="custom-highlight">text</span>`.

## Usage

```python
import markdown
from chordsmd import MyExtension

text = "This is !!highlighted!!"
html = markdown.markdown(text, extensions=[MyExtension()])
print(html)
```
