#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, List, Optional
import sys
import re
import os
from Bio import SeqIO

class Args(NamedTuple):
    """ Command-line Arguments. """

    file: List[TextIO]
    pattern: str
    input_format: str
    output_format: str
    outfile: TextIO
    insensitive: bool

def get_args() -> Args:
    """ Get command-line Arguments. """

    parser = argparse.ArgumentParser(description="Grep through FASTX files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', metavar="FILE", nargs='+', help="Input file(s)",type=argparse.FileType('rt'))

    parser.add_argument('pattern', metavar='PATTERN', type=str, help="Search pattern")

    parser.add_argument('-f', '--format', metavar='str', help='Input file format', choices=['fasta', 'fastq'], default="")

    parser.add_argument('-O', '--outfmt', metavar='str', help='Output file format', choices=['fasta', 'fastq', 'fasta-2line'], default="")

    parser.add_argument('-o', '--outfile', help='Output file', type=argparse.FileType('wt'), metavar='FILE', default=sys.stdout)

    parser.add_argument('-i', '--insensitive',help="Case-insensitive search", action="store_true")

    args = parser.parse_args()

    return Args(file = args.file, pattern = args.pattern, input_format = args.format, output_format = args.outfmt, outfile = args.outfile, insensitive = args.insensitive)

def guess_format(filename: str) -> Optional[str]:
    """ Guess format from specific extension. """
    
    format = re.sub('^[.]','',os.path.splitext(filename)[1])
    return 'fasta' if re.match('f(ast|n|a)?a$',format) else 'fastq' if re.match('f(ast)?q$',format) else None

def read_fast_file(fh: TextIO, frt: Optional[str]=None) -> Optional[TextIO]:
    """ Read a file depends of format. """

    if frt is None:
        return None
    seq = SeqIO.parse(fh, frt)
    return seq

def write_fast_file(rec:TextIO, outfile:str, frt:str) -> None:
    """ Write a file dpeends of format. """

    SeqIO.write(rec, outfile, frt)

def main() -> None:
    """ Run code. """

    args = get_args()
    regex = re.compile(args.pattern,re.IGNORECASE if args.insensitive else 0)

    for fh in args.file:
        input_format = args.input_format or guess_format(fh.name)

        if not input_format:
            sys.exit(f'Please specify file format for "{fh.name}"')

        output_format = args.output_format or input_format

        for rec in read_fast_file(fh,input_format):
            if any(map(regex.search,[rec.id, rec.description])):
                write_fast_file(rec,args.outfile,output_format)


if __name__ == "__main__":
    main() 