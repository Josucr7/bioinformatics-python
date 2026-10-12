#!/usr/bin/env python 3

import argparse
from typing import NamedTuple, TextIO

class Args(NamedTuple):
    """ Command-line Arguments. """

    hits: TextIO
    annotations: TextIO
    outfile: TextIO
    delimiter: str
    pctid: float

def get_args() -> Args:
    """ Get command-line arguments. """

    parse = argparse.ArgumentParser(description="Probabilistically subset FASTA files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('-b', '--blasthits', metavar='FILE', type=argparse.FileType('rt'), help='BLAST -outfmt 6', required=True)

    parse.add_argument('-a', '--annotations', metavar='FILE', type=argparse.FileType('rt'), help='Annotations file', required=True)

    parse.add_argument('-o', '--outfile', metavar='FILE', type=argparse.FileType('wt'), help='Output file', default='out.csv')

    parse.add_argument('-d', '--delimiter', metavar='DELIM', type=str, help='Output field delimiter', default='')

    parse.add_argument('-p', '--pctid', metavar='PCTID', type=float, help='Minimum percent identity', default=0.)

    args = parse.parse_args()

    return Args(hits=args.blasthits,annotations=args.annotations, outfile=args.outfile, delimiter=args.delimiter, pctid=args.pctid)


