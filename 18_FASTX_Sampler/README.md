# Probabilistic FASTA Sampler

## Description

This project is a command-line tool for probabilistically selecting sequences from FASTA or FASTQ files.
The program randomly selects sequences based on a user-defined probability and writes the selected sequences to FASTA files. It also allows the user to specify a maximum number of sequences and a random seed for reproducible results.
Multiple input files can be processed in a single execution.

## Features
- Reads FASTA and FASTQ files.
- Randomly selects sequences based on a probability.
- Allows a maximum number of sequences to be selected.
- Supports random seeds for reproducible results.
- Processes multiple input files.
- Creates an output directory automatically.
- Always writes the selected sequences in FASTA format.

## Usage
```bash
./fastx.py [OPTIONS] FILE [FILE ...]
```
