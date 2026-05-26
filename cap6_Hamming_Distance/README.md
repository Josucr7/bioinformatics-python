# Calculate the Hamming Distance Between Two Sequences
## Description
This project analyzes the best alignment between two DNA sequences and returns the Hamming distance value. The program can read two sequences as strings or from a FASTA file containing two sequences.
## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading input from FASTA file(s).
- Calculating the Hamming Distance between sequences.
- Sequence alignment.
- Error value application.

## Requirements
- Python
- Biopython
- FASTA input file(s)
## Usage
```bash
python hamm.py -s1 "DNA sequence" -s2 "DNA sequence"
```
or 
```bash
python hamm.py -f file.fa
```
