import re

from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension


PREFIX_PLACEHOLDER = "OMtxTKldR2f1LZ5Q"


class CommentsExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(
            CommentMunger(md), "comment_munger", 175)
        md.preprocessors.register(
            CommentRemover(md), "comment_remover", 170)
        md.parser.blockprocessors.register(
            RawCommentReplacer(md.parser), "raw_comment_replacer", 180)


class CommentMunger(Preprocessor):
    def run(self, lines):
        return [re.sub(r'<!---', PREFIX_PLACEHOLDER, line) for line in lines]


class CommentRemover(Preprocessor):
    def run(self, lines):
        new_lines = []
        is_multi = False
        for line in lines:
            if not is_multi:
                new_line, is_multi = self._uncommenter(line)
            else:
                new_line, is_multi = self._unmultiliner(line)
            new_lines.append(new_line)
        return new_lines

    def _uncommenter(self, line):
        # inline
        line = re.sub(r'\s*' + PREFIX_PLACEHOLDER + r'.*?-->', '', line)

        # start multiline
        line, count = re.subn(r'\s*' + PREFIX_PLACEHOLDER + r'.*', '', line)

        return line, bool(count)

    def _unmultiliner(self, line):
        new_line, count = re.subn(r'.*?-->', '', line, count=1)

        # end multiline
        if count > 0:
            return self._uncommenter(new_line)

        # continue multiline
        else:
            return ('', True)


class RawCommentReplacer(BlockProcessor):
    def test(self, parent, block):
        return PREFIX_PLACEHOLDER in block

    def run(self, parent, blocks):
        #blocks[0] = re.sub(PREFIX_PLACEHOLDER, '<!---', blocks[0])
        pass
#class RawCommentReplacer(Postprocessor):
#    def run(self, text):
#        return re.sub(PREFIX_PLACEHOLDER, '<!---', text)


def makeExtension(*args, **kwargs):
    return CommentsExtension(*args, **kwargs)