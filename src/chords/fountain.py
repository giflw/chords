import logging
import re
import xml.etree.ElementTree as etree

from markdown import markdown
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s [%(func)s] - %(message)s')


class FountainWrapperTreeProcessor(Treeprocessor):
    def run(self, root):
        new_root = etree.Element("div")

        wrapper = etree.Element("div")
        wrapper.set("class", "fountain")
        new_root.insert(0, wrapper)

        wrapper.extend(root.iterfind('*'))
        return new_root


class CenteredTextBlockProcessor(BlockProcessor):
    RE = re.compile(r'^\s*>\s*(.+)\s*<\s*')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        p = etree.SubElement(parent, 'p')
        p.set("class", "center")
        p.text = self.RE.sub(r'\1', blocks.pop(0))

class SceneHeadingBlockProcessor(BlockProcessor):

    # headers must not stat with !, as it indicates action
    RE = re.compile(r'^\s*(?<!!)((INT|EXT|EST|INT\./EXT|INT/EXT|I/E|\.)\.{0,1}\s*.*)\s*')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        p = etree.SubElement(parent, 'h3')
        p.set("class", "scene-heading")
        text = blocks.pop(0)
        p.text = self.RE.sub(r'\1', text[1:].lstrip() if text.startswith(".") else text)

class ActionForcedBlockProcessor(BlockProcessor):
    RE = re.compile(r'^\n*(\s*!.*)\s*')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        p = etree.SubElement(parent, 'p')
        p.text = self.RE.sub(r'\1', blocks.pop(0)).replace("!", "", 1)

class SynopsesBlockProcessor(BlockProcessor):
    RE = re.compile(r'^\s*=\s*(.+)\s*')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        p = etree.SubElement(parent, 'p')
        p.set("class", "synopses")
        p.text = self.RE.sub(r'\1', blocks.pop(0))

class BoneyardPreprocessor(Preprocessor):
    """
    If you want Fountain to ignore some text, wrap it with /* some text */.
    In this example, an entire scene is put in the boneyard.
    It will be ignored completely on formatted output.

    Escape using \\/* */.
    """

    def run(self, lines):
        logging.info(lines)
        lines = "\n".join(lines)
        lines = lines.replace(r'\/*', '\v')
        lines = re.sub(r"\\?/\*.*?\*/", "", lines, flags=re.MULTILINE | re.DOTALL | re.UNICODE)
        lines = lines.replace('\v', '/*')
        logging.info(lines)
        return lines.split("\n")


class FountainMarkdownExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'option1': ['value1', 'description1'],
            'option2': ['value2', 'description2']
        }
        super(FountainMarkdownExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.inlinePatterns.deregister("em_strong")
        md.inlinePatterns.deregister("em_strong2")

        md.parser.blockprocessors.deregister("quote")

        md.preprocessors.register(BoneyardPreprocessor(md), 'fountain-comments', 175)

        ## process scene headers, without as long they dont start with !
        ## --> \s*(?<!!)(INT|EXT|EST|INT\./EXT|INT/EXT|I/E)\.{0,1}.*\s*
        ### scene numbers must be computed at compile time and setted to data-scene-number
        ## --> .*#\s*(.*?)\s*#\s* (only last # # ocurrence
        ## after this, inline mark # # can work as expected
        md.parser.blockprocessors.register(SceneHeadingBlockProcessor(md.parser), "fountain-scene-heading", 175)
        md.parser.blockprocessors.register(SynopsesBlockProcessor(md.parser), "fountain-synopses", 175)
        md.parser.blockprocessors.register(CenteredTextBlockProcessor(md.parser), 'fountain-centered-text', 175)
        md.parser.blockprocessors.register(ActionForcedBlockProcessor(md.parser), "fountain-action-forced", 170)


        md.treeprocessors.register(FountainWrapperTreeProcessor(md), 'fountain-wrapper', 175)


def makeExtension(**kwargs):
    return FountainMarkdownExtension(**kwargs)


def parse(text: str) -> str:
    return markdown(text, extensions=[FountainMarkdownExtension()])
