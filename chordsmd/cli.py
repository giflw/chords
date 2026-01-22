import argparse
import sys
import markdown
import os
from chordsmd import ChordsMDExtension

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown/Text with ChordsMD extensions to HTML.')
    parser.add_argument('input', help='Input file (.md or .txt)')
    parser.add_argument('-o', '--output', help='Output HTML file (default: input_base.html)')
    
    # Extension switches
    parser.add_argument('--chords', action='store_true', default=True, help='Enable chords extension (default: True)')
    parser.add_argument('--no-chords', action='store_false', dest='chords')
    
    parser.add_argument('--tabs', action='store_true', default=True, help='Enable tabs extension (default: True)')
    parser.add_argument('--no-tabs', action='store_false', dest='tabs')
    
    parser.add_argument('--abc', action='store_true', default=True, help='Enable ABC extension (default: True)')
    parser.add_argument('--no-abc', action='store_false', dest='abc')
    
    parser.add_argument('--chordpro', action='store_true', default=True, help='Enable ChordPro extension (default: True)')
    parser.add_argument('--no-chordpro', action='store_false', dest='chordpro')
    
    parser.add_argument('--fountain', action='store_true', default=True, help='Enable Fountain extension (default: True)')
    parser.add_argument('--no-fountain', action='store_false', dest='fountain')
    
    parser.add_argument('--strumming', action='store_true', default=True, help='Enable strumming extension (default: True)')
    parser.add_argument('--no-strumming', action='store_false', dest='strumming')
    
    parser.add_argument('--diagrams', action='store_true', default=True, help='Enable diagrams extension (default: True)')
    parser.add_argument('--no-diagrams', action='store_false', dest='diagrams')
    
    parser.add_argument('--asciidoc', action='store_true', default=True, help='Enable AsciiDoc extension (default: True)')
    parser.add_argument('--no-asciidoc', action='store_false', dest='asciidoc')

    parser.add_argument('--standalone', action='store_true', help='Generate standalone HTML with boilerplate')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File {args.input} not found.")
        sys.exit(1)

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Configure extension
    ext = ChordsMDExtension(
        chords=args.chords,
        tabs=args.tabs,
        abc=args.abc,
        chordpro=args.chordpro,
        fountain=args.fountain,
        strumming=args.strumming,
        diagrams=args.diagrams,
        asciidoc=args.asciidoc
    )

    html_content = markdown.markdown(content, extensions=[ext])

    if args.standalone:
        # Wrap in boilerplate
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{os.path.basename(args.input)}</title>
    <link rel="stylesheet" href="chordsmd/assets/style/style.css">
    <script src="chordsmd/assets/vendor/svguitar.umd.js"></script>
    <script src="chordsmd/assets/vendor/abcjs-basic-min.js"></script>
    <script src="chordsmd/assets/js/transposer.js"></script>
    <script src="chordsmd/assets/js/column-layout.js"></script>
</head>
<body>
    <div class="content">
{html_content}
    </div>
</body>
</html>"""

    output_file = args.output if args.output else os.path.splitext(args.input)[0] + ".html"

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully converted {args.input} to {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
