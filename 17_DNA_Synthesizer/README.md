# DNA Synthesizer

## Description

This project is a command-line tool that generates synthetic DNA sequences based on a training set of DNA sequences.
The program analyzes the frequency of k-mers in one or more input FASTA or FASTQ files and uses these frequencies to generate new DNA sequences with similar patterns to the training data.
The generated sequences can be customized by specifying the number of sequences, minimum and maximum sequence length, k-mer size, and random seed.

## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading FASTA and FASTQ files with Biopython.
- Writing FASTA files with Biopython.
- Working with `Seq`, `SeqRecord`, and `SeqIO`.
- Finding k-mers in DNA sequences.
- Counting nucleotide frequencies using `Counter`.
- Building a k-mer probability model.
- Generating sequences using weighted random choices.
- Using `random.seed()` to obtain reproducible results.
- Processing multiple input files.
- Using type hints with `List`, `Optional`, `Dict`, and `NamedTuple`.
- Creating command-line programs with a `main()` function.
- Testing the program with `pytest`.

## Usage
```bash
./synt.py FILE [FILE ...] [OPTIONS]
```
