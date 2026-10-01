#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, List, Optional
import os
import random
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

class Args(NamedTuple):
    """ Command-line Arguments. """

    file: List[TextIO]
    i_format: str
    percent: float
    n_max: int
    seed: Optional[int]
    out_d:str


def get_args() -> Args:
    """ Get command-line arguments. """

    parse = argparse.ArgumentParser(description="Probabilistically subset FASTA files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('file', metavar='FILE', help="Input FASTA/Q file(s)", type=argparse.FileType('rt'), nargs= '+')

    parse.add_argument('-f', '--format', metavar="format", type=str, help='Input file format', choices=['fasta','fastq'], default='fasta')

    parse.add_argument('-p', '--percent', metavar='reads', type=float, help='Percent of reads', default=0.1)

    parse.add_argument('-m', '--max', metavar='max', type=int, help='Maximum number of reads', default=0)

    parse.add_argument('-s', '--seed', metavar='seed', type=int, help='Random seed value', default=None)

    parse.add_argument('-o', '--outdir', metavar='DIR', type=str, help='Output directory', default='out')
    
    args =  parse.parse_args()

    if not 0 < args.percent < 1:
        parse.error(f'--percent "{args.percent}" must be between 0 and 1')
    
    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)


    return Args(file=args.file, i_format=args.format, percent=args.percent, n_max=args.max, seed=args.seed, out_d=args.outdir)


def read_file(file:TextIO, frmt: str) -> List[Seq]:
    """ Read the file depends the format. """
    
    seq = [record.seq for record in SeqIO.parse(file,frmt)]
    return seq

def main() -> None:
    """ Run code. """

    args = get_args()

    if args.seed is not None:
        random.seed(args.seed)
    
    total_num = 0
    for file in args.file:
        out_file = os.path.join(args.out_d,os.path.basename(file.name))
        records = read_file(file=file,frmt=args.i_format)
        count = 0
        with open(out_file,'wt') as ot:
            for seq in records:
                ran_num = random.random()
                if ran_num <= args.percent:
                    sequence = SeqRecord(seq, id=str(count+1), description="")
                    SeqIO.write(sequence, ot, 'fasta')
                    count+=1
                if args.n_max > 0 and count == args.n_max:
                    break
        total_num += count

    
    print(f'Wrote {total_num:,} sequence{"" if total_num == 1 else "s"} '
          f'from {len(args.file):,} file{"" if len(args.file) == 1 else "s"} '
          f'to directory "{args.out_d}".')

if __name__ == "__main__":
    main()