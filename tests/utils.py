import glob
import os


def get_group_from_test_file_path(test_file_path) -> str:
    return os.path.splitext(os.path.split(test_file_path)[1])[0].split("test_")[1]


def list_source_files(group) -> list[str]:
    files = glob.glob(os.path.join("tests", group, "*.*"))
    return [
        os.path.basename(file)
        for file in files
        if not file.endswith(".html")
           and not file.endswith(".sh")
           and not file.endswith("README.md")
    ]


def read_source_and_html(group, source_path) -> tuple[str, str]:
    source_path = os.path.join("tests", group, source_path)
    with open(source_path, "r", encoding="utf-8") as file:
        source = file.read()

    html = os.path.splitext(source_path)[0] + ".html"
    with open(html, "r", encoding="utf-8") as file:
        html = file.read()

    return source, html
