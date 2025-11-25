# import  html escape to be able to properly view assert error diff in html report

from html import escape as html_escape

import pytest
from pygments.styles.dracula import background

import src.chords.fountain as parser
import utils

group = utils.get_group_from_test_file_path(__file__)
sources = None
# sources = ["line-breaks.fountain"]
if sources is None:
    sources = utils.list_source_files(group)

style = utils.dict2css({
    ".fountain .script": {
        "margin": "3px",
        "padding": "3px",
        "border": "1px solid green",
        "background": "ligthgrey"
    },
    ".fountain *": {
        "margin": 0,
        "padding": 0,
        "white-space": "normal !important"
    },
    ".fountain p": {
        "border": "red solid 1px",
        "padding": "3px"
    },
    "th, td": {
        "vertical-align": "top"
    },
    ".fountain > .script [class]": {
        "border": "solid blue 1px !important",
        "padding": "3px",
        "font-weight": "bold"
    }
})


@pytest.mark.parametrize("source_path", sources, ids=lambda n: n.split(".")[0].upper())
@pytest.mark.fountain
def test_fountain(source_path):
    source, html, options, parsed = utils.read_source_and_html(group, source_path, parser, style)

    assert html_escape(parsed.strip()) == html_escape(html.strip())
