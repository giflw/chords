import logging
import xml.etree.ElementTree as etree

import regex as re
from markdown import markdown, Markdown
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor

CHARACTER_REGISTRY_NAME = "fountain_character_registry"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s [%(func)s] - %(message)s')


class FountainWrapperTreeProcessor(Treeprocessor):
    def run(self, root):
        new_root = etree.Element("div")

        wrapper = etree.Element("div")
        wrapper.set("class", "fountain")
        new_root.insert(0, wrapper)

        script = etree.SubElement(wrapper, "div")
        script.set("class", "script")

        script.extend(root.iterfind('*'))
        return new_root


class FountainCharacterListTreeProcessor(Treeprocessor):

    def __init__(self, md: Markdown | None = None, config=None):
        super().__init__(md)
        self.config = config

    def run(self, root: etree.Element):
        fountain = root[0]
        char_list = None
        for char in [p for p in fountain.iter("p") if p.get("class") == "character"]:
            if char_list is None:
                char_div = etree.SubElement(fountain, "div")
                char_div.set("class", "characters")

                char_head = etree.SubElement(char_div, "h3")
                char_head.text = self.config.get("characters_title", "Characters")

                char_list = etree.SubElement(char_div, "ol")
            li = etree.SubElement(char_list, "li")
            li.text = char.text
        return root


class BoneyardPreprocessor(Preprocessor):
    """
    If you want Fountain to ignore some text, wrap it with /* some text */.
    In this example, an entire scene is put in the boneyard.
    It will be ignored completely on formatted output.

    Escape using \\/* */.
    """

    def run(self, lines):
        lines = "\n".join(lines)
        lines = lines.replace(r'\/*', '\v')
        lines = re.sub(r"(?<!\\)\/\*.*?\*\/", "", lines, flags=re.DOTALL)
        lines = lines.replace('\v', '/*')
        return lines.split("\n")


class SceneHeadingBlockProcessor(BlockProcessor):
    """
    Uses h3 to define scene headings
    """
    ## process scene headers, without as long they dont start with !
    ## --> \s*(?<!!)(INT|EXT|EST|INT\./EXT|INT/EXT|I/E)\.{0,1}.*\s*
    ### scene numbers must be computed at compile time and setted to data-scene-number
    ## --> .*#\s*(.*?)\s*#\s* (only last # # ocurrence
    ## after this, inline mark # # can work as expected

    # headers must not stat with !, as it indicates action
    RE = re.compile(r'^\s*(?<!!)((INT|EXT|EST|INT\./EXT|INT/EXT|I/E|\.)\.?\s*.*)(#[^#]+#)*\s*$')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        p = etree.SubElement(parent, 'h3')
        p.set("class", "scene-heading")
        text = blocks.pop(0)
        text = self.RE.sub(r'\1', text[1:].lstrip() if text.startswith(".") else text)
        number = ""
        splitted = text.split("#")
        # if has number, it has 2 #, so it will be at least 3 in lenght
        if len(splitted) >= 3:
            # last item is empty
            number = splitted[-2].strip()
            text = "#".join(splitted[0:-2]).strip()
        p.text = text
        if number:
            p.text = f"{p.text} "
            p.set("data-scene-number", number)
            span = etree.SubElement(p, "span")
            span.text = number
            span.set("class", "scene-number")


class CenteredTextBlockProcessor(BlockProcessor):
    RE = re.compile(r'^\s*>\s*(.+?)\s*<\s*$')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        p = etree.SubElement(parent, 'p')
        p.set("class", "center")
        p.text = self.RE.sub(r'\1', blocks.pop(0))

class LyricsBlockProcessor(BlockProcessor):
    RE = re.compile(r'^\s*\~\s*(.+?)')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        p = etree.SubElement(parent, 'p')
        p.set("class", "lyrics")

        p = etree.SubElement(p, "i")
        block = blocks.pop(0)
        text = "<br />\n".join([re.sub(r'\~\s?(\*{2})?', "", line) for line in block.split("\n")])
        p.text = self.RE.sub(r'\1', text)


class ActionBlockProcessor(BlockProcessor):
    """
    As action is anything that is not other thing,
    any block not recognized as special will be turned in paragraph,
    as it should for actions.

    Here with add support for edge cases and forced actions.
    """

    RE_FORCED = re.compile(r'^\s*!(.*)\s*$')
    RE_TABBED = re.compile(r'^(\s+\S+.*)\s*$', flags=re.DOTALL)

    def test(self, parent, block):
        self.last_match = None
        if self.RE_FORCED.search(block):
            self.last_match = True
        elif self.RE_TABBED.search(block):
            self.last_match = False

        return bool(self.last_match is not None)

    def run(self, parent, blocks):
        block = blocks.pop(0)
        p = etree.SubElement(parent, 'p')
        if self.last_match is True:
            p.text = self.RE_FORCED.sub(r'\1', block)
        elif self.last_match is False:
            # force line breaks with br and tab using 4 spaces
            p.text = (
                self.RE_TABBED.sub(r'\1', block)
                .replace("\n", " <br />")
                .replace("\t", "    ")
            )
            p.set("style", "white-space: pre")


class SynopsesBlockProcessor(BlockProcessor):
    RE = re.compile(r'^\s*=\s*(.+)\s*$')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        p = etree.SubElement(parent, 'p')
        p.set("class", "synopses")
        p.text = self.RE.sub(r'\1', blocks.pop(0))


class CharacterBlockProcessor(BlockProcessor):
    RE_DEFAULT = re.compile(r'^\s*([[:upper:] -]+[(\w)]*)\s*$', flags=re.UNICODE | re.MULTILINE)
    RE_FORCED = re.compile(r'^\s*@(.+)\s*$', flags=re.MULTILINE)

    def test(self, parent, block):
        return bool(self.RE_DEFAULT.search(block) or self.RE_FORCED.search(block))

    def run(self, parent, blocks):
        block = blocks[0]
        block, *tail = block.split("\n")
        blocks[0] = "\n".join(tail)
        character = None
        if self.RE_DEFAULT.search(block):
            character = self.RE_DEFAULT.sub(r'\1', block)
        elif self.RE_FORCED.search(block):
            character = self.RE_FORCED.sub(r'\1', block)
        if character:
            p = etree.SubElement(parent, "p")
            p.set("class", "character")
            p.text = character


class BlockContinuationPostprocessor(Postprocessor):

    def run(self, text):
        parts = text.split("\n")
        last_part_was_break = False
        for i in range(0, len(parts)):
            if parts[i] == "**":
                if last_part_was_break:
                    parts[i] = "<br />"
                else:
                    last_part_was_break = True
                    parts[i] = "<br />\n<br />"
            else:
                last_part_was_break = False
        return "\n".join(parts)


# class DialogBlockProcessor(BlockProcessor):
#     RE_DEFAULT = re.compile(r'^\s*([A-Z0-9- ]+(\(\w*\))*)\s*\^?\s*\n')
#     RE_FORCED = re.compile(r'^\s*@(.+)\s*\^?\s*\n')
#
#     def test(self, parent, block):
#         return bool(self.RE_DEFAULT.search(block) or self.RE_FORCED.search(block))
#
#     def run(self, parent, blocks):
#         block = blocks[0]
#         div = etree.SubElement(parent, 'div')
#         div.set("class", "dialog")
#         dialog_blocks = block.split("\n")
#         self.parser.parseBlocks(div, dialog_blocks)


class FountainMarkdownExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'characters_title': ['Characters', 'Title of list of characters']
        }
        super(FountainMarkdownExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        base_priority = 275
        md.inlinePatterns.deregister("em_strong")
        md.inlinePatterns.deregister("em_strong2")
        md.parser.blockprocessors.deregister("quote")

        # print("PRE REGISTERED PROCESSORS")
        # print(md.inlinePatterns._data)

        md.preprocessors.register(BoneyardPreprocessor(md), 'fountain-comments', base_priority)

        block_proc_reg = md.parser.blockprocessors.register

        # md.parser.blockprocessors.register(DialogBlockProcessor(md.parser), "fountain-dialog", base_priority - 100)

        block_proc_reg(SceneHeadingBlockProcessor(md.parser), "fountain-scene-heading", base_priority)
        block_proc_reg(SynopsesBlockProcessor(md.parser), "fountain-synopses", base_priority)
        block_proc_reg(CenteredTextBlockProcessor(md.parser), 'fountain-centered-text', base_priority)
        block_proc_reg(LyricsBlockProcessor(md.parser), 'fountain-lyrics', base_priority)

        block_proc_reg(ActionBlockProcessor(md.parser), "fountain-action", base_priority - 20)
        block_proc_reg(CharacterBlockProcessor(md.parser), "fountain-character", base_priority - 5)

        # inline_proc_reg = md.inlinePatterns.register
        # inline_proc_reg(BlockContinuationNthInlineProcessor(), "fountain-block-continuation-nth", base_priority + 10)
        # inline_proc_reg(BlockContinuationExtraInlineProcessor(), "fountain-block-continuation-extra", base_priority + 5)
        # inline_proc_reg(BlockContinuationFirstInlineProcessor(), "fountain-block-continuation-first", base_priority)

        tree_reg = md.treeprocessors.register
        tree_reg(FountainWrapperTreeProcessor(md), 'fountain-wrapper', base_priority)
        tree_reg(FountainCharacterListTreeProcessor(md, self.getConfigs()), 'fountain-character-list', base_priority)

        md.postprocessors.register(BlockContinuationPostprocessor(md), "fountain-block-continuation", base_priority)

def makeExtension(**kwargs):
    return FountainMarkdownExtension(**kwargs)


def parse(text: str, **kwargs) -> str:
    return markdown(text, extensions=[FountainMarkdownExtension(**kwargs)])
