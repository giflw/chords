import logging
import re
import xml.etree.ElementTree as etree

from markdown import markdown
from markdown.blockparser import BlockParser
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.preprocessors import Preprocessor
from markdown.util import deprecated

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CommentsPreprocessor(Preprocessor):
    """
    Skip any line starting with // (can be preceded by spaces).

    >>> parse("foo\\n// bar")
    '<p>foo</p>'
    """

    def run(self, lines):
        new_lines = []
        for line in lines:
            m = re.search(r"\s*//", line)
            if not m:
                # any line not starting with // is passed through
                new_lines.append(line)
        return new_lines


class TagsPreprocessor(Preprocessor):
    """
    Render words prefixed by # as tags.

    >>> parse("# foo\\n#bar")
    '<h1>foo</h1>\\n<p><span class="tag">bar</span></p>'
    """

    def run(self, lines):
        """
        Replace #... with <span class="tag">...</span>
        First char must be letter or number
        """

        new_lines = []
        for line in lines:
            line = re.sub(r'#([a-zA-Z0-9]+\S+)', r'<span class="tag">\1</span>', line)
            new_lines.append(line)
        return new_lines


class ChordWrapperPreprocessor(Preprocessor):
    """
    Single line of chords are detected and each chord is wrapped in span

    >>> parse("C   Am E# Ddim C4(9)")
    '<p><span class="chord">C</span>   <span class="chord">Am</span> <span class="chord">E#</span> <span class="chord">Ddim</span> <span class="chord">C4(9)</span></p>'

    >>> parse("Ah, this is a C grade.")
    '<p>Ah, this is a C grade.</p>'
    """

    def run(self, lines):
        new_lines = []
        for line in lines:
            if re.match(r'^ *(([A-H][1-9Mm#bdisue°+()/-]*) *)+ *$', line):
                line = re.sub(r'([A-H][1-9Mm#bdisue°+()/-]*)', r'<span class="chord">\1</span>', line)
            new_lines.append(line)
        return new_lines


@deprecated("FIXME")
class ChordsInlineProcessor(SimpleTagInlineProcessor):
    """
    Parse chords and wrap inside tag

    >>> parse("foo bar A#m C D4 Edim(9)")
    '<p><del>foo bar</del></p>'
    """

    def __init__(self):
        super().__init__(r'[A-H1-9Mm#bdisue°+\%()*~v^|!?\&: ><\[\]/mpf-]+', 'span')

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element, int, int]:  # pragma: no cover
        import rich
        rich.print(m)
        """
        Return [`Element`][xml.etree.ElementTree.Element] of type `tag` with the string in `group(2)` of a
        matching pattern as the Element's text.
        """
        el = etree.Element(self.tag)
        el.text = m.group(2)
        return el, m.start(0), m.end(0)


@deprecated("Should be reviewed")
class BoxBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'^ *!{3,} *\n'  # start line, e.g., `   !!!! `
    RE_FENCE_END = r'\n *!{3,}\s*$'  # last non-blank line, e.g, '!!!\n  \n\n'

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

        # Find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # remove fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)
                # render fenced area inside a new div
                e = etree.SubElement(parent, 'div')
                e.set('style', 'display: inline-block; border: 1px solid red;')
                self.parser.parseBlocks(e, blocks[0:block_num + 1])
                # remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # or could have had no return statement
        # No closing marker!  Restore and do nothing
        blocks[0] = original_block
        return False  # equivalent to our test() routine returning False


@deprecated("Should be reviewed")
class VerbatimBlockProcessor(BlockProcessor):
    """
    Use div with pre style in this section

    >>> parse(':verbatim:\\nfoo\\n  bar\\n\\n:verbatim:')
    '<div class="verbatim" style="font-family: monospace; display: block; border: 1px solid green; background-color: #f9f9f9; white-space: pre-wrap">\\n<p>foo\\n  bar</p>\\n</div>'
    """

    RE_FENCE_START = r'^ *:verbatim: *'  # start line, e.g., `   !!!! `
    RE_FENCE_END = r' *:verbatim:\s*$'  # last non-blank line, e.g, '!!!\n  \n\n'

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

        # Find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # remove fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)
                # render fenced area inside a new pre
                e = etree.SubElement(parent, 'div')
                e.set('style',
                      'font-family: monospace; display: block; border: 1px solid green; background-color: #f9f9f9; white-space: pre-wrap')
                e.set('class', 'verbatim')
                self.parser.parseBlocks(e, blocks[0:block_num + 1])
                # remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # or could have had no return statement
        # No closing marker!  Restore and do nothing
        blocks[0] = original_block
        return False  # equivalent to our test() routine returning False


class HardbreakBlockProcessor(BlockProcessor):
    """
    Force breaks on \\n as <br />.
    Do not break spaces, but use NBSP instead.

    >>> parse(':hardbreak:\\nfoo  \\n  bar\\n:hardbreak:')
    '<p><br />foo\xa0\xa0<br />\xa0\xa0bar<br /></p>'
    """
    NBSP = "\u00A0"
    RE_FENCE_START = r'^ *:hardbreak: *'  # start line, e.g., `   !!!! `
    RE_FENCE_END = r' *:hardbreak:\s*$'  # last non-blank line, e.g, '!!!\n  \n\n'

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

        # Find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # remove fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)

                hardbreak_blocks = [line.replace(" ", self.NBSP).replace("\n", "<br />") for line in
                                    blocks[0:block_num + 1]]
                self.parser.parseBlocks(parent, hardbreak_blocks)
                # remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # or could have had no return statement
        # No closing marker!  Restore and do nothing
        blocks[0] = original_block
        return False  # equivalent to our test() routine returning False


@deprecated("Should be reviewed")
class AdocListingBlockProcessor(HardbreakBlockProcessor):
    """
    Force breaks on \\n as <br />.
    Do not break spaces, but use NBSP instead.

    >>> parse('----\\nfoo  \\n  bar\\n----')
    '<p><br />foo\xa0\xa0<br />\xa0\xa0bar<br /></p>'
    """


class ChordsSectionBlockProcessor(BlockProcessor):
    def __init__(self, parser: BlockParser, re_start: str, re_end: str):
        super().__init__(parser)
        self.RE_FENCE_START = re_start
        self.RE_FENCE_END = re_end

    def test(self, parent, block):
        return re.match(self.RE_FENCE_START, block)

    def run(self, parent: etree.Element, blocks: list[str]) -> bool | None:
        # logging.warning(f"enter -> {blocks}")
        block = blocks.pop(0)
        # logging.warning(f"title -> {block}")
        new_parent = etree.SubElement(parent, 'div')
        new_parent.set('class', 'chords-section')
        e = etree.SubElement(new_parent, 'h3')
        e.text = re.sub(self.RE_FENCE_START, r'\1', block)

        blocks_to_parse = []
        for block_num, block in enumerate(blocks):
            #    logging.warning(f"for -> {block}")
            # logging.warning(f"close {block} re: {self.RE_FENCE_END} search: {re.search(self.RE_FENCE_END, block)}")
            if re.search(self.RE_FENCE_END, block):
                # logging.warning(f"end -> {blocks}")
                break
            else:
                blocks_to_parse.append(block)
        #        logging.warning(f"next -> {blocks}")
        #        logging.warning(f"next to parse -> {blocks_to_parse}")
        self.parser.parseBlocks(new_parent, [*blocks_to_parse])
        for _ in blocks_to_parse:
            blocks.pop(0)
        #    logging.warning(f"pop -> {blocks}")
        # logging.warning(f"exiting -> {blocks}")
        return True


class BracketChordsSectionBlockProcessor(ChordsSectionBlockProcessor):
    """
    FIXME DOC

    >>> parse(' [sectname1]\\n\\nfoo  \\n  bar\\n\\n[nextsect-bracket]')
    '<div class="chords-section">\\n<h3>sectname1</h3>\\n<p>foo<br />\\n  bar</p>\\n</div>\\n<div class="chords-section">\\n<h3>nextsect-bracket</h3>\\n</div>'

    >>> parse('\\n[Intro]\\n\\n[Verso 1]\\n\\nfoo bar\\n')
    '<div class="chords-section">\\n<h3>Intro</h3>\\n</div>\\n<div class="chords-section">\\n<h3>Verso 1</h3>\\n<p>foo bar</p>\\n</div>'


    """

    def __init__(self, parser: BlockParser):
        super().__init__(parser, r'^ *\[(.*)\] *', r' *\[.*\]\s*$')


class DotSectionBlockProcessor(ChordsSectionBlockProcessor):
    """
    FIXME DOC

    >>> parse(' .sectname1.\\n\\nfoo  \\n  bar\\n\\n.nextsect-dots.')
    '<div class="chords-section">\\n<h3>sectname1</h3>\\n<p>foo<br />\\n  bar</p>\\n</div>\\n<div class="chords-section">\\n<h3>nextsect-dots</h3>\\n</div>'

    """

    def __init__(self, parser: BlockParser):
        super().__init__(parser, r'^ *\.(.*)\. *', r' *\..*\.\s*$')


class ChordsMarkdownExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'option1': ['value1', 'description1'],
            'option2': ['value2', 'description2']
        }
        super(ChordsMarkdownExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.preprocessors.register(ChordWrapperPreprocessor(md), 'chords_pre', 175)
        md.preprocessors.register(CommentsPreprocessor(md), 'comment', 175)
        md.preprocessors.register(TagsPreprocessor(md), 'tag', 175)

        # md.parser.blockprocessors.register(AdocListingBlockProcessor(md.parser), 'adoc-listing-block', 175)
        md.parser.blockprocessors.register(HardbreakBlockProcessor(md.parser), 'hardbreak', 175)

        md.parser.blockprocessors.register(BracketChordsSectionBlockProcessor(md.parser), 'chords-sections-brackets',
                                           175)
        md.parser.blockprocessors.register(DotSectionBlockProcessor(md.parser), 'chords-sections-dots', 175)


def makeExtension(**kwargs):
    return ChordsMarkdownExtension(**kwargs)


def parse(text: str) -> str:
    return markdown(text, extensions=[ChordsMarkdownExtension()])
