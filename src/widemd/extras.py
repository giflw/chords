import xml.etree.ElementTree as etree

import regex as re
from markdown import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.preprocessors import Preprocessor


class AutoLinkInlineProcessor(InlineProcessor):

    def __init__(self):
        super().__init__(r'.*(https?://[^\s]+).*')

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | str | None, int | None, int | None]:
        link = m.group(1)
        note = etree.Element("a", {"href": link})
        note.text = link
        return note, m.start(1), m.end(1)


class IncludePreprocessor(Preprocessor):
    """
    // include
    """

    priority = 500

    RE = re.compile(r"^\s*//\s*include\s+([\S].+[\S])\s*")

    def run(self, lines):
        new_lines = []
        for line in lines:
            match = self.RE.search(line)
            if match:
                filename = match.group(1)
                print(f"Including [{filename}]")
                with open(filename, "r", encoding="UTF-8") as file:
                    included_lines = file.read().split("\n")
                    # empty string are simple new line breaks
                    new_lines.extend(['', '', f"<!-- include start: {filename} -->", '', ''])
                    new_lines.extend(included_lines)
                    new_lines.extend(['', '', f"<!-- include end: {filename} -->", '', ''])
                print(f"[{filename}] included.")
            else:
                new_lines.append(line)
        return new_lines


class ExtrasMarkdownExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            # 'characters_title': ['Characters', 'Title of list of characters']
        }
        super(ExtrasMarkdownExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.preprocessors.register(IncludePreprocessor(), "extras-include", IncludePreprocessor.priority)
        md.inlinePatterns.register(AutoLinkInlineProcessor(), "extras-autolink", 175)


def makeExtension(**kwargs):
    return ExtrasMarkdownExtension(**kwargs)


def parse(text: str, **kwargs) -> str:
    return markdown(text, extensions=[ExtrasMarkdownExtension(**kwargs)])
