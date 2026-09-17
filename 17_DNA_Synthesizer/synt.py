#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, List, Optional
import random

class Args(NamedTuple):
    """ Command line arguments. """

    file: List[TextIO]
    out_file: TextIO
    input_format: str
    number: int
    x_max: int
    m_min: int
    k_kmer:int
    seed: Optional[int]

def get_args() -> Args:
    """ Get command line arguments. """

    parse = argparse.ArgumentParser(description="",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('file', metavar='FILE', help="Input training file(s)", nargs= "+", type=argparse.FileType("rt"))

    parse.add_argument('-o','--out_file', metavar='FILE', help="The out_file's name", type=argparse.FileType("wt"), default="out.fa")

    parse.add_argument('-f','--format', metavar='format', type=str, help="Input file format", choices=['fasta', 'fastq'], default="fasta")

    parse.add_argument('-n', '--number', metavar='number', type=int, help="Number of sequences to create", default=100)

    parse.add_argument('-x', '--max', metavar='max',help="Maximum sequence length", default=75)

    parse.add_argument('-m', '--min', metavar='min', type=int, help="Minimum sequence length", default=15)
    
    parse.add_argument('-k', '--kmer',metavar='kmer', type=int, help="Size of k_mer", default=15)

    parse.add_argument('-s', '--seed', help='Random seed value', metavar='seed', type=int, default=None)
    args = parse.parse_args()

    return Args(file=args.file, out_file=args.out_file, input_format=args.format, number= args.number, x_max=args.max, m_min=args.min, k_kmer=args.kmer, seed=args.seed)

def main() -> None:
    """ Run code. """
    
    args = get_args()
    random.seed(args.seed)
    return args

if __name__ == "__main__":
    main()
