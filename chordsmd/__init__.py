from markdown.extensions import Extension
from .chordsheet import ChordSheetExtension
from .chordpro import ChordProExtension
from .tabs import TabExtension
from .abc import AbcExtension
from .fountain import FountainExtension
from .strumming import StrummingExtension
from .diagrams import ChordDiagramExtension

class ChordsMDExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'chords': [True, 'Enable chord sheets (```chords)'],
            'tabs': [True, 'Enable tablature (```tab)'],
            'abc': [True, 'Enable ABC notation (```abc)'],
            'chordpro': [True, 'Enable ChordPro (```chordpro)'],
            'fountain': [True, 'Enable Fountain screenplay (```fountain)'],
            'strumming': [True, 'Enable strumming patterns (```strum)'],
            'diagrams': [True, 'Enable chord diagrams (```chord diagrams)'],
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
        if self.getConfig('fountain'):
            FountainExtension().extendMarkdown(md)
        if self.getConfig('strumming'):
            StrummingExtension().extendMarkdown(md)
        if self.getConfig('diagrams'):
            ChordDiagramExtension().extendMarkdown(md)

# Alias for backward compatibility if needed
MyExtension = ChordSheetExtension

def makeExtension(**kwargs):
    return ChordsMDExtension(**kwargs)
