#!/usr/bin/env python3
from typing import NamedTuple
import argparse

""" Find a DNA subsequence in a DNA sequence. """

class Args(NamedTuple):
    """ Command line-arguments"""

    dna: str
    sub_dna: str

def get_args() -> Args:
    """ Get command line arguments. """

    parser = argparse.ArgumentParser(description="The program analyzes the occurrences of a DNA subsequence in a DNA sequence.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dna',metavar="DNA",help="Input DNA sequence")

    parser.add_argument('sub_dna',metavar="sub_DNA",help="Input DNA subsequence")

    args=parser.parse_args()

    return Args(dna=args.dna,sub_dna=args.sub_dna)

def range_seq(seq:str) -> list[int]:
    """ Get a range of a sequences. """

    return list(range(len(seq)))

def match_subseq_in_seq(seq:str,sub:str) -> list[int]:
    """ Match the position if the subsequence is in sequences. """

    positions = []
    for i in range_seq(seq):
        position = seq.find(sub,i)+1
        if position != 0 and not position in positions:
            positions.append(position)
    return positions

def main() -> None:
    """ Run the code. """

    args = get_args()

    positions = match_subseq_in_seq(seq=args.dna,sub=args.sub_dna)
    
    if len(positions)==0:
        print(None)
    else:
        print(positions)

if __name__=="__main__":
    main()