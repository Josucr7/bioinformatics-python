#!/usr/bin/env python
""" Translation mRNA sequence into protein using Biopython. """

import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from typing import TextIO,NamedTuple,Optional,List


class Args(NamedTuple):
    """ Command-line arguments. """
    mrna: Optional[str]
    file: Optional[TextIO]

def get_args() -> Args:
    """ Get command-line arguments. """

    parser =  argparse.ArgumentParser(description="Translation of mRNA sequences to protein sequence.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-s","--sequence",metavar="STR",help="Input a mRNA sequence")

    parser.add_argument("-f","--file",metavar="FILE",help="Input a FASTA file with a RNA sequence.",type=argparse.FileType("rt"))

    args = parser.parse_args()

    return Args(mrna=args.sequence,file=args.file)

def read_fasta_file(file:TextIO) -> List[str]:
    """ Get the sequence mRNA of a FASTA file. """
    
    records = SeqIO.parse(file,"fasta")
    sequences = [str(record.seq) for record in records]

    return sequences


def translation(sequence:str) -> Seq:
    """ Translation mRNA sequence into protein. """

    protein = Seq(sequence).translate()
    return protein

def main() -> None:
    """Run the code. """
    
    args = get_args()

    if args.file is None and args.mrna is None:
        raise ValueError("Input a Fasta File or an mRNA sequence.")
    
    if args.file:
        sequences = read_fasta_file(args.file)
    else:
        sequences = [args.mrna]
        
    proteins = [translation(sequence) for sequence in sequences]
   
    print(proteins)


if __name__=="__main__":
    main()