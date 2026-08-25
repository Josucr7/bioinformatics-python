#!/usr/bin/env python3
import argparse
from typing import NamedTuple, TextIO, Optional
from Bio import SeqIO, Seq

class Args(NamedTuple):
    """ Command line-Arguments."""

    file: TextIO

def get_args() -> Args:
    """ Get command line-Arguments. """

    parse = argparse.ArgumentParser(description="Detect region of nucleotides that transcribe amino acid sequences.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument("file",metavar="FILE",help="Input a FASTA file.",type=argparse.FileType('rt'))

    args = parse.parse_args()
    
    return Args(file=args.file)

def read_fasta_file(file:TextIO) -> Optional[str]:
    """ Read a fasta file. """

    records = SeqIO.parse(file,"fasta")
    sequence = next(records,None)
    if sequence is not None:
        return str(sequence.seq)
    return None

def dna_to_aa(dna:str) -> str:
    """ From DNA sequence translate to aminoacid sequence.  """

    return Seq.translate(dna,to_stop=True)


def main() -> None:
    """ Run code. """
    args = get_args()
    sequence = read_fasta_file(args.file)
    print(dna_to_aa(sequence))

if __name__ == "__main__":
    main()