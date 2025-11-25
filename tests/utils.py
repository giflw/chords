import glob
import logging
import os
from types import MappingProxyType


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


def dict2css(style: dict[str, dict[str, str | int | bool]] = MappingProxyType({})):
    style_str = ""
    for k, v in style.items():
        values = [f"    {ik}: {iv};\n" for ik, iv in v.items()]
        style_str += f"{k} {{\n{"".join(values)}}}\n"
    return style_str


def read_source_and_html(group, source_path, parser, style: str = "") -> tuple[str, str, dict, str]:
    source_path = os.path.join("tests", group, source_path)
    with open(source_path, "r", encoding="utf-8") as file:
        source = file.read()

    html = os.path.splitext(source_path)[0] + ".html"
    with open(html, "r", encoding="utf-8") as file:
        html = file.read()

    if source.startswith("options:"):
        source = source.split("\n", 1)
        options = source[0]
        source = source[1]
        options = eval(options.split(":", 1)[1])
    else:
        options = {}

    logging.info(f"Options: {options}")
    parsed = parser.parse(source, **options)

    html_gen = os.path.splitext(source_path)[0] + ".generated.html"
    with open(html_gen, "w", encoding="utf-8") as file:
        file.write(parsed)
    # logging.info(f"Parsed: [{parsed}]")

    print(f"""<style>{style}</style>
    <table style="width: 100%; border: 1px solid darkgray; border-collapse: collapse">
        <thead>
        <tr style="border: 1px solid darkgray;">
            <th style="border: 1px solid darkgray;">Source</th>
            <th style="border: 1px solid darkgray;">Parsed</th>
        </tr>
        </thead>
        <tbody>
        <tr style="border: 1px solid darkgray;">
            <td style="border: 1px solid darkgray;">{source}</td>
            <td style="border: 1px solid darkgray;">{parsed}</td>
        </tr>
        </tbody>
    </table>""")

    return source, html, options, parsed
