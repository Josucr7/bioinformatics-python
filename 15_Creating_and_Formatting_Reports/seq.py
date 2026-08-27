#!/usr/bien/env python3
import argparse
from typing import NamedTuple, TextIO

class Args(NamedTuple):
    """ Command line arguments. """

    file: TextIO
    
    tablefmt: bool

def get_args() -> Args:
    """ Get command line arguments. """

    parser = argparse.ArgumentParser(description='Mimic seqmagick',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',metavar="FILE",help="Input FASTA file(s).",type=argparse.FileType('rt'))

    parser.add_argument('-t table','--tablefmt',help="Tabulate table style", default="plain")

    args = parser.parse_args()

    return Args(file=args.file,tablefmt=args.tablefmt)

def main () -> None:
    """"""
    args = get_args()

if __name__ == "__main__":
    main()