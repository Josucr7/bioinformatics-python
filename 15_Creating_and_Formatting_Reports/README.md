# Creating and Formatting Reports.

## Description

This project obtains specific data from FASTA files and tabulates the data. The objective is to generate readable reports that present the information in an organized and detailed format.
The program can display the results in several formats according to the user's preference. The project may also apply Bash scripting to generate reports for analysis.

## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading DNA sequences from FASTA files.
- Creating reports using the `tabulate` library.
- Writing Bash scripts.

## Requirements
- Python
- Biopython
- Tabulate
- Bash
- FASTA files containing DNA sequences.

## Usage
```bash
python seq.py -t [table_format] file(s).fa
```
