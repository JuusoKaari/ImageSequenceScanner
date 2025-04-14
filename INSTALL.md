# Installation and Usage Guide

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Windows Quick Start

For Windows users, we provide two batch files for easy setup and running:

1. Run `setup_venv.bat` to create a virtual environment and install dependencies
2. Run `run_app.bat` to launch the application

That's it! The batch files will handle everything else for you.

### Manual Installation

If you prefer to set up manually or are using macOS/Linux:

1. Create and activate a virtual environment:
   ```bash
   # Create venv
   python -m venv venv

   # Activate venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install the package and dependencies:
   ```
   pip install -e .
   ```

   This will install the package in development mode, allowing you to make changes to the code without reinstalling.

### Usage

#### Running the Application

There are several ways to run the application:

1. **Using the run script**:
   ```
   python run_scanner.py
   ```

2. **Using the module**:
   ```
   python -m image_sequence_scanner
   ```

3. **Using the command-line entry point** (if installed with pip):
   ```
   image-sequence-scanner
   ```

#### Using the Application

1. Launch the application using one of the methods above.
2. Click the "Select Folder" button and navigate to a directory containing image sequences.
3. The application will scan the directory and display all detected sequences as timelines.
4. Each frame is color-coded:
   - Green: Normal frame
   - Red: Missing frame
   - Yellow: Suspiciously small frame (possibly corrupted)
5. Hover over frames to see details like file size and status.
6. Click on a frame to open it with your system's default application.

#### Running Tests

To run the test suite:

```
python -m unittest discover tests
```

## Troubleshooting

- **Missing PySide6**: If you get an error about PySide6 being missing, install it with `pip install PySide6`.
- **No sequences detected**: Ensure your files follow the pattern `name.####.extension` where #### represents the frame number.
- **Virtual environment issues**: If you have problems with the virtual environment:
  1. Delete the `venv` directory
  2. Run `setup_venv.bat` again (Windows) or recreate the environment manually 