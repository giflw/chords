import pytest

import src.chords.text_formatting as parser
import utils

group = utils.get_group_from_test_file_path(__file__)


@pytest.mark.parametrize("source_path", utils.list_source_files(group), ids=lambda n: n.split(".")[0].upper())
def test_text_formatting(source_path):
    # logger.info(f"Source path: {source_path}")
    source, html = utils.read_source_and_html(group, source_path)
    assert parser.parse(source) == html
