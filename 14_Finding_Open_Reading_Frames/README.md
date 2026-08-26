# Finding Open Reading Frames.
## Description

This project finds possible open reading frames (ORFs), which are regions of DNA that can potentially code for proteins. They are between a start codon and a stop codon. 
First, the program reads a FASTA file and extracts the DNA sequence. It then generates the reverse complement DNA sequence and transcribes both DNA sequences into RNA.
The program translates the RNA sequences, checks whether their lengths are divisible by 3 so they can be translated into codons of three nucleotides.
Finally, the translations generate amino acid sequences, and the program finds all possible ORFs.

## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading DNA sequences from FASTA files.
- Generating the reverse complement of a DNA sequence.
- Transcribing DNA sequences into RNA sequences.
- Checking whether sequence lengths are divisible by 3.
- Translating RNA sequences into amino acid sequences.
- Finding open reading frames (ORFs).
- Applying regular expressions (regex) for sequence searches.

## Requirements
- Python
- Biopython
- Regular expressions
- A FASTA file containing a DNA sequence.

## Usage
```bash
python orf.py file.fa
```
