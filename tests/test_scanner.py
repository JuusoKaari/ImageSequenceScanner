"""
Tests for the scanner module of ImageSequenceScanner.
"""

import os
import tempfile
import unittest
from pathlib import Path

from image_sequence_scanner.scanner import Scanner, FrameStatus


class TestScanner(unittest.TestCase):
    """Test case for the Scanner class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        
        # Create some test files
        self._create_test_files()
        
        # Create scanner
        self.scanner = Scanner(small_file_threshold=50)  # 50 bytes threshold for small files
    
    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()
    
    def _create_test_files(self):
        """Create test image sequence files."""
        # Create a sequence with all frames
        seq1_dir = self.test_dir / "seq1"
        seq1_dir.mkdir()
        
        for i in range(1, 11):
            file_path = seq1_dir / f"render.{i:04d}.exr"
            with open(file_path, "wb") as f:
                # Normal files have 100 bytes
                f.write(b"X" * 100)
        
        # Create a sequence with missing frames
        seq2_dir = self.test_dir / "seq2"
        seq2_dir.mkdir()
        
        for i in [1, 2, 3, 5, 6, 9, 10]:  # Missing 4, 7, 8
            file_path = seq2_dir / f"render.{i:04d}.exr"
            with open(file_path, "wb") as f:
                if i == 6:  # Make one file small
                    f.write(b"X" * 20)
                else:
                    f.write(b"X" * 100)
    
    def test_scan_directory(self):
        """Test scanning a directory for sequences."""
        sequences = self.scanner.scan_directory(str(self.test_dir))
        
        # Should find 2 sequences
        self.assertEqual(len(sequences), 2)
        
        # Check keys format - they include the path, base name, and extension
        for key in sequences.keys():
            self.assertIn("|render|.exr", key)
        
        # Find the two sequences
        seq1_key = next(k for k in sequences.keys() if "seq1" in k)
        seq2_key = next(k for k in sequences.keys() if "seq2" in k)
        
        # Check first sequence
        seq1 = sequences[seq1_key]
        self.assertEqual(seq1.min_frame, 1)
        self.assertEqual(seq1.max_frame, 10)
        self.assertEqual(len(seq1.frames), 10)
        
        # Check second sequence
        seq2 = sequences[seq2_key]
        self.assertEqual(seq2.min_frame, 1)
        self.assertEqual(seq2.max_frame, 10)
        self.assertEqual(len(seq2.frames), 7)  # Only 7 files
        
        # Check small file detection
        frame6 = seq2.frames[6]
        self.assertEqual(frame6.status, FrameStatus.SMALL)
    
    def test_analyze_sequences(self):
        """Test analyzing sequences for issues."""
        sequences = self.scanner.scan_directory(str(self.test_dir))
        analysis = self.scanner.analyze_sequences(sequences)
        
        # Should have two results
        self.assertEqual(len(analysis), 2)
        
        # Find the two results
        seq1_key = next(k for k in analysis.keys() if "seq1" in k)
        seq2_key = next(k for k in analysis.keys() if "seq2" in k)
        
        # First sequence should have no issues
        self.assertEqual(analysis[seq1_key]['missing_count'], 0)
        self.assertEqual(analysis[seq1_key]['small_count'], 0)
        self.assertFalse(analysis[seq1_key]['has_issues'])
        
        # Second sequence should have issues
        self.assertEqual(analysis[seq2_key]['missing_count'], 3)
        self.assertEqual(sorted(analysis[seq2_key]['missing_frames']), [4, 7, 8])
        self.assertEqual(analysis[seq2_key]['small_count'], 1)
        self.assertEqual(analysis[seq2_key]['small_frames'], [6])
        self.assertTrue(analysis[seq2_key]['has_issues'])


if __name__ == "__main__":
    unittest.main() 