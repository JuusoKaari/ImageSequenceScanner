# ImageSequenceScanner

**ImageSequenceScanner** is a lightweight Python-based tool for visualizing and sanity-checking 3D render image sequences before compositing. It helps identify missing or broken frames, unusually small files, and other render inconsistencies—before you commit time in Nuke, After Effects, or Fusion.

---

## 🔍 What It Does

- Scans a given folder structure recursively
- Detects all image sequences (e.g., `basename.####.exr`)
- Calculates the in/out frame range for each sequence
- Flags:
  - Missing frames
  - Suspiciously small files (possible broken renders)
  - Inconsistent render passes
- Visualizes this info in a clear, scrollable, and lightweight GUI timeline

---

## 🧩 Implementation

### Core
- **Python 3.9+**
- File system scanning with `os`, `glob`, `re`, and `pathlib`
- Data structures to store:
  - Sequence base name
  - Frame numbers present
  - File sizes
  - Flags (missing, small, etc.)

### GUI
- **PySide6** – for cross-platform native GUI
  - Timeline-style visualizations
  - Color-coded indicators (green = good, red = missing, yellow = small)
  - Scrollable layout for viewing multiple passes
  - Tooltips on hover (file size, frame number, status)
  - Frame click-to-open functionality
  - Folder picker dialog to select render directories

---

## 📂 Project Structure

```
ImageSequenceScanner/
├── image_sequence_scanner/     # Main package
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # Entry point for module execution
│   ├── scanner.py              # Core file scanning functionality
│   ├── gui.py                  # Main window and application logic
│   └── timeline_widget.py      # Timeline visualization widget
├── tests/                      # Test directory
│   ├── __init__.py
│   └── test_scanner.py         # Tests for scanner module
├── run_scanner.py              # Convenience script to run the app
├── setup.py                    # Package installation
├── requirements.txt            # Dependencies
├── INSTALL.md                  # Installation and usage guide
├── README.md                   # This file
└── .gitignore                  # Git ignore file
```

---

## 🚀 Getting Started

See [INSTALL.md](INSTALL.md) for detailed installation and usage instructions.
