# Creating a Utility Program to Select Sequences

## Description

This project implements a command-line utility for searching biological sequences in FASTA and FASTQ files.
The program automatically detects the input file format from its extension, or allows the user to specify the format manually. It searches for a given pattern in the sequence IDs and descriptions and outputs the matching sequences in FASTA or FASTQ format.

## Concepts Practiced
- Using argparse to handle command-line arguments.
- Detecting FASTA and FASTQ file formats from file extensions.
- Reading FASTA and FASTQ files with Biopython.
- Writing sequences in different output formats.
- Using regular expressions (`re`) to search for patterns.
- Handling case-insensitive searches.
- Working with input and output files from the command line.

## Requirements
- Python 3
- Biopython
- FASTA or FASTQ files

## Usage
```bash
python fastx_grep.py [-h] [-f {fasta,fastq}] [-O {fasta,fastq,fasta-2line}] [-o FILE] [-i] FILE... PATTERN
```
