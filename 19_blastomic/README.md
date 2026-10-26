# BLAST Hits and Sequence Annotations

## Description

A Python command-line tool for combining BLAST results with sequence annotations and filtering hits by percent identity.

This project contains **two implementations** of the same task:

- `pandas` — implementation using the pandas library.
- `csv` — implementation using Python's built-in `csv` module.

The goal is to compare two approaches for processing tabular biological data.

## Features

- Read BLAST results in tabular format.
- Read sequence annotation data from a CSV file.
- Filter BLAST hits by minimum percent identity.
- Match BLAST query sequences with their annotations.
- Export selected fields to CSV or TSV.
- Automatically determine the output delimiter from the output file extension.
- Allow the output delimiter to be specified manually.

## Usage
```bash
blast_cv.py [-h] -b FILE -a FILE [-o FILE] [-d DELIM] [-p PCTID]
blast_panda.py [-h] -b FILE -a FILE [-o FILE] [-d DELIM] [-p PCTID]
```
