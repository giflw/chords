import re
import json
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class VexTabPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        r'^`{3,}[ ]*vextab[ ]*\n(.*?)^`{3,}[ ]*$',
        re.MULTILINE | re.DOTALL
    )

    def __init__(self, md):
        super().__init__(md)
        self.counter = 0

    def run(self, lines):
        text = "\n".join(lines)

        def replace(match):
            return self.render_vextab(match.group(1))

        return self.FENCED_BLOCK_RE.sub(replace, text).split('\n')

    def render_vextab(self, content):
        self.counter += 1
        container_id = f'vextab-{self.counter}'
        html.append('<script>')
        html.append('(function(){')
        html.append('  const src = ' + js_code + ';')
        html.append(f'  const target = document.getElementById("{container_id}");')
        html.append('  function loadScript(url){')
        html.append('    return new Promise(function(resolve, reject){')
        html.append('      var s = document.createElement("script");')
        html.append('      s.src = url;')
        html.append('      s.onload = resolve;')
        html.append('      s.onerror = reject;')
        html.append('      document.head.appendChild(s);')
        html.append('    });')
        html.append('  }')
        html.append('  function render(){')
        html.append('    try{')
        html.append('      if(typeof vextab === "undefined" || typeof vextab.Div === "undefined"){')
        html.append('        throw new Error("VexTab not loaded");')
        html.append('      }')
        html.append('      // Use VexTab auto-renderer')
        html.append('      var div = document.createElement("div");')
        html.append('      div.className = "vextab-auto";')
        html.append('      div.innerText = src;')
        html.append('      target.appendChild(div);')
        html.append('      vextab.Div.renderAll();')
        html.append('    } catch(e){')
        html.append('      console.error(e);')
        html.append('      target.innerText = src;')
        html.append('    }')
        html.append('  }')
        html.append('  function init(){')
        html.append('    if (typeof vextab === "undefined" || typeof vextab.Div === "undefined") {')
        html.append('      loadScript("/assets/chordsmd/vendor/vextab.min.js").then(render).catch(function(err){')
        html.append('        console.error("Failed to load VexTab vendor file:", err);')
        html.append('        target.innerText = src;')
        html.append('      });')
        html.append('    } else {')
        html.append('      render();')
        html.append('    }')
        html.append('  }')
        html.append('  if (document.readyState === "loading") {')
        html.append('    document.addEventListener("DOMContentLoaded", init);')
        html.append('  } else {')
        html.append('    init();')
        html.append('  }')
        html.append('})();')
        html.append('</script>')
        html.append('</div>')

        return "\n".join(html)


class VexTabExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(VexTabPreprocessor(md), 'vextab_block', 30)


def makeExtension(**kwargs):
    return VexTabExtension(**kwargs)
