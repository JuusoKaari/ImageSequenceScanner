# Examples

This directory contains example scripts to help you get started with ImageSequenceScanner.

## Test Sequence Generator

`create_test_sequences.py` generates a set of test image sequences to demonstrate the functionality of ImageSequenceScanner:

1. A complete sequence with all frames
2. A sequence with missing frames
3. A sequence with suspiciously small files
4. A mixed sequence with both missing frames and small files

### Usage:

```bash
# Create test sequences in the default location (./test_sequences)
python create_test_sequences.py

# Or specify a custom output directory
python create_test_sequences.py --output /path/to/output
```

After generating the test sequences, run ImageSequenceScanner and select the output directory to analyze the sequences.

## Expected Results

When you scan the generated test sequences with ImageSequenceScanner, you should see:

- `complete_sequence` with all frames (1-10) in green
- `missing_frames_sequence` with frames 3, 5, and 8 shown in red (missing)
- `small_files_sequence` with frames 2 and 7 shown in yellow (small files)
- `mixed_issues_sequence` with frames 4 and 9 in red (missing) and frames 3 and 8 in yellow (small) 