# import  html escape to be able to properly view assert error diff in html report
from html import escape as html_escape

import pytest

import src.chords.text_formatting as parser
import utils

group = utils.get_group_from_test_file_path(__file__)
# sources = ["code.md", "mode-single.md"]
sources = utils.list_source_files(group)


@pytest.mark.parametrize("source_path", sources, ids=lambda n: n.split(".")[0].upper())
@pytest.mark.text_formating
def test_text_formatting(source_path):
    source, html, options, parsed = utils.read_source_and_html(group, source_path, parser)

    assert html_escape(parsed.strip()) == html_escape(html.strip())
