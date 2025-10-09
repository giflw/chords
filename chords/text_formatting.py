import logging

from markdown import Extension, markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CodeInlineProcessor(SimpleTagInlineProcessor):
    """
    Replace ``anything`` by <del>anything</del>.

    >>> parse("``foo bar``")
    '<p><code>foo bar</code></p>'
    """

    def __init__(self):
        super().__init__(r'(``)(.*?)\1', 'code')


class DelInlineProcessor(SimpleTagInlineProcessor):
    """
    Replace --anything-- by <del>anything</del>.

    >>> parse("--foo bar--")
    '<p><del>foo bar</del></p>'
    """

    def __init__(self):
        super().__init__(r'(--)(.*?)\1', 'del')


class EmInlineProcessor(SimpleTagInlineProcessor):
    """
    Replace __anything__ by <em>anything</em>.

    >>> parse("__foo bar__")
    '<p><em>foo bar</em></p>'
    """

    def __init__(self):
        super().__init__(r'(__)(.*?)\1', 'em')


class InsInlineProcessor(SimpleTagInlineProcessor):
    """
    Replace ++anything++ by <ins>anything</ins>.

    >>> parse("++foo bar++")
    '<p><ins>foo bar</ins></p>'
    """

    def __init__(self):
        super().__init__(r'(\+\+)(.*?)\1', 'ins')


class MarkInlineProcessor(SimpleTagInlineProcessor):
    """
    Replace ##anything## by <mark>anything</mark>.

    >>> parse("==foo bar==")
    '<p><mark>foo bar</mark></p>'
    """

    def __init__(self):
        super().__init__(r'(==)(.*?)\1', 'mark')


class StrongInlineProcessor(SimpleTagInlineProcessor):
    """
    Replace **anything** by <strong>anything</strong>.

    >>> parse("**foo bar**")
    '<p><strong>foo bar</strong></p>'
    """

    def __init__(self):
        super().__init__(r'(\*\*)(.*?)\1', 'strong')


class TextFormattingMarkdownExtension(Extension):
    # def __init__(self, **kwargs):
    #    self.config = {
    #        'option1': ['value1', 'description1'],
    #        'option2': ['value2', 'description2']
    #    }
    #    super(TextFormattingMarkdownExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        for clazz in [CodeInlineProcessor, DelInlineProcessor, EmInlineProcessor, InsInlineProcessor,
                      MarkInlineProcessor, StrongInlineProcessor]:
            md.inlinePatterns.register(clazz(),
                                       clazz.__name__.replace("InlineProcessor", "").lower(), 175)


def makeExtension(**kwargs):
    return TextFormattingMarkdownExtension(**kwargs)


def parse(text: str) -> str:
    return markdown(text, extensions=[TextFormattingMarkdownExtension()])
