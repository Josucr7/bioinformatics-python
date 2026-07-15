# Finding the Longest Shared Subsequences
## Description
This poyect reads a FASTA file and finds the shared subsequences present in all DNA sequences.
The program extracts all possible k-mers from each sequence and compares them to identify the k-mers shared by every sequence. Finally, it prints the longest shared subsequences to the terminal.

## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading a FASTA file.
- Using binary search to find a starting k-mer length.
- Extracting all possible k-mers from DNA sequences.
- Identifying the k-mers shared by all sequences.
- Finding the longest shared subsequences.

## Requirements

- Python
- Biopython
- A FASTA file

## Usage

```bash
python lcsm.py FASTA_FILE
```
