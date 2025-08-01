def renumber_vtt(input_path: str, output_path: str) -> None:
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = []
    counter = 1
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip headers and comments
        if line.startswith('WEBVTT') or line.startswith('NOTE') or '-->' in line or line == '':
            output_lines.append(lines[i])
            i += 1
            continue

        # Cue number: replace with new number
        if line.isdigit():
            output_lines.append(f'{counter}\n')
            counter += 1
            i += 1
        else:
            output_lines.append(lines[i])
            i += 1

    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)


# Example usage
renumber_vtt('input.vtt', 'output.vtt')