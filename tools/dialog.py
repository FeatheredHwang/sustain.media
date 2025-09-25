import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path


def select_file(ext: str = None, initialdir: Path = None) -> Path | None:
    """
    Open a dialog to select a VTT file and save the corrected version.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    title = f"Select a file"
    filetypes = [("All files", "*.*")]
    if not ext:
        pass
    elif ext and len(ext) > 2:
        if ext.startswith('.'):
            ext = ext[1:]
        title = f"Select a {ext.upper()} file"
        filetypes.insert(0, (f"{ext.upper()}", f".{ext}"))
    else:
        print("Invalid file extension!")
        return None
    file_path = filedialog.askopenfilename(title=title, initialdir=initialdir, filetypes=filetypes)

    if not file_path:
        print("No file selected.")
        return None

    input_path = Path(file_path)
    print(f"✅ Selected file: {input_path}")
    return input_path


def show_warning(msg: str):
    messagebox.showwarning("Warning", "msg")
    print(f"❕Warning: {msg}")


# def ask_choice():
#     answer = messagebox.askquestion("Choose", "Do you want A or B?")