from markdown.extensions import Extension
from .chordsheet import ChordSheetExtension
from .chordpro import ChordProExtension
from .tabs import TabExtension
from .abc import AbcExtension

class ChordsMDExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'chords': [True, 'Enable chord sheets (```chords)'],
            'tabs': [True, 'Enable tablature (```tab)'],
            'abc': [True, 'Enable ABC notation (```abc)'],
            'chordpro': [True, 'Enable ChordPro (```chordpro)'],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        if self.getConfig('chords'):
            ChordSheetExtension().extendMarkdown(md)
        if self.getConfig('tabs'):
            TabExtension().extendMarkdown(md)
        if self.getConfig('abc'):
            AbcExtension().extendMarkdown(md)
        if self.getConfig('chordpro'):
            ChordProExtension().extendMarkdown(md)

# Alias for backward compatibility if needed
MyExtension = ChordSheetExtension

def makeExtension(**kwargs):
    return ChordsMDExtension(**kwargs)
