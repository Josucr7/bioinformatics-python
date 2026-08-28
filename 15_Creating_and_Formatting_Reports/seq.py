#!/usr/bin/env python3
import argparse
from typing import NamedTuple, TextIO, List, Optional
from tabulate import tabulate
from Bio import SeqIO
import numpy as np

class Args(NamedTuple):
    """ Command-line arguments. """

    file: List[TextIO]
    
    tablefmt: str

class FastaInfo(NamedTuple):
    """ FASTA file information. """

    filename: str
    min_len: int
    max_len: int
    avg_len: float
    num_seqs: int


def get_args() -> Args:
    """ Get command-line arguments. """

    parser = argparse.ArgumentParser(description='Mimic SeqMagick',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',metavar="FILE",help="Input FASTA file(s).",nargs='+',type=argparse.FileType('rt'))

    parser.add_argument('-t','--tablefmt',metavar='TABLE',type=str,help="Table format", choices=['plain', 'simple', 'grid', 'pipe', 'orgtbl', 'rst','mediawiki', 'latex', 'latex_raw', 'latex_booktabs'],default='plain')

    args = parser.parse_args()

    return Args(file=args.file,tablefmt=args.tablefmt)

def read_fasta_file(file: TextIO)->Optional[List[str]]:
    """ Read a FASTA file. """
    
    seq = [str(sequence.seq) for sequence in SeqIO.parse(file,'fasta')]
    if seq:
        return seq
    return None   

def process(fh:TextIO) -> FastaInfo:
    """ Process a FASTA file and return its statistics. """

    if rec := read_fasta_file(fh):
        if lengths:= [len(seq) for seq in rec]:
            return FastaInfo(
                filename=fh.name,
                min_len=min(lengths),
                max_len=max(lengths),
                avg_len=round(float(np.mean(lengths)), 2),
                num_seqs=len(lengths)
            )
    return FastaInfo(
                filename=fh.name,
                min_len=0,
                max_len=0,
                avg_len=0.,
                num_seqs=0)

def main () -> None:
    """Run code. """
    args = get_args()
    hdr = ['name','min_len','max_len','avg_len','num_seqs']
    dates = [process(fh) for fh in args.file]
    print(tabulate(dates, headers=hdr, tablefmt=args.tablefmt, floatfmt='.2f'))


if __name__ == "__main__":
    main()