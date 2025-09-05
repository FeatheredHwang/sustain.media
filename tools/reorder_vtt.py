from pathlib import Path
import dialog


def reorder_vtt(input_path: str, output_path: str) -> None:
    """
    Reorder subtitle numbering in a VTT file sequentially.

    Args:
        input_path (str): Path to the original .vtt file.
        output_path (str): Path to save the corrected .vtt file.
    """
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = []
    counter = 1
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Keep WEBVTT header untouched
        if i == 0 and line.upper() == "WEBVTT":
            output_lines.append(lines[i])
            i += 1
            continue

        # Cue number: replace with new number
        if line.isdigit():
            output_lines.append(f'{counter}\n')
            counter += 1
        else:
            output_lines.append(lines[i])

        i += 1

    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)


if __name__ == '__main__':
    subs_dir = Path(__file__).parent.parent / "data" / "subtitle"
    input_path = dialog.select_file(ext="vtt", initialdir=subs_dir)
    output_path = input_path.with_name(f"{input_path.stem}_reordered.vtt")
    reorder_vtt(str(input_path), str(output_path))
