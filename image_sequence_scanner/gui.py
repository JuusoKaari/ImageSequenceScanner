"""
GUI module for ImageSequenceScanner.

This module provides the graphical user interface for visualizing image sequences
and their frames in a timeline-like view.
"""

import os
import sys
from typing import Dict

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QScrollArea, QFrame
)

from .scanner import Scanner
from .timeline_widget import TimelineWidget


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        self.scanner = Scanner()
        self.sequences = {}
        self.analysis_results = {}
        
        self.setWindowTitle("Image Sequence Scanner")
        self.resize(1200, 800)  # Increased default window size
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)  # Reduce margins for better space usage
        main_layout.setSpacing(4)  # Reduce spacing between widgets
        
        # Top controls
        controls_layout = QHBoxLayout()
        self.folder_btn = QPushButton("Select Folder")
        self.folder_btn.clicked.connect(self._on_select_folder)
        controls_layout.addWidget(self.folder_btn)
        
        self.status_label = QLabel("Ready")
        controls_layout.addWidget(self.status_label, 1)
        
        main_layout.addLayout(controls_layout)
        
        # Timeline view with scroll area
        scroll_area = QScrollArea()
        scroll_area.setFrameStyle(QFrame.NoFrame)  # Remove frame border
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setMinimumHeight(400)  # Ensure reasonable minimum height
        
        # Create a container widget for the timeline
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.timeline_widget = TimelineWidget()
        self.timeline_widget.frameClicked.connect(self._on_frame_clicked)
        container_layout.addWidget(self.timeline_widget)
        
        # Add stretch to push timeline widget to top
        container_layout.addStretch()
        
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area, 1)
        
        # Summary area
        self.summary_label = QLabel("No sequences loaded")
        main_layout.addWidget(self.summary_label)
        
        self.setCentralWidget(main_widget)
        
        # Set minimum size for the window
        self.setMinimumSize(800, 600)
    
    def _on_select_folder(self):
        """Handle folder selection."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder:
            return
            
        self.status_label.setText(f"Scanning {folder}...")
        QApplication.processEvents()
        
        # Scan for sequences
        self.sequences = self.scanner.scan_directory(folder)
        self.analysis_results = self.scanner.analyze_sequences(self.sequences)
        
        # Update UI
        self.timeline_widget.set_sequences(self.sequences, self.analysis_results)
        
        # Update summary
        self._update_summary()
        
        self.status_label.setText(f"Found {len(self.sequences)} sequences in {folder}")
    
    def _update_summary(self):
        """Update the summary label with sequence info."""
        if not self.sequences:
            self.summary_label.setText("No sequences loaded")
            return
            
        total_seqs = len(self.sequences)
        seqs_with_issues = sum(1 for result in self.analysis_results.values() if result['has_issues'])
        total_missing = sum(result['missing_count'] for result in self.analysis_results.values())
        total_small = sum(result['small_count'] for result in self.analysis_results.values())
        
        summary = f"Sequences: {total_seqs} | "
        summary += f"Sequences with issues: {seqs_with_issues} | "
        summary += f"Total missing frames: {total_missing} | "
        summary += f"Total suspicious frames: {total_small}"
        
        self.summary_label.setText(summary)
    
    def _on_frame_clicked(self, file_path):
        """Handle frame clicks to open the file."""
        # Use the operating system's default method to open the file
        if sys.platform == 'win32':
            os.startfile(file_path)
        elif sys.platform == 'darwin':
            import subprocess
            subprocess.call(('open', file_path))
        else:
            import subprocess
            subprocess.call(('xdg-open', file_path))


def run_app():
    """Run the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 