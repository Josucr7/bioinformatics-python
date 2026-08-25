# Locating Restriction Sites.
## Description

This project detects palindromic sequences in DNA, which are recognized by restriction enzymes.
The program reads a FASTA file and extracts the DNA sequence. It then generates possible k-mers and computes their reverse complements to identify palindromic sequences.
Finally, the program reports the position where each potential restriction site begins and its length.

## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading DNA sequences from FASTA files.
- Generating possible k-mers from DNA sequences.
- Producing reverse complement sequences.
- Identifying palindromic sequences as potential restriction sites.

## Requirements
- Python
- Biopython
- A FASTA file containing a DNA sequence.

## Usage
```bash
python rev.py file.fa
```
