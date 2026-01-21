#!/usr/bin/env python3
"""Generate the reverse complement sequence of a DNA sequence."""
import argparse
from typing import NamedTuple
import os
from Bio.Seq import Seq

class Args(NamedTuple):
    """Command Line Arguments."""
    dna:str

def get_args()->Args:
    """Get command line Arguments."""
    
    parser=argparse.ArgumentParser(description="Generate the reverse complement sequence of a DNA sequence.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dna',metavar='DNA',help='Input DNA sequence or file.')

    args=parser.parse_args()

    if os.path.isfile(args.dna):
        with open(args.dna) as fh:
            args.dna=fh.read().rstrip()

    return Args(args.dna)

def reverse_complement(dna:str)->str:
    """Generte the reverse complement of a sequence."""
    seq=Seq(dna)
    return str(seq.reverse_complement())

def main()->None:
    """Program entry point."""
    args=get_args()

    print(reverse_complement(args.dna))

if __name__=='__main__':
    main()
