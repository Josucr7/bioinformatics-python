#!/usr/bin/env python3

"""Calculate tetranucleotide frequency in a DNA sequence."""

import argparse
import os 
from typing import NamedTuple
from collections import Counter

class Args(NamedTuple):
    """Command line Arguments"""
    dna:str

def get_args()->Args:
    """Get command line Arguments"""
    parser=argparse.ArgumentParser(description='Tetranucleotide frequency in a DNA sequence.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('dna',metavar='DNA',help='Input a DNA sequence.')

    args=parser.parse_args()

    if os.path.isfile(args.dna):
        args.dna = open(args.dna).read().rstrip()

    return Args(args.dna)

def counter_nucleotides(seq)->None:
    """Function to Counter the nucleotides in dna sequence."""
    return Counter(seq)

def main()->None:
    """Return the exact number for any nucleotide"""
    args = get_args()
    nucleotides=counter_nucleotides(args.dna.upper())
    print(nucleotides['A'],nucleotides['C'],nucleotides['G'],nucleotides['T'])

if __name__=='__main__':
    main()