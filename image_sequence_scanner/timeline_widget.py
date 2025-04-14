"""
Timeline widget module for ImageSequenceScanner.

This module contains the TimelineWidget class which is responsible for
visualizing image sequences in a timeline view.
"""

import os
from typing import Dict

from PySide6.QtCore import Qt, QSize, QRect, Signal
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget, QToolTip, QSizePolicy

from .scanner import ImageSequence, FrameStatus


class TimelineWidget(QWidget):
    """Widget for visualizing image sequences as timelines."""
    
    frameClicked = Signal(str)  # Signal emitted when a frame is clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sequences = {}
        self.analysis_results = {}
        self.frame_width = 10
        self.timeline_height = 20
        self.timeline_spacing = 30
        self.min_global_frame = 0
        self.max_global_frame = 100
        self.setMouseTracking(True)
        
        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        
    def set_sequences(self, sequences: Dict[str, ImageSequence], analysis_results: Dict):
        """Set the sequences to display."""
        self.sequences = sequences
        self.analysis_results = analysis_results
        
        # Determine global frame range
        min_frames = [seq.min_frame for seq in sequences.values() if seq.min_frame is not None]
        max_frames = [seq.max_frame for seq in sequences.values() if seq.max_frame is not None]
        
        if min_frames and max_frames:
            self.min_global_frame = min(min_frames)
            self.max_global_frame = max(max_frames)
        
        # Calculate and set fixed height based on number of sequences
        height = len(sequences) * self.timeline_spacing + 100  # Extra 100px for ruler and padding
        self.setMinimumHeight(height)
        
        # Update widget size
        self.updateGeometry()
        self.update()
    
    def sizeHint(self):
        """Suggest an appropriate size for the widget."""
        # Calculate width based on frame range and name area
        width = (self.max_global_frame - self.min_global_frame + 1) * self.frame_width + 300
        
        # Calculate height based on number of sequences
        height = len(self.sequences) * self.timeline_spacing + 100  # Extra 100px for ruler and padding
        
        return QSize(max(width, 800), height)
    
    def minimumSizeHint(self):
        """Return the minimum size of the widget."""
        return QSize(800, 200)  # Minimum reasonable size for usability
    
    def paintEvent(self, event):
        """Paint the timelines."""
        if not self.sequences:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        painter.fillRect(event.rect(), QColor(245, 245, 245))
        
        # Draw frame ruler
        self._draw_ruler(painter)
        
        # Draw each sequence timeline
        y_offset = 50  # Start below the ruler
        for seq_key, sequence in self.sequences.items():
            self._draw_timeline(painter, sequence, seq_key, y_offset)
            y_offset += self.timeline_spacing
    
    def _draw_ruler(self, painter):
        """Draw a ruler showing frame numbers."""
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        
        # Draw ruler line
        ruler_y = 30
        painter.drawLine(0, ruler_y, self.width(), ruler_y)
        
        # Draw tick marks and labels for frames
        frame_step = max(1, (self.max_global_frame - self.min_global_frame) // 20)
        for frame in range(self.min_global_frame, self.max_global_frame + 1, frame_step):
            x = self._frame_to_x(frame)
            
            # Draw tick
            painter.drawLine(x, ruler_y - 5, x, ruler_y + 5)
            
            # Draw label
            painter.drawText(x - 15, ruler_y - 10, 30, 10, Qt.AlignCenter, str(frame))
    
    def _draw_timeline(self, painter, sequence: ImageSequence, seq_key: str, y: int):
        """Draw a timeline for a single sequence."""
        # Draw sequence name with folder structure
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        name_rect = QRect(10, y, 300, 20)  # Increased width for longer names
        
        # Get the relative path from sequence base name
        base_path = os.path.dirname(sequence.base_name)
        base_name = os.path.basename(sequence.base_name)
        
        # Format the display name to show folder structure
        if base_path:
            # Split the path into components
            path_parts = base_path.split(os.sep)
            # Take last three folder names if path is long
            if len(path_parts) > 3:
                path_parts = ['...'] + path_parts[-3:]
            folder_path = os.sep.join(path_parts)
            display_name = f"{folder_path}/{base_name}"
        else:
            display_name = base_name
        
        # Draw the full path with elided text if needed
        metrics = painter.fontMetrics()
        elided_text = metrics.elidedText(display_name, Qt.ElideMiddle, name_rect.width())
        painter.drawText(name_rect, Qt.AlignLeft | Qt.AlignVCenter, elided_text)
        
        # Draw timeline background
        if sequence.min_frame is not None and sequence.max_frame is not None:
            timeline_x = self._frame_to_x(sequence.min_frame)
            timeline_width = (sequence.max_frame - sequence.min_frame + 1) * self.frame_width
            
            bg_rect = QRect(timeline_x, y, timeline_width, self.timeline_height)
            painter.fillRect(bg_rect, QColor(200, 200, 200))
            
            # Draw each frame
            for frame_num in range(sequence.min_frame, sequence.max_frame + 1):
                frame_x = self._frame_to_x(frame_num)
                frame_rect = QRect(frame_x, y, self.frame_width, self.timeline_height)
                
                if frame_num in sequence.frames:
                    frame = sequence.frames[frame_num]
                    # Color based on status
                    if frame.status == FrameStatus.SMALL:
                        color = QColor(255, 100, 0)  # Orange for hard size limit
                    elif frame.status == FrameStatus.SMALL_RELATIVE:
                        color = QColor(255, 200, 0)  # Yellow for relative size issues
                    else:
                        color = QColor(0, 180, 0)    # Green for normal files
                else:
                    # Red for missing frames
                    color = QColor(255, 0, 0)
                
                painter.fillRect(frame_rect, color)
                painter.setPen(QPen(QColor(150, 150, 150), 1))
                painter.drawRect(frame_rect)
    
    def _frame_to_x(self, frame: int) -> int:
        """Convert a frame number to an x-coordinate."""
        return 320 + (frame - self.min_global_frame) * self.frame_width  # Increased x offset for longer names
    
    def _x_to_frame(self, x: int) -> int:
        """Convert an x-coordinate to a frame number."""
        return self.min_global_frame + (x - 320) // self.frame_width  # Increased x offset for longer names
    
    def mouseMoveEvent(self, event):
        """Handle mouse movement to show frame info in tooltips."""
        if not self.sequences:
            return
            
        # Calculate which frame we're hovering over
        x, y = event.x(), event.y()
        
        # Check if we're in the timeline area
        if x < 320 or y < 50:  # Increased x threshold for longer names
            return
            
        frame_num = self._x_to_frame(x)
        if frame_num < self.min_global_frame or frame_num > self.max_global_frame:
            return
            
        # Find which sequence we're hovering over
        seq_idx = (y - 50) // self.timeline_spacing
        if seq_idx < 0 or seq_idx >= len(self.sequences):
            return
            
        # Get the sequence and check if this frame exists
        seq_key = list(self.sequences.keys())[seq_idx]
        sequence = self.sequences[seq_key]
        
        tooltip_text = f"Frame: {frame_num}"
        
        if frame_num in sequence.frames:
            frame = sequence.frames[frame_num]
            tooltip_text += f"\nFile: {os.path.basename(frame.file_path)}"
            tooltip_text += f"\nPath: {os.path.dirname(frame.file_path)}"
            tooltip_text += f"\nSize: {frame.file_size / 1024:.1f} KB"
            
            # Add more detailed status info
            if frame.status == FrameStatus.SMALL:
                tooltip_text += f"\nStatus: Suspiciously small (under {100} KB)"
            elif frame.status == FrameStatus.SMALL_RELATIVE:
                tooltip_text += "\nStatus: Significantly smaller than neighboring frames"
            else:
                tooltip_text += "\nStatus: Normal"
        else:
            tooltip_text += "\nStatus: Missing"
            
        QToolTip.showText(event.globalPos(), tooltip_text, self)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse clicks to open files."""
        if event.button() != Qt.LeftButton or not self.sequences:
            return
            
        # Calculate which frame was clicked
        x, y = event.x(), event.y()
        
        # Check if we're in the timeline area
        if x < 320 or y < 50:  # Increased x threshold for longer names
            return
            
        frame_num = self._x_to_frame(x)
        if frame_num < self.min_global_frame or frame_num > self.max_global_frame:
            return
            
        # Find which sequence was clicked
        seq_idx = (y - 50) // self.timeline_spacing
        if seq_idx < 0 or seq_idx >= len(self.sequences):
            return
            
        # Get the sequence and check if this frame exists
        seq_key = list(self.sequences.keys())[seq_idx]
        sequence = self.sequences[seq_key]
        
        if frame_num in sequence.frames:
            frame = sequence.frames[frame_num]
            self.frameClicked.emit(frame.file_path) 