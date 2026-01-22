# AsciiDoc Text Formatting

**Extension:** `AsciidocExtension`  
**Config Option:** `asciidoc` (enabled by default)

## Overview

This extension adds support for AsciiDoc-style text formatting, providing convenient shorthands for common typographic elements and admonitions.

## Inline Formatting

| Syntax | HTML Result | Description | Example |
|--------|-------------|-------------|---------|
| `*text*` | `<strong>text</strong>` | Bold | `*bold*` |
| `_text_` | `<em>text</em>` | Italic | `_italic_` |
| `[~]text[~]` | `<del>text</del>` | Strikethrough | `[~]deleted[~]` |
| `[_]text[_]` | `<u>text</u>` | Underline | `[_]underlined[_]` |
| `#text#` | `<mark>text</mark>` | Highlight | `#Important#` |
| `+text+` | `<code>text</code>` | Monospace | `+git status+` |
| `^text^` | `<sup>text</sup>` | Superscript | `mc^2^` |
| `~text~` | `<sub>text</sub>` | Subscript | `H~2~O` |
| `` ``text'' `` | `<span>text</span>` | Double Quotes | `` ``text'' `` |
| `` `text' `` | `<span>text</span>` | Single Quotes | `` `text' `` |

### Examples

```markdown
E = mc^2^
H~2~O is water.
Use the +git commit+ command.
This is a #highlighted# word.
```

## Admonitions

AsciiDoc-style admonitions are rendered as styled boxes with titles. They must start at the beginning of a line.

| Trigger | Class | Visual |
|---------|-------|--------|
| `NOTE:` | `note` | Blue box |
| `TIP:` | `tip` | Green box |
| `IMPORTANT:` | `important` | Orange box |
| `WARNING:` | `warning` | Red box |
| `CAUTION:` | `caution` | Purple box |

### Example

```text
NOTE: This is a helpful note.
TIP: Remember to save your work.
WARNING: This action cannot be undone.
```

## CSS Styling

Admonitions are styled using the following classes in `assets/style/style.css`:

- `.admonition` - Base class for all admonition boxes.
- `.admonition.note`, `.admonition.tip`, etc. - Type-specific styling.
- `.admonition-title` - The bold title (e.g., NOTE).

## Configuration

The extension is enabled by default in `ChordsMDExtension`. To disable it:

```python
md = markdown.Markdown(extensions=[
    ChordsMDExtension(asciidoc=False)
])
```
