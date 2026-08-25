#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, Optional, List
from Bio import SeqIO, Seq

class Args(NamedTuple):
    """ Command line-arguments """

    file: TextIO

def get_args() -> Args:
    """ Get command line-arguments """

    parser = argparse.ArgumentParser(description="Locating Restriction Sites.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',metavar="FILE",help="Input a FASTA file.",type=argparse.FileType("rt"))

    args = parser.parse_args()

    return Args(file=args.file)

def read_fasta_file(file:TextIO) -> Optional[str]:
    """ Read a fasta file. """

    rec = SeqIO.parse(file,"fasta")
    sequence = next(rec,None)
    if sequence is not None:
        return str(sequence.seq)
    return None

def reverse_complement(seq:str) -> str:
    """ Generate the reverse complement sequences. """

    return Seq.reverse_complement(seq)

def k_mers(sequence:str,k:int) -> List[str]:
    """ Get k-mers from a DNA sequence. """

    n = len(sequence) + 1 - k
    return [] if n < 1 else [sequence[i:i+k] for i in range(n)]

def compare_kmer(kmers:List[str]) -> Optional[List[List[int]]]:
    """ Detect k-mers that are equal to their reverse complement. """

    reverse = [reverse_complement(kmer) for kmer in kmers]
    base = list(enumerate(zip(kmers,reverse),start=1))
    positions = [[position,len(sequences[0])] for position,sequences in base if sequences[0]==sequences[1]] 
    if not positions:
        return None
    return positions

def main() -> None:
    """ Run code. """
    args = get_args()
    sequence = read_fasta_file(args.file)
    if sequence is None:
        return None
    sites=[site for i in range(4,len(sequence)+1) if (site:=compare_kmer(k_mers(sequence,i))) is not None]
    for site in sites:
        for pair in site:
            print(*pair)
if __name__ == "__main__":
    main()
