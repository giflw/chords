import xml.etree.ElementTree as etree

import regex as re

from markdown import markdown, Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor


class AutoLinkInlineProcessor(InlineProcessor):

    def __init__(self):
        super().__init__(r'.*(https?://[^\s]+).*')

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | str | None, int | None, int | None]:
        link = m.group(1)
        note = etree.Element("a", { "href": link })
        note.text = link
        return note, m.start(1), m.end(1)

class IncludePreProcessor():
    """
    TODO
    """
    pass

class ExtrasMarkdownExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            #'characters_title': ['Characters', 'Title of list of characters']
        }
        super(ExtrasMarkdownExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.inlinePatterns.register(AutoLinkInlineProcessor(), "extras-autolink", 175)

def makeExtension(**kwargs):
    return ExtrasMarkdownExtension(**kwargs)


def parse(text: str, **kwargs) -> str:
    return markdown(text, extensions=[ExtrasMarkdownExtension(**kwargs)])
