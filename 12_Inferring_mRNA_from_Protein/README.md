# Counting mRNA Sequences from a Protein
## Description

This project takes a protein sequence, for each amino acid in the sequence, the program determines the possible mRNA codons. The program calculates the number of possible mRNA sequences.
The program can optionally display the exact number of possible mRNA sequences.
If the value is exceedingly large, the program presents the option to specify the limit and only return the remainder after division.
The program supports modular arithmetic to return the remainder of the number of combinations after division by a specified modulus.
A stop codon is also included, resulting in three possible termination codons.

## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading sequences from text files.
- Calculating posible combinations that can encode a protein.
- Returning the remainder after division.
- Dictionaries and list comprehensions
- Combinatorial calculations
- Modular arithmetic
- Efficient multiplication using `double-and-add`
- Handling very large integers

## Requirements
- Python
- A text file containing a protein sequence (optional)

## Usage
```bash
python mrna_protein.py file.txt [-a] [-m number]
```
