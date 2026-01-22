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
    from mkdocs.structure.files import File
    import os
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
                'assets/chordsmd/vendor/abcjs-basic-min.js',
                'assets/chordsmd/js/transposer.js' # Adding this too for documentation interaction
            ]
            for js in js_paths:
                if js not in config['extra_javascript']:
                    config['extra_javascript'].append(js)
            
            return config

        def on_files(self, files, config, **kwargs):
            """
            Add assets from the package to the MkDocs files collection.
            """
            try:
                # For Python 3.9+
                pkg_asset_root = resources.files('chordsmd') / 'assets'
                
                # Recursively add files
                def add_files_from_package(path, subpath=""):
                    for entry in path.iterdir():
                        rel_path = os.path.join(subpath, entry.name)
                        if entry.is_dir():
                            add_files_from_package(entry, rel_path)
                        else:
                            # Create a File object that MkDocs understands
                            # The 'src_uri' is the physical path on disk
                            # The 'dest_uri' is where it should go in 'site/'
                            # 'use_directory_urls' is usually from config
                            mkdocs_file = File(
                                path=os.path.join('assets', 'chordsmd', rel_path),
                                src_dir=str(path),
                                dest_dir=config['site_dir'],
                                use_directory_urls=config['use_directory_urls']
                            )
                            # Manually set the source path since File constructor expects it relative to src_dir
                            mkdocs_file.abs_src_path = str(entry)
                            files.append(mkdocs_file)

                add_files_from_package(pkg_asset_root)
            except Exception as e:
                # Fallback or error logging could go here
                print(f"Error injecting ChordsMD assets: {e}")
            
            return files

except ImportError:
    # MkDocs not installed, plugin support disabled
    class ChordsMDPlugin:
        pass
