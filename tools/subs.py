import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
import shutil

import dialog


def parse_timestamp(ts: str) -> timedelta:
    """Convert a VTT timestamp (HH:MM:SS.mmm) into a timedelta object."""
    h, m, s, ms = re.split(r'[:.]', ts)
    return timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))


def format_timestamp(td: timedelta) -> str:
    """Format timedelta back into SRT timestamp (HH:MM:SS,mmm)."""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def vtt_chk(og_path: str) -> None:
    """
    Convert a WebVTT file into SRT format.
    Adjust start time if it equals the previous end time.
    """
    # ######################################################################################## #
    # Create a timestamped backup copy of a file.
    _og_path = Path(og_path)
    backup_folder = _og_path.parent / "__pycache__"
    backup_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{_og_path.stem}_backup_{timestamp}{_og_path.suffix}"
    backup_path = backup_folder / backup_name

    shutil.copy2(_og_path, backup_path)
    print(f"VTT file backup-ed: {backup_path}")

    # ######################################################################################## #
    # Fix subtitle timestamp offset caused by Aegisub, and
    # reorder subtitle numbering in a VTT file sequentially.
    with open(og_path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    chk_lines = []
    prev_end = None
    counter = 0
    i = 0

    # Keep WEBVTT header untouched
    if lines[0].upper() == "WEBVTT":
        chk_lines.append(lines[i])
        i += 1

    while i < len(lines):
        line = lines[i].strip()

        if "-->" in line:  # timestamp line
            counter += 1

            start, end = [t.strip() for t in line.split("-->")]
            # Parse into timedelta
            start_td = parse_timestamp(start)
            end_td = parse_timestamp(end)

            # Fix subtitle timestamp offset caused by Aegisub (less than 0.01 s)
            if prev_end and start_td < prev_end:
                if (prev_end - start_td).total_seconds() < 0.02:
                    start_td = prev_end
                else:
                    print(f"Timeline chaos WARNING at counter {Counter}, {start}")

            prev_end = end_td

            # Write counter and timestamps
            chk_lines.append(str(counter) + "\n")
            chk_lines.append(f"{format_timestamp(start_td)} --> {format_timestamp(end_td)}\n".replace(',', '.'))
        # skip counter line
        elif line and not line.isdigit():
            chk_lines.append(line + "\n")
        elif line == "" and counter > 0:
            chk_lines.append("\n")

        i += 1

    output_path = _og_path.with_name(f"{_og_path.stem}_checked.vtt")
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.writelines(chk_lines)


    # ######################################################################################## #
    # Convert the WebVTT content into SRT format.

    lines = chk_lines

    # Remove "WEBVTT" header if it exists
    if lines and lines[0].strip().startswith("WEBVTT"):
        lines = lines[1:]

    srt_lines = []
    prev_end = None
    counter = 0
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if "-->" in line:  # timestamp line
            start, end = [t.strip() for t in line.split("-->")]

            # Parse into timedelta
            start_td = parse_timestamp(start)
            end_td = parse_timestamp(end)

            # Resolve overlapping timestamps that are valid in VTT but causes disorder in SRT
            if prev_end and start_td == prev_end:
                start_td += timedelta(milliseconds=1)

            prev_end = end_td

            # Write counter and timestamps
            counter += 1
            srt_lines.append(str(counter) + "\n")
            srt_lines.append(f"{format_timestamp(start_td)} --> {format_timestamp(end_td)}\n")
        # skip counter line
        elif line and not line.isdigit():
            srt_lines.append(line + "\n")
        elif line == "" and counter > 0:
            srt_lines.append("\n")

        i += 1

    output_path = _og_path.with_name(f"{_og_path.stem}.srt")
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.writelines(srt_lines)
    
    print(f"SRT file generated: {output_path}")



# Example usage
if __name__ == "__main__":
    subs_dir = Path(__file__).parent.parent / "data" / "subtitle"
    vtt_path = Path(dialog.select_file(ext="vtt", initialdir=subs_dir))
    vtt_chk(str(vtt_path))
