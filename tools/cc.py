import re
from pathlib import Path

from opencc import OpenCC

import dialog


def translate_cc(input_path: Path, output_path: Path, config: str = 's2t') -> None:
    """
    Convert a text file between Traditional Chinese and Simplified Chinese using OpenCC.

    Args:
        input_path (Path): Path to the Original Chinese input file.
        output_path (Path): Path to save the translated Chinese output file.
        config (str): Use either 't2s' or 's2t': 't2s' means Traditional-to-Simplified, and 's2t' means the reverse.
    """
    if not config:
        print('')
        return
    if not config in {"t2s", "s2t"}:
        raise ValueError(f"Invalid word: {config}. Must be either 't2s' or 's2t'.")
    cc = OpenCC(config)
    with open(input_path, 'r', encoding='utf-8') as infile, \
            open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            simplified_line = cc.convert(line)
            outfile.write(simplified_line)


if __name__ == "__main__":
    subs_dir = Path(__file__).parent.parent / "data" / "subtitle"
    og_path = dialog.select_file(initialdir=subs_dir)
    lang_pattern = re.compile(r"\((?P<lang>[a-z]{2}(?:-[a-z]{2})*)\)(?=\.[^.]+$)", re.IGNORECASE)
    match = lang_pattern.search(og_path.name)
    flag = ''
    tr_path = og_path.parent / "__pycache__"
    if not match:
        print("Language Code not found, exit the program.")
        exit()
    elif match.group('lang') in {'zh-cn', 'zh-sg'}:
        flag = 's2t'
        tr_path = tr_path / lang_pattern.sub('(zh-tw)', og_path.name)
    elif match.group('lang') in {'zh-tw', 'zh-hk'}:
        flag = 't2s'
        tr_path = tr_path / lang_pattern.sub('(zh-cn)', og_path.name)
    else:
        print("The language code is not Chinese, exit the program.")
        exit()

    translate_cc(input_path=og_path, output_path=tr_path, config=flag)
    print(f"✅ Translated file using '{flag}', output as: {tr_path}")
