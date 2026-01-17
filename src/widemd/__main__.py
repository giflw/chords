import os
import shutil
import sys

import markdown
from markdown.extensions.toc import TocExtension

from .chords import ChordsMarkdownExtension
from .extras import ExtrasMarkdownExtension
from .fountain import FountainMarkdownExtension
from .mkcomments import CommentsExtension
from .text_formatting import TextFormattingMarkdownExtension

MODES = {
    "chords": [TextFormattingMarkdownExtension(), ChordsMarkdownExtension()],
    "text_formating": [TextFormattingMarkdownExtension()],
    "comments": [CommentsExtension()],
    "fountain": ["extra", TocExtension(baselevel=1, toc_depth=3, anchorlink=True, permalink=True), FountainMarkdownExtension()],
    "extras": [ExtrasMarkdownExtension()]
}

# to clear dist: shutil.rmtree(dist)

mode = sys.argv[1]
files = sys.argv[2:]

extensions = MODES[mode]

# FIXME
# if not files:
#     files = [extension.default_file_name]



CWD_DIR = os.getcwd()
BUILD_DIR = os.path.join(os.getcwd(), "dist")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
ASSETS_DIR = os.path.join(CWD_DIR, "assets")


def prepare_build() -> str:
    try:
        if not os.path.exists(BUILD_DIR):
            os.mkdir(BUILD_DIR)
    except:
        raise

    for asset in ["normalize.css", "fountain-paged.css"]:
        shutil.copy(os.path.join(TEMPLATES_DIR, asset), os.path.join(BUILD_DIR, asset))

    with open(os.path.join(os.path.dirname(__file__), "templates", f"{mode}.html"), "r") as file:
        template = file.read()
    return template


if files:
    template = prepare_build()
    
    if os.path.exists(ASSETS_DIR):
        shutil.copytree(ASSETS_DIR, BUILD_DIR, dirs_exist_ok=True)

    for file in files:
        try:
            with open(file, 'r', encoding="utf-8") as input:
                html = markdown.markdown(
                    input.read(),
                    extensions=extensions
                )
                out_file = os.path.join(BUILD_DIR, file.replace(".fountain", ".html").replace(".md", ".html"))
                try:
                    print(os.path.dirname(out_file))
                    os.makedirs(os.path.dirname(out_file), exist_ok=True)
                    with open(out_file, 'w', encoding="utf-8") as output:
                        output.write(template % html)
                        print(f"Done processing {file} to {output.name}")
                except IOError as error:
                    print(f"Output file {out_file} not found!", error)
                    exit(2)
        except IOError as error:
            print(f"Input file {file} not found!", error)
            exit(1)
else:
    print("No files provided")
