#!/usr/bin/env python3
""" Hamming Distance of two DNA sequences. """

import argparse
from typing import NamedTuple, Optional, TextIO, Tuple
from Bio import SeqIO

class Args(NamedTuple):
    """Command line Arguments."""

    seq1: Optional[str]
    seq2: Optional[str]
    file: Optional[TextIO]

def get_args() -> Args:
    """Get command line Arguments."""

    parser = argparse.ArgumentParser(description="Hamming distance in sequences.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-s1','--sequence_1',metavar='STR',help="Input a DNA sequence.")

    parser.add_argument('-s2','--sequence_2',metavar='STR',help="Input a DNA sequence to compare.")

    parser.add_argument('-f',"--file",metavar='FILE',help="Input a FASTA file with two DNA sequences to compare.",nargs='?',type=argparse.FileType("rt"))

    args = parser.parse_args()

    return Args(seq1=args.sequence_1,seq2=args.sequence_2,file=args.file)


def read_fasta_file(file:TextIO) -> Tuple[str,str]:
    """Read FASTA files and return two DNA sequences."""

    records = SeqIO.parse(file,'fasta')
    sequences =  [str(record.seq) for record in records]

    if len(sequences) < 2:
        raise ValueError("The FASTA file must contain two sequences.")

    seq1, seq2 = sequences

    return seq1,seq2


def hamm_value(value:int,seq1:str,seq2:str)->int:
    """Calculate the Hamming distance."""

    return (max(len(seq1),len(seq2))-value)

def matching_bases(seq1:list,seq2:list) -> int:
    """Calculate matching nucleotides between two sequences."""
    
    match = 0
    for a,b in zip(seq1,seq2):
        if a == b:
            match+=1
    
    return match


def alignment_seq(seq1:str,seq2:str) -> int:
    """Align sequences to find the best Hamming distance."""

    hamm_align = 0
    conditional_1 = True
    conditional_2 = False

    seq_1 = [nucleotide.upper() for nucleotide in seq1]
    seq_2 = [nucleotide.upper() for nucleotide in seq2]

    
    while conditional_1:
        hamm = matching_bases(seq_1,seq_2)
        if hamm > hamm_align:
            hamm_align = hamm
        
        seq_2.insert(0,"-")

        if seq_2.count("-")==len(seq_1):
            conditional_1 = False
            conditional_2 = True
    
    seq_1 = [nucleotide.upper() for nucleotide in seq1]
    seq_2 = [nucleotide.upper() for nucleotide in seq2]

    while conditional_2:
        hamm = matching_bases(seq_1,seq_2)
        if hamm > hamm_align:
            hamm_align = hamm
        
        seq_1.insert(0,"-")
        if seq_1.count("-")==len(seq_2):
            conditional_1 = False
            conditional_2 = False
    

    return hamm_value(hamm_align,seq1,seq2)

        

def main() -> None:
    """Run the code."""
    
    args = get_args()
    
    if args.file:
        sequences = read_fasta_file(args.file)
        seq1 = sequences[0]
        seq2 = sequences[1]
    else:
        seq1 = args.seq1
        seq2 = args.seq2

        if seq1 is None or seq2 is None:
            raise ValueError("Provide two sequences or a FASTA file.")

    print(alignment_seq(seq1,seq2))

if __name__ == "__main__":
    main()