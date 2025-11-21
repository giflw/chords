# import  html escape to be able to properly view assert error diff in html report
import logging
from html import escape as html_escape

import pytest

import src.chords.text_formatting as parser
import utils
from src.chords.text_formatting import CharToTagInlineProcessor

group = utils.get_group_from_test_file_path(__file__)
# sources = ["code.md", "mode-single.md"]
sources = utils.list_source_files(group)


def test_processor_mode_unknown():
    with pytest.raises(ValueError):
        CharToTagInlineProcessor.of("tag", "c", "foo")


@pytest.mark.parametrize("source_path", sources, ids=lambda n: n.split(".")[0].upper())
def test_text_formatting(source_path):
    source, html = utils.read_source_and_html(group, source_path)

    if source.startswith("options:"):
        source = source.split("\n", 1)
        options = source[0]
        source = source[1]
        options = eval(options.split(":", 1)[1])
    else:
        options = {}
    logging.info(f"Options: {options}")
    parsed = parser.parse(source, **options)
    logging.info(f"Parsed: [{parsed}]")
    assert html_escape(parsed.strip()) == html_escape(html.strip())
