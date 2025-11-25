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


class WrapperTreeProcessor(Treeprocessor):

    def run(self, root):
        new_root = etree.Element("div")

        wrapper = etree.Element("div")
        wrapper.set("class", "fountain")
        new_root.insert(0, wrapper)

        script = etree.SubElement(wrapper, "div")
        script.set("class", "script")

        script.extend(root.iterfind('*'))
        return new_root


class CharacterListTreeProcessor(Treeprocessor):

    def __init__(self, md: Markdown | None = None, config=None):
        super().__init__(md)
        self.config = config

    def run(self, root: etree.Element):
        fountain = root[0]
        char_list = None
        char_set = set()
        for char in [p for p in fountain.iter("p") if p.get("class") == "character"]:
            char_set.add(char.text)

        for char in sorted(char_set):
            if char_list is None:
                char_div = etree.SubElement(fountain, "div")
                char_div.set("class", "characters")

                char_head = etree.SubElement(char_div, "h3")
                char_head.text = self.config.get("characters_title", "Characters")

                char_list = etree.SubElement(char_div, "ol")
            li = etree.SubElement(char_list, "li")
            li.text = char
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


class BlockContinuation:
    BLK_CONT = f"[|BlckCntntn|]"
    LF = f"[|LnFd|]"


class BlockContinuationPreprocessor(Preprocessor):

    def run(self, lines):
        new_lines = []
        first_new_line = True
        for line in lines:
            if line == "  " or line == "**":
                # if first_new_line:
                #    first_new_line = False
                #    new_lines.append(BlockContinuation.BLK_CONT)
                new_lines.append(BlockContinuation.BLK_CONT)
            else:
                first_new_line = True
                new_lines.append(line)
        return new_lines


class BlockContinuationPostprocessor(Postprocessor):

    def run(self, text):
        return text.replace(BlockContinuation.BLK_CONT, "").replace(BlockContinuation.LF, "<br />\n")


class LineBreaksTreeProcessor(Treeprocessor):

    def run(self, root):
        fountain = root[0]
        for par in [p for p in fountain.iter("p") if p.get("class") == ActionBlockProcessor.CLASS]:
            if "\n" in par.text:
                par.text = par.text.replace("\n", f"{BlockContinuation.LF}")
        return root


class TitlePageBlockProcessor(BlockProcessor):
    """
    Match one or two words followed by ":"
    """
    RE = re.compile(r'^[\n]*([\w\d]+( [\w\d]+)?:.*(\n\s+.*)*)', flags=re.MULTILINE)

    HEADER = "header"
    TITLE = "title"
    AUTHOR = "author"
    AUTHORS = "authors"
    CREDIT = "credit"
    REVISION = "revision"
    SOURCE = "source"
    NOTES = "notes"
    DRAFT_DATE = "draft date"
    FOOTER = "footer"

    """
    Add option to translate keys, using dict.
    Add ignore case key iteration.
    Keys are processed in this order.
    """
    KEYS = [
        HEADER, TITLE, AUTHOR, AUTHORS, REVISION, SOURCE,
        DRAFT_DATE, FOOTER
    ]

    title_processed = False

    def test(self, parent, block):
        if self.title_processed:
            return False
        self.title_processed = True
        print("self.RE.search(block)")
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        last_pos = 0
        part = True
        information = {}
        while part:
            part = self.RE.search(block, last_pos)
            if part:
                meta = part.group(0)
                last_pos = part.end(0)
                name, values = meta.split(":", maxsplit=1)
                values = [v.strip() for v in values.split("\n") if v]
                information[name.lower()] = values

        page = etree.SubElement(parent, "div", {"class": "title-page"})
        self.header = etree.SubElement(page, "div", {"class": "header"})
        self.top = etree.SubElement(page, "div", {"class": "title-page-top"})
        self.center = etree.SubElement(page, "div", {"class": "title-page-center"})
        self.bottom = etree.SubElement(page, "div", {"class": "title-page-bottom"})
        self.footer = etree.SubElement(page, "div", {"class": "footer"})

        for info_name in self.KEYS:
            func_name = f"info_{info_name.lower().replace(" ", "_")}"
            func = getattr(self, func_name) if hasattr(self, func_name) else None
            if func and info_name in information:
                values = information.pop(info_name)
                func(values, information)

        self.info_notes(information.pop(self.NOTES, []), information)
        import pprint
        pprint.pp(information)

    def info_header(self, values: list[str], information):
        for value in values:
            etree.SubElement(self.header, "div").text = value

    def info_title(self, values: list[str], information):
        etree.SubElement(self.top, "h1", {"class": "title"}).text = values[0]
        if len(values) > 1:
            etree.SubElement(self.top, "h2", {"class": "subtitle"}).text = values[1]
        if len(values) > 2:
            for extra in values[2:]:
                etree.SubElement(self.top, "p", {"class": "subsubtitle"}).text = extra

    def info_author(self, values: list[str], information):
        self.info_authors(values, information)

    def info_authors(self, values: list[str], information):
        p_credit = etree.SubElement(self.top, "p", {"class": "credit"})
        credit = " ".join(information.pop(self.CREDIT, ""))
        p_credit.text = f"{credit} " if credit else ""
        last_author = None
        for author in values:
            if last_author is not None:
                last_author.tail = ", "
            last_author = etree.SubElement(p_credit, "span", {"class": "author"})
            last_author.text = author

    def info_revision(self, values: list[str], information):
        etree.SubElement(self.top, "p", {"class": "revision"}).text = " ".join(values)

    def info_source(self, values: list[str], information):
        etree.SubElement(self.top, "p", {"class": "source"}).text = " ".join(values)


    def info_notes(self, values: list[str], information):
        metas = etree.SubElement(self.center, "div", {"class": "metas"})
        if values:
            notes = etree.SubElement(metas, "div", {"class": "notes"})
            for value in values:
                etree.SubElement(notes, "p").text = value
        # Unknown info keys
        for info in set(information.keys()):
            if info not in self.KEYS:
                values = information.pop(info)
                div = etree.SubElement(metas, "div", {"data-information-key": info.lower().replace(" ", "-")})
                for value in values:
                    etree.SubElement(div, "p").text = value

    def info_draft_date(self, values: list[str], information):
        etree.SubElement(self.bottom, "p", {"class": "draft-date"}).text = " ".join(values)

    def info_footer(self, values: list[str], information):
        for value in values:
            etree.SubElement(self.footer, "div").text = value


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
        text = "<br />\n".join([re.sub(r'^\~\s?(\*{2})?', "", line) for line in block.split("\n")])
        p.text = self.RE.sub(r'\1', text)


class ActionBlockProcessor(BlockProcessor):
    """
    As action is anything that is not other thing,
    any block not recognized as special will be turned in paragraph,
    as it should for actions.

    Here with add support for edge cases and forced actions.
    """

    CLASS = "action"

    # if starts with ! is an action
    RE_FORCED = re.compile(r'^\s*!(.*)\s*$')
    # ignores = synopses, # sections or @ characters
    RE_TABBED = re.compile(r'^(\s*[^=#@]\S+.*)\s*$', flags=re.DOTALL)

    def test(self, parent, block):
        self.last_match = None
        if self.RE_FORCED.search(block):
            self.last_match = True
        elif self.RE_TABBED.search(block):
            self.last_match = False

        return bool(self.last_match is not None)

    def run(self, parent, blocks):
        block = blocks.pop(0)
        # FIXME add class action
        p = etree.SubElement(parent, 'p', {"class": "action"})
        if self.last_match is True:
            p.text = self.RE_FORCED.sub(r'\1', block)
        elif self.last_match is False:
            # force line breaks with br and tab using 4 spaces
            text = self.RE_TABBED.sub(r'\1', block)
            new_lines = []
            for line in text.split("\n"):
                linestripped = line.lstrip(" ")
                if not new_lines and not linestripped:
                    # skip first nth empty lines
                    continue
                line = (u'\xa0' * (len(line) - len(linestripped))) + linestripped
                new_lines.append(line.rstrip())
            text = "\n".join(new_lines)

            p.text = text


class SynopsesBlockProcessor(BlockProcessor):
    RE = re.compile(r'^\s*=[^=]\s*(.+)\s*$')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        p = etree.SubElement(parent, 'p')
        p.set("class", "synopses")
        p.text = self.RE.sub(r'\1', blocks.pop(0))


class PageBreakBlockProcessor(BlockProcessor):
    RE = re.compile(r'^\s*===\s*$')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        blocks.pop(0)
        el = etree.SubElement(parent, 'div')
        el.set("class", "page-break")  # <div style="break-after:page"></div>


class DialogueBlockProcessor(BlockProcessor):
    RE_DEFAULT = re.compile(r'^\s*([[:upper:]]{1}[^[:lower:]]+?)\s*$', flags=re.UNICODE | re.MULTILINE)
    RE_FORCED = re.compile(r'^\s*@(.+)\s*$', flags=re.MULTILINE)

    RE_PARENTHETICAL = re.compile(r'^\s*(\(.+\))\s*$', re.MULTILINE)

    def test(self, parent, block):
        return bool(self.RE_DEFAULT.search(block) or self.RE_FORCED.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        dialog = etree.SubElement(parent, "div", {"class": "dialogue"})

        character, *tail = block.split("\n")
        if not character:
            character, *tail = tail
        if self.RE_DEFAULT.search(character):
            character = self.RE_DEFAULT.sub(r'\1', character)
        elif self.RE_FORCED.search(character):
            character = self.RE_FORCED.sub(r'\1', character)
        if character.endswith("^"):
            character = character[:-1].strip()
            dialog.set("class", f"{dialog.get("class")} dual")
        p = etree.SubElement(dialog, "p", {"class": "character"})
        p.text = character

        spoken_words = None
        for line in tail:
            if self.RE_PARENTHETICAL.search(line):
                p = etree.SubElement(dialog, "p", {"class": "parenthetical"})
                p.text = self.RE_PARENTHETICAL.sub(r'\1', line)
                spoken_words = None
            else:
                if spoken_words is None:
                    spoken_words = etree.SubElement(dialog, "p", {"class": "spoken-words"})
                    spoken_words.text = line.strip()
                else:
                    br = etree.SubElement(spoken_words, "br")
                    br.tail = line.strip()
        return dialog


class TransitionBlockProcessor(BlockProcessor):
    RE_DEFAULT = re.compile(r'^\s*([[:upper:]]{1}[^[:lower:]]+?\s+TO:)\s*$', flags=re.UNICODE | re.MULTILINE)
    RE_FORCED = re.compile(r'^\s*>\s*(.+)\s*[^<]\s*$', flags=re.MULTILINE)

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
            p.set("class", "transition")
            p.text = character


class NotesInlineProcessor(InlineProcessor):

    def __init__(self):
        super().__init__(r'(\[\[.+\]\])')

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | str | None, int | None, int | None]:
        note = etree.Element("span", {"class": "note"})
        note.text = m.group(1)
        return note, m.start(1), m.end(1)


class EmphasisInlineProcessor(InlineProcessor):
    """
        *italics*
        **bold**
        ***bold italics***
        _underline_
    """

    def __init__(self):
        """
        Create an instant of an simple tag processor.

        Arguments:
            pattern: A regular expression that matches a pattern.
            tag: Tag of element.

        """
        InlineProcessor.__init__(self, r'(?<!/)(\*\*\*|\*\*|\*|\_)((\s*[^*_\s]+)+\s*)(\1)')
        self.compiled_re = re.compile(self.pattern, flags=re.DOTALL | re.UNICODE | re.MULTILINE)
        self.tags = {"*": ["em"], "**": ["strong"], "***": ["strong", "em"], "_": ["u"]}
        """ The tag of the rendered element. """

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element, int, int]:  # pragma: no cover
        """
        Return [`Element`][xml.etree.ElementTree.Element] of type `tag` with the string in `group(2)` of a
        matching pattern as the Element's text.
        """
        emphasis = m.group(1)
        outer_el = etree.Element(self.tags[emphasis][0])
        el = outer_el
        for i in range(1, len(self.tags[emphasis])):
            el = etree.SubElement(el, self.tags[emphasis][i])
        el.text = m.group(2)
        return outer_el, m.start(0), m.end(0)


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
        md.preprocessors.register(BlockContinuationPreprocessor(md),
                                  "fountain-block-continuation-pre", base_priority)
        # md.preprocessors.register(BlockContinuationPreprocessor(md), 'fountain-block-containuation', base_priority)

        block_proc_reg = md.parser.blockprocessors.register

        # md.parser.blockprocessors.register(DialogBlockProcessor(md.parser), "fountain-dialog", base_priority - 100)

        # block_proc_reg(HashHeaderProcessor(md.parser), 'hashheader', base_priority - 20)

        block_proc_reg(TitlePageBlockProcessor(md.parser), "fountain-title-page", base_priority + 20)
        block_proc_reg(SceneHeadingBlockProcessor(md.parser), "fountain-scene-heading", base_priority)
        block_proc_reg(SynopsesBlockProcessor(md.parser), "fountain-synopses", base_priority)
        block_proc_reg(CenteredTextBlockProcessor(md.parser), 'fountain-centered-text', base_priority)
        block_proc_reg(LyricsBlockProcessor(md.parser), 'fountain-lyrics', base_priority)
        block_proc_reg(PageBreakBlockProcessor(md.parser), "fountaint-page-break", base_priority)
        block_proc_reg(TransitionBlockProcessor(md.parser), "fountain-transition", base_priority)
        block_proc_reg(DialogueBlockProcessor(md.parser), "fountain-dialogue", base_priority - 5)
        # block_proc_reg(ParentheticalBlockProcessor(md.parser), "fountain-parenthetical", base_priority - 10)
        block_proc_reg(ActionBlockProcessor(md.parser), "fountain-action", base_priority - 20)

        inline_proc_reg = md.inlinePatterns.register
        inline_proc_reg(EmphasisInlineProcessor(), "fountain-emphasis", base_priority)
        inline_proc_reg(NotesInlineProcessor(), "fountain-notes", base_priority)
        # inline_proc_reg(BlockContinuationNthInlineProcessor(), "fountain-block-continuation-nth", base_priority + 10)
        # inline_proc_reg(BlockContinuationExtraInlineProcessor(), "fountain-block-continuation-extra", base_priority + 5)
        # inline_proc_reg(BlockContinuationFirstInlineProcessor(), "fountain-block-continuation-first", base_priority)

        tree_reg = md.treeprocessors.register
        tree_reg(WrapperTreeProcessor(md), 'fountain-wrapper', base_priority)
        tree_reg(CharacterListTreeProcessor(md, self.getConfigs()), 'fountain-character-list', base_priority)
        tree_reg(LineBreaksTreeProcessor(md), 'fountain-line-breaks', base_priority - 50)

        md.postprocessors.register(BlockContinuationPostprocessor(md), "fountain-block-continuation-post",
                                   base_priority)


def makeExtension(**kwargs):
    return FountainMarkdownExtension(**kwargs)


def parse(text: str, **kwargs) -> str:
    return markdown(text, extensions=[FountainMarkdownExtension(**kwargs)])
