"""
Scanner module for ImageSequenceScanner.

This module provides functionality to scan directories for image sequences,
detect frame ranges, missing frames, and file issues.
"""

import os
import re
import glob
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, NamedTuple
from statistics import mean


class FrameStatus:
    NORMAL = "normal"
    MISSING = "missing"
    SMALL = "small"  # Below hard limit
    SMALL_RELATIVE = "small_relative"  # Smaller than neighbors


class Frame(NamedTuple):
    """Represents a single frame in an image sequence."""
    number: int
    file_path: str
    file_size: int
    status: str


class ImageSequence:
    """Represents an image sequence with its frames and metadata."""
    
    def __init__(self, base_name: str, extension: str):
        self.base_name = base_name
        self.extension = extension
        self.frames: Dict[int, Frame] = {}
        self.min_frame: Optional[int] = None
        self.max_frame: Optional[int] = None
    
    def add_frame(self, frame: Frame) -> None:
        """Add a frame to this sequence."""
        self.frames[frame.number] = frame
        
        # Update min/max frame numbers
        if self.min_frame is None or frame.number < self.min_frame:
            self.min_frame = frame.number
        
        if self.max_frame is None or frame.number > self.max_frame:
            self.max_frame = frame.number
    
    def get_missing_frames(self) -> List[int]:
        """Return a list of missing frame numbers."""
        if self.min_frame is None or self.max_frame is None:
            return []
        
        expected_frames = set(range(self.min_frame, self.max_frame + 1))
        actual_frames = set(self.frames.keys())
        return sorted(expected_frames - actual_frames)
    
    def __str__(self) -> str:
        return f"{self.base_name} [{self.min_frame}-{self.max_frame}] {self.extension}"


class Scanner:
    """Scanner for detecting and analyzing image sequences."""
    
    # Common image formats used in 3D rendering
    IMAGE_EXTENSIONS = {'.exr', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.dpx'}
    
    # Regular expression for matching sequence patterns
    SEQUENCE_PATTERN = re.compile(r'(.+?)(\d+)(\.\w+)$')
    
    def __init__(self, 
                 hard_size_threshold: int = 100 * 1024,  # 100 KB
                 relative_size_threshold: float = 0.8,  # 80% of neighbors
                 neighbor_window: int = 5  # Check 5 frames before and after
                 ):
        """
        Initialize the scanner.
        
        Args:
            hard_size_threshold: File size threshold in bytes below which a file
                               is considered suspiciously small.
            relative_size_threshold: Threshold ratio (0-1) for comparing frame size
                                   to its neighbors. A frame smaller than this ratio
                                   of its neighbors' average is considered suspicious.
            neighbor_window: Number of neighboring frames to check on each side
                           for relative size comparison.
        """
        self.hard_size_threshold = hard_size_threshold
        self.relative_size_threshold = relative_size_threshold
        self.neighbor_window = neighbor_window
    
    def _check_relative_size(self, frame_num: int, frames: Dict[int, Frame]) -> bool:
        """
        Check if a frame is suspiciously smaller than its neighbors.
        
        Args:
            frame_num: The frame number to check
            frames: Dictionary of all frames in the sequence
            
        Returns:
            True if the frame is suspiciously small compared to its neighbors
        """
        if frame_num not in frames:
            return False
            
        current_size = frames[frame_num].file_size
        
        # Get sizes of neighboring frames
        neighbor_sizes = []
        for i in range(-self.neighbor_window, self.neighbor_window + 1):
            if i == 0:  # Skip current frame
                continue
            neighbor_num = frame_num + i
            if neighbor_num in frames:
                neighbor_sizes.append(frames[neighbor_num].file_size)
        
        # If we don't have enough neighbors for comparison, skip relative check
        if len(neighbor_sizes) < 2:
            return False
        
        # Calculate average size of neighbors
        avg_neighbor_size = mean(neighbor_sizes)
        
        # Check if current frame is suspiciously small compared to neighbors
        return current_size < (avg_neighbor_size * self.relative_size_threshold)
    
    def scan_directory(self, directory: str) -> Dict[str, ImageSequence]:
        """
        Recursively scan a directory for image sequences.
        
        Args:
            directory: Path to the directory to scan
            
        Returns:
            Dictionary mapping sequence identifiers to ImageSequence objects
        """
        sequences = {}
        
        # First pass: collect all frames
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if it's an image file
                _, ext = os.path.splitext(file)
                if ext.lower() not in self.IMAGE_EXTENSIONS:
                    continue
                
                # Try to match the sequence pattern
                match = self.SEQUENCE_PATTERN.match(file)
                if not match:
                    continue
                
                base_name, frame_number_str, extension = match.groups()
                frame_number = int(frame_number_str)
                
                # Create a unique key for this sequence
                sequence_key = f"{os.path.dirname(file_path)}|{base_name}|{extension}"
                
                # Get or create the sequence
                if sequence_key not in sequences:
                    sequences[sequence_key] = ImageSequence(
                        base_name=os.path.join(os.path.dirname(file_path), base_name),
                        extension=extension
                    )
                
                # Add the frame with initial status
                file_size = os.path.getsize(file_path)
                initial_status = (
                    FrameStatus.SMALL if file_size < self.hard_size_threshold
                    else FrameStatus.NORMAL
                )
                
                frame = Frame(
                    number=frame_number,
                    file_path=file_path,
                    file_size=file_size,
                    status=initial_status
                )
                sequences[sequence_key].add_frame(frame)
        
        # Second pass: check relative sizes
        for sequence in sequences.values():
            if sequence.min_frame is None:
                continue
                
            # Create new frames dict with updated statuses
            new_frames = {}
            for frame_num in range(sequence.min_frame, sequence.max_frame + 1):
                if frame_num not in sequence.frames:
                    continue
                    
                old_frame = sequence.frames[frame_num]
                
                # If frame is already marked as small (hard limit), keep that status
                if old_frame.status == FrameStatus.SMALL:
                    new_frames[frame_num] = old_frame
                    continue
                
                # Check relative size
                if self._check_relative_size(frame_num, sequence.frames):
                    new_frames[frame_num] = Frame(
                        number=old_frame.number,
                        file_path=old_frame.file_path,
                        file_size=old_frame.file_size,
                        status=FrameStatus.SMALL_RELATIVE
                    )
                else:
                    new_frames[frame_num] = old_frame
            
            # Update sequence with new frames
            sequence.frames = new_frames
        
        return sequences
    
    def analyze_sequences(self, 
                        sequences: Dict[str, ImageSequence]
                        ) -> Dict[str, Dict]:
        """
        Analyze sequences for missing frames and other issues.
        
        Args:
            sequences: Dictionary of sequences to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        results = {}
        
        for seq_key, sequence in sequences.items():
            missing_frames = sequence.get_missing_frames()
            small_frames = [
                frame_num for frame_num, frame in sequence.frames.items()
                if frame.status in (FrameStatus.SMALL, FrameStatus.SMALL_RELATIVE)
            ]
            
            results[seq_key] = {
                'base_name': sequence.base_name,
                'extension': sequence.extension,
                'frame_range': (sequence.min_frame, sequence.max_frame),
                'total_frames': len(sequence.frames),
                'missing_frames': missing_frames,
                'missing_count': len(missing_frames),
                'small_frames': small_frames,
                'small_count': len(small_frames),
                'has_issues': bool(missing_frames or small_frames)
            }
        
        return results 