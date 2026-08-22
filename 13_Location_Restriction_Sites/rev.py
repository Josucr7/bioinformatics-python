#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, Optional
from Bio import SeqIO, Seq

class Args(NamedTuple):
    """ Command line-arguments """

    file: TextIO

def get_args() -> Args:
    """ Get command line-arguments """

    parser = argparse.ArgumentParser(description="Locating Restriction Files.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',metavar="FILE",help="Input a FASTA file.",type=argparse.FileType("rt"))

    args = parser.parse_args()

    return Args(file=args.file)

def read_fasta_file(file:TextIO) -> str:
    """ Read a fasta file. """

    rec = SeqIO.parse(file,"fasta")
    return str(next(rec).seq)

def reverse_complement(seq:str):
    """ Generate the reverse complement sequences. """

    return Seq.reverse_complement(seq)

def k_mers(sequence:str,k:int) -> Optional[str]:
    """ Get k-mers from a DNA sequences. """

    n = len(sequence) + 1 - k
    return [] if n < 1 else [sequence[i:i+k] for i in range(n)]
     

def main():
    """ Run code """

    args = get_args()

    seq = read_fasta_file(args.file)
    rev = reverse_complement(seq)
    print(rev)
    print(k_mers(seq,3))

if __name__ == "__main__":
    main()