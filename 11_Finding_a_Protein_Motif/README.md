# Finding a Protein Motif
## Description

This project takes protein IDs from a file, downloads their protein sequences, and identifies sequences that contain the N-glycosylation motif.
The program downloads a FASTA file for each protein ID from the UniProt website. Each FASTA file contains the corresponding amino acid sequence. The downloaded files are then saved in a specified directory.
Finally, the program opens each FASTA file and detects the locations and matching N-glycosylation motifs in the protein sequences.
The program uses a Bash script to download protein sequences, so it must be run on Linux.

## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading data from a text file.
- Writing and using Bash scripts on Linux.
- Reading and parsing FASTA files with Biopython.
- Using regular expressions to identify N-glycosylation motifs in protein sequences.
- Downloading protein sequences from UniProt.
- Processing biological sequence data.

## Requirements
- Python
- Biopython
- Linux (required to run the Bash download script)
- A text file containing UniProt protein IDs

## Usage

```bash
python protein_motif.py file.txt [-d download_dir] [-v]
```
