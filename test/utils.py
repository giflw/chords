import glob
import os
from types import MappingProxyType

from html import escape as html_escape


def get_group_from_test_file_path(test_file_path) -> str:
    return os.path.splitext(os.path.split(test_file_path)[1])[0].split("test_")[1]


def list_source_files(group, ext) -> list[str]:
    files = glob.glob(os.path.join("test", group, "*.*"))
    return [
        os.path.basename(file)
        for file in files
        if file.endswith(ext)
    ]


def dict2css(style: dict[str, dict[str, str | int | bool]] = MappingProxyType({})):
    style_str = ""
    for k, v in style.items():
        values = [f"    {ik}: {iv};\n" for ik, iv in v.items()]
        style_str += f"{k} {{\n{"".join(values)}}}\n"
    return style_str

SPLIT_TEXT = "\n---\n"
def read_test_sources(group, source_path, parser, style: str = "") -> tuple[str, str, dict, str]:

    source_path = os.path.join("test", group, source_path)
    with open(source_path, "r", encoding="utf-8") as file:
        source = file.read()

    split_source = source.split(SPLIT_TEXT)


    expected = split_source[-1]
    source = SPLIT_TEXT.join(split_source[:-1])

    if source.startswith("options:"):
        source = source.split("\n", 1)
        options = source[0]
        source = source[1]
        options = eval(options.split(":", 1)[1])
    else:
        options = {}

    # logging.info(f"Options: {options}")
    parsed = parser.parse(source, **options)

    # html_gen = os.path.splitext(source_path)[0] + ".generated.expected"
    # with open(html_gen, "w", encoding="utf-8") as file:
    #     file.write(parsed)
    # logging.info(f"Parsed: [{parsed}]")

    print(f"""<style>{style}</style>
    <table style="width: 100%; border: 1px solid darkgray; border-collapse: collapse">
        <thead>
        <tr style="border: 1px solid darkgray;">
            <th style="border: 1px solid darkgray;">Source</th>
            <th style="border: 1px solid darkgray;">Parsed</th>
            <th style="border: 1px solid darkgray;">Expected</th>
        </tr>
        </thead>
        <tbody>
        <tr style="border: 1px solid darkgray;">
            <td style="border: 1px solid darkgray;">{source}</td>
            <td style="border: 1px solid darkgray;">{html_escape(parsed)}</td>
            <td style="border: 1px solid darkgray;">{html_escape(expected)}</td>
        </tr>
        </tbody>
    </table>""")

    return source, expected, options, parsed
