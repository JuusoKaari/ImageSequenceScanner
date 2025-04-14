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

## 🧩 Planned Tech Stack

### Core
- **Python 3.9+**
- File system scanning with `os`, `glob`, `re`, and possibly `pathlib`
- Basic data structure to store:
  - Sequence base name
  - Frame numbers present
  - File sizes
  - Flags (missing, small, etc.)

### GUI
- **PyQt or PySide** – for cross-platform native GUI
  - Timeline-style visualizations using `QGraphicsView` or `QTableView`
  - Color-coded indicators (green = good, red = missing, yellow = small)
  - Scrollable layout for viewing multiple passes
  - Optional tooltips on hover (file size, frame number, etc.)
  - Folder picker dialog to select render directories

---

## 🎯 MVP Milestones

1. **File Scanner Module**
   - Detect sequences using filename patterns
   - Map available frames per sequence
   - Flag missing or small-sized frames
   - Output diagnostic info as structured data

3. **GUI Prototype**
   - Select folder
   - Show sequences as timelines (rows)
   - Mark frame statuses with colors or symbols

4. **Interactivity & Polish**
   - Hover to inspect frame metadata
   - Click to open file in OS
   - Zoom/pan if needed
