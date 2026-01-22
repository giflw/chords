from markdown.extensions import Extension
from .chordsheet import ChordSheetExtension
from .chordpro import ChordProExtension
from .tabs import TabExtension
from .abc import AbcExtension

class ChordsMDExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'enable_chords': [True, 'Enable chord sheets (```chords)'],
            'enable_tabs': [True, 'Enable tablature (```tab)'],
            'enable_abc': [True, 'Enable ABC notation (```abc)'],
            'enable_chordpro': [True, 'Enable ChordPro (```chordpro)'],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        if self.getConfig('enable_chords'):
            ChordSheetExtension().extendMarkdown(md)
        if self.getConfig('enable_tabs'):
            TabExtension().extendMarkdown(md)
        if self.getConfig('enable_abc'):
            AbcExtension().extendMarkdown(md)
        if self.getConfig('enable_chordpro'):
            ChordProExtension().extendMarkdown(md)

# Alias for backward compatibility if needed
MyExtension = ChordSheetExtension

def makeExtension(**kwargs):
    return ChordsMDExtension(**kwargs)
