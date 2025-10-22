# test_main.py
import src.chords.fountain as f

with open("tests/test_fountain.fountain", "r") as file:
    text = file.read()

with open("tests/test_fountain.html", "r") as file:
    html = file.read()

# def test_the_last_birthday_card():
#     with open("res/fountain/The-Last-Birthday-Card.fountain", 'r') as source:
#         with open("res/fountain/The-Last-Birthday-Card.expected.html", 'r') as target:
#             assert f.parse(source.read()).strip() == f.parse(target.read()).strip()


def test_basic_fountain():
    assert f.parse(text).strip() == html.strip()