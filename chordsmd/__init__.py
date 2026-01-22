from markdown.extensions import Extension
from .chordsheet import ChordSheetExtension
from .chordpro import ChordProExtension
from .tabs import TabExtension
from .abc import AbcExtension
from .fountain import FountainExtension
from .strumming import StrummingExtension
from .diagrams import ChordDiagramExtension
from .asciidoc import AsciidocExtension

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
            'asciidoc': [True, 'Enable AsciiDoc-like formatting'],
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
        if self.getConfig('asciidoc'):
            AsciidocExtension().extendMarkdown(md)

# Alias for backward compatibility if needed
MyExtension = ChordSheetExtension

def makeExtension(**kwargs):
    return ChordsMDExtension(**kwargs)

# MkDocs Plugin Support
try:
    from mkdocs.plugins import BasePlugin
    import os
    import shutil
    try:
        from importlib import resources
    except ImportError:
        import importlib_resources as resources
    
    class ChordsMDPlugin(BasePlugin):
        """
        MkDocs plugin that automatically configures ChordsMD extension
        and injects required CSS/JS assets.
        """
        def on_config(self, config, **kwargs):
            # 1. Register ChordsMD as a markdown extension if not already there
            if 'chordsmd' not in config['markdown_extensions']:
                config['markdown_extensions'].append('chordsmd')
            
            # 2. Add custom CSS (relative to site root)
            css_path = 'assets/chordsmd/style/style.css'
            if css_path not in config['extra_css']:
                config['extra_css'].append(css_path)
            
            # 3. Add custom JavaScript (relative to site root)
            js_paths = [
                'assets/chordsmd/vendor/svguitar.umd.js',
                'assets/chordsmd/vendor/abcjs-basic-min.js'
            ]
            for js in js_paths:
                if js not in config['extra_javascript']:
                    config['extra_javascript'].append(js)
            
            return config

        def on_post_build(self, config, **kwargs):
            """
            Copy assets from the package to the site directory.
            """
            site_dir = config['site_dir']
            dest_dir = os.path.join(site_dir, 'assets', 'chordsmd')
            
            # Get asset path from package
            try:
                # For Python 3.9+
                pkg_asset_path = resources.files('chordsmd') / 'assets'
                if os.path.exists(dest_dir):
                    shutil.rmtree(dest_dir)
                shutil.copytree(str(pkg_asset_path), dest_dir)
            except Exception:
                # Fallback for older Python or if files() isn't available
                with resources.path('chordsmd', 'assets') as p:
                    if os.path.exists(dest_dir):
                        shutil.rmtree(dest_dir)
                    shutil.copytree(str(p), dest_dir)
except ImportError:
    # MkDocs not installed, plugin support disabled
    class ChordsMDPlugin:
        pass
