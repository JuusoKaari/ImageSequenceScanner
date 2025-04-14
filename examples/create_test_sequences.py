#!/usr/bin/env python3
"""
Example script to create test image sequences for ImageSequenceScanner.

This script creates a set of test image sequences to demonstrate the
functionality of ImageSequenceScanner. It generates:
1. A complete sequence with all frames
2. A sequence with missing frames
3. A sequence with some suspiciously small files

Run this script first, then use ImageSequenceScanner to analyze the created sequences.
"""

import os
import argparse
from pathlib import Path
import random


def create_test_sequence(base_dir, seq_name, frames, frame_range, 
                         missing_frames=None, small_frames=None):
    """Create a test image sequence with optional missing or small frames."""
    # Create the sequence directory
    seq_dir = Path(base_dir) / seq_name
    seq_dir.mkdir(parents=True, exist_ok=True)
    
    # List of created files
    created_files = []
    
    # Create each frame
    for frame in range(frame_range[0], frame_range[1] + 1):
        # Skip if frame should be missing
        if missing_frames and frame in missing_frames:
            continue
            
        # Create the file
        file_path = seq_dir / f"render.{frame:04d}.exr"
        
        # Determine file size
        if small_frames and frame in small_frames:
            size = random.randint(10, 50)  # Small file (10-50 bytes)
        else:
            size = random.randint(10000, 50000)  # Normal file (10-50 KB)
        
        # Write the file with random bytes
        with open(file_path, 'wb') as f:
            f.write(os.urandom(size))
        
        created_files.append(file_path)
    
    return created_files


def main():
    parser = argparse.ArgumentParser(description='Create test image sequences')
    parser.add_argument('--output', '-o', default='./test_sequences',
                      help='Output directory for test sequences')
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    
    print(f"Creating test sequences in {output_dir}")
    
    # 1. Create a complete sequence
    files1 = create_test_sequence(
        output_dir, 
        "complete_sequence",
        frames=10, 
        frame_range=(1, 10)
    )
    print(f"Created complete sequence with {len(files1)} frames")
    
    # 2. Create a sequence with missing frames
    files2 = create_test_sequence(
        output_dir, 
        "missing_frames_sequence",
        frames=7, 
        frame_range=(1, 10),
        missing_frames=[3, 5, 8]
    )
    print(f"Created sequence with missing frames: {len(files2)} frames, missing: 3, 5, 8")
    
    # 3. Create a sequence with some small files
    files3 = create_test_sequence(
        output_dir, 
        "small_files_sequence",
        frames=10, 
        frame_range=(1, 10),
        small_frames=[2, 7]
    )
    print(f"Created sequence with small files: {len(files3)} frames, small files: 2, 7")
    
    # 4. Create a mixed sequence with both issues
    files4 = create_test_sequence(
        output_dir, 
        "mixed_issues_sequence",
        frames=8, 
        frame_range=(1, 10),
        missing_frames=[4, 9],
        small_frames=[3, 8]
    )
    print(f"Created mixed sequence: {len(files4)} frames, missing: 4, 9, small: 3, 8")
    
    print("\nTest sequences created successfully. Run the ImageSequenceScanner app "
          f"and select the directory: {output_dir}")


if __name__ == "__main__":
    main() 