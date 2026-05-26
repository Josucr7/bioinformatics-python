# Calculate the Cytosine and Guanine content of DNA Sequences in FASTA files.
## Description
The actual project reads FASTA Files containing DNA sequences and calculates the percentage of cytosine (C) and guanine (G) content of each sequence. The program identifies the sequence with highest GC content and saves the result in an output directory.

## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading input from FASTA file(s).
- Calculating GC content in a DNA sequence using the Biopython library.
- Creating an output directory to store the GC content results.
- Generation output FASTA files(s). 
## Requirements
- Python
- Biopython 
- Input FASTA file(s)
## Usage
```bash
python cgc.py FASTA file(s)
```
