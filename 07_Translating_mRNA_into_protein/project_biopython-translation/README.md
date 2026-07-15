# Translate an mRNA Sequence into Protein Sequence using Biopython.
## Description
The project uses the Biopython library for translating an mRNA sequence provided either as a string or from a FASTA file.
## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading input from FASTA files containing one or more sequences.
- Translating mRNA sequences into protein sequences.
- Applying biological concepts such as stop codons.

## Requirements
- Python
- Biopython
- FASTA input file(s)
## Usage
```bash
python mrna_proteins_bio.py -s "mRNA sequence"
```
or 
```bash
python mrna_proteins_bio.py -f file.fa
```
