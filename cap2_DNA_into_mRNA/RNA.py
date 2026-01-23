#!/usr/bin/env python3
"""Translate a DNA sequence into RNA sequence."""
import argparse
import os 
from typing import NamedTuple, List, TextIO


class Args(NamedTuple):
    """Command line Arguments"""
    file : List[TextIO]
    out_dir : str

def get_args()->Args:
    """Get command line arguments"""
    parser = argparse.ArgumentParser(description='Translate a DNA sequence into RNA sequence.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',metavar='FILE',help='Input DNA file(s)',nargs='+',type=argparse.FileType('rt'))

    parser.add_argument('-o','--out_dir',help='Output Directory',default='Out',type=str)

    args = parser.parse_args()

    return Args(file=args.file,out_dir=args.out_dir)


def dna_to_rna(dna:str)->str:
    """Translate DNA sequence to RNA sequence."""
    return dna.upper().replace('T','U')

def process_file(fh,out_dir:str)->int:
    """Translate DNA sequences in one file and write RNA output."""
    out_file=os.path.join(out_dir,os.path.basename(fh.name))
    num_seq=0
    with open(out_file,'wt') as out_fh:
        for dna in fh:
            num_seq+=1
            print(dna_to_rna(dna),end='',file=out_fh)

    return num_seq

def plural(num:int)->str:
    """Return a singular or plural depends by number of files and sequences."""
    return '' if num==1 else 's'

def main()->None:
    """Translate DNA sequences to RNA and write output files."""
    args=get_args()
    
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    
    num_file=0
    num_seq=0
    for fh in args.file:
        num_file+=1
        num_seq+=process_file(fh,args.out_dir)
    print(f'Done, wrote {num_seq} sequence{plural(num_seq)} in {num_file} file{plural(num_file)}.')

if __name__=="__main__":
    main()