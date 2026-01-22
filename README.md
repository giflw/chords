# My Markdown Extension

This is a simple extension for Python Markdown that converts `!!text!!` into `<span class="custom-highlight">text</span>`.

## Usage

```python
import markdown
from my_extension import MyExtension

text = "This is !!highlighted!!"
html = markdown.markdown(text, extensions=[MyExtension()])
print(html)
```
