# Icon Creatives Renamer

A tiny Tkinter app that batch-renames exported design assets to a clean, consistent format for delivery.

> **Input pattern → Output pattern**  
> `"<ratio> (<number>).<ext>"` → `"<company>_hook<number>_<ratio>.<ext>"`

Examples:
- `1x1 (1).jpg` → `acme_hook1_1x1.jpg`  
# Icon Creatives Renamer

A tiny Tkinter app that batch-renames exported design assets to a clean, consistent format for delivery.

Input pattern → Output pattern

  "<ratio> (<number>).<ext>" → "<company>_hook<number>_<ratio>.<ext>"

Examples:
 - `1x1 (1).jpg` → `acme_hook1_1x1.jpg`
 - `4x5 (2).png` → `acme_hook2_4x5.png`
 - `16x9 (10).jpeg` → `acme_hook10_16x9.jpeg`

---

## Features

 - Select a folder and auto-detect files matching `ratio (number).ext`
 - Set **Company Name** and a **Start Hook Number** (e.g., start from 101)
 - **Preview** the changes before renaming
 - **One-click Rename** with success/error log
 - Supports: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

---

## Quick Start

### Requirements

 - Python 3.8+
 - Tkinter (bundled with Python on Windows/macOS; on Linux you may need `sudo apt install python3-tk`)

### Run from source

```powershell
python design_renamer_gui.py
```

### Build a standalone Windows EXE

Python must be installed to run the `.py` directly. To create a distributable Windows EXE (so end users don't need Python), build with PyInstaller.

We've provided a small helper and guidance:

 - `requirements.txt` — lists `pyinstaller` needed for building
 - `build_exe.ps1` — PowerShell script that installs PyInstaller if missing and runs the build

Build steps (PowerShell):

```powershell
cd "d:\VS Code\Project\Icon-creatives-renamer"
# optional: create & activate venv
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
.\build_exe.ps1
```

After building, the EXE will be in `dist\` (e.g. `DesignRenamer-v0.1.0.exe`).

### Keep source and EXE synchronized

 - The authoritative source is `design_renamer_gui.py` — it contains the `__version__` constant printed in the About box.
 - When you change features or behavior, update `__version__` in `design_renamer_gui.py`, then re-run the build script to produce an EXE with matching version and behavior.
 - If you want programmatic parity checks, consider adding a `--version` CLI flag that prints `__version__` (the EXE will expose the same output when built).

---

## Filename Rules (important)

Input must match: `^([a-zA-Z0-9x]+)\s*\((\d+)\)\.(jpg|jpeg|png|gif|bmp)$`

Examples: `1x1 (1).jpg`, `4x5(2).png`, `16x9 (10).jpeg`

Output becomes: `<company>_hook<calculated-number>_<ratio>.<ext>` — where `<calculated-number>` = `Start Hook Number + (file's <number> - 1)`

---

## Troubleshooting

 - “No matching files found.” — Ensure filenames follow the input pattern exactly.
 - Linux: Tkinter not found — `sudo apt install python3-tk`
 - Accidentally renamed wrongly? — Restore from backups or re-export; the app doesn’t keep an undo list.

---

## Development notes

 - Single entry point: `design_renamer_gui.py`
 - Bump `__version__` inside that file on meaningful changes so the built EXE reports the correct version.

---

## License

MIT
