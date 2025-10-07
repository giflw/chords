import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class NoRender(Preprocessor):
    """ Skip any line with words 'NO RENDER' in it. """

    def run(self, lines):
        new_lines = []
        for line in lines:
            m = re.search("NO RENDER", line)
            if not m:
                # any line without NO RENDER is passed through
                new_lines.append(line)
        return new_lines


class MyExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'option1': ['value1', 'description1'],
            'option2': ['value2', 'description2']
        }
        super(MyExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.preprocessors.register(NoRender(md), 'norender', 175)

def makeExtension(**kwargs):
    return MyExtension(**kwargs)
