from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re
from xml.sax.saxutils import escape

class AbcPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*abc[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

    def run(self, lines):
        text = "\n".join(lines)
        def replace(match):
            return self.render_abc_block(match.group(1))
        return self.FENCED_BLOCK_RE.sub(replace, text).split('\n')

    def render_abc_block(self, abc_content):
        # We need a unique ID for each block to initialize abcjs
        # Simple hash or count?
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        
        # HTML structure
        # Hidden (or visible but raw) source?
        # Usually we just put content in JS call.
        
        escaped_content = abc_content.strip().replace('`', '\\`').replace('$', '\\$').replace('\n', '\\n')
        
        # We return a div placeholder and a script tag
        html = f"""
<div class="abc-container">
    <div id="score-{unique_id}" class="abc-score"></div>
    <div id="midi-{unique_id}" class="abc-midi"></div>
    <script>
    (function() {{
        var abc = `{escaped_content}`;
        if (typeof ABCJS !== 'undefined') {{
            ABCJS.renderAbc("score-{unique_id}", abc, {{ responsive: "resize" }});
            ABCJS.renderMidi("midi-{unique_id}", abc, {{}});
        }} else {{
            console.warn("ABCJS not loaded");
        }}
    }})();
    </script>
</div>
"""
        return html

class AbcExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(AbcPreprocessor(md), 'abc_block', 33)

def makeExtension(**kwargs):
    return AbcExtension(**kwargs)
