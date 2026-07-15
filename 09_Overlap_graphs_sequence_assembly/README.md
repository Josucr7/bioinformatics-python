#  Sequence Assembly Using Shared K-mers

## Description

This proyect reads a FASTA file and extracts the first and last k-mers from each sequence.
It then identifies overlaps between all sequences.
Finally, it can generate a graph to visualize the overlaps and create a log file containing information about the extracted k-mers.

## Concepts Practiced


## Concepts Practiced
- Using argparse to handle command-line arguments.
- Reading FASTA file.
- Extracting the first and last k-mers from sequences.
- Finding overlpa between seqquences.
- Grouping Sequences by overlapping k-mers.
- Generating log files using logging levels.
- Visualizing overlap graphs with Graphviz.

  
## Requirements
- Python
- Graphviz 
- Biopython
- A FASTA file
## Usage

```bash
python overlap.py [-k K_MERS] [-d] [-o OUTFILE] [-v] FASTA_FILE
```
