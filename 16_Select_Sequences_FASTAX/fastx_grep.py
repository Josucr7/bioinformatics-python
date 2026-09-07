#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, List
import sys

class Args(NamedTuple):
    """ Command-line Arguments. """

    file: List[TextIO]
    pattern: str
    input_format: str
    output_format: str
    output: TextIO
    insensitive: bool

def get_args() -> Args:
    """ Get command-line Arguments. """

    parser = argparse.ArgumentParser(description="Grep through FASTX files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', metavar="FILE", nargs='+', help="Input file(s)",type=argparse.FileType('rt'))

    parser.add_argument('pattern', metavar='PATTERN', type=str, help="Search pattern")

    parser.add_argument('-f', '--format', metavar='str', help='Input file format', choices=['fasta', 'fastq'], default="")

    parser.add_argument('-O', '--outfmt', metavar='str', help='Output file format', choices=['fasta', 'fastq', 'fasta-2line'], default="")

    parser.add_argument('-o', '--outfile', help='Output file', type=argparse.FileType('wt'), metavar='FILE', default=sys.stdout)

    parser.add_argument('-i', '--insensitive', metavar="bool",help="Case-insensitive search", default=False)

    args = parser.parse_args()

    return Args(file=args.file, pattern=args.pattern, input_format=args.f, output_format=args.O, output=args.o, insensitive=args.i)

def main() -> None:
    """ Run code. """

    args = get_args()

    return args

if __name__ == "__main__":
    main() 