import os
import shutil
import sys

import markdown

from src.giflwmd.chordsmd import ChordsMarkdownExtension
from src.giflwmd.extras import ExtrasMarkdownExtension
from src.giflwmd.fountain import FountainMarkdownExtension
from src.giflwmd.mkcomments import CommentsExtension
from src.giflwmd.text_formatting import TextFormattingMarkdownExtension

MODES = {
    "chords": ChordsMarkdownExtension(),
    "text_formating": TextFormattingMarkdownExtension(),
    "comments": CommentsExtension(),
    "fountain": FountainMarkdownExtension(),
    "extras": ExtrasMarkdownExtension()
}

# to clear dist: shutil.rmtree(dist)

mode = sys.argv[1]
files = sys.argv[2:]

if not files:
    files = ["screenplay.fountain"]

extension = MODES[mode]


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

    for asset in ["normalize.css", "fountain.css"]:
        shutil.copy(os.path.join(TEMPLATES_DIR, asset), os.path.join(BUILD_DIR, asset))

    with open(os.path.join(os.path.dirname(__file__), "templates", f"{mode}.html"), "r") as file:
        template = file.read()
    return template


if files:
    template = prepare_build()
    
    shutil.copytree(ASSETS_DIR, BUILD_DIR, dirs_exist_ok=True)

    for file in files:
        with open(file, 'r', encoding="utf-8") as input:
            html = markdown.markdown(
                input.read(),
                extensions=[extension]
            )
            out_file = os.path.join(BUILD_DIR, file.replace(".fountain", ".html"))
            with open(out_file, 'w', encoding="utf-8") as output:
                output.write(template % html)
                print(f"Done processing {file} to {output.name}")
else:
    print("No files provided")
