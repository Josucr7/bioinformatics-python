#!/usr/bin/env python3
import argparse
from typing import NamedTuple, TextIO, Optional, Tuple, List
from Bio import SeqIO, Seq
import re
import itertools

class Args(NamedTuple):
    """ Command line-Arguments."""

    file: TextIO

def get_args() -> Args:
    """ Get command line-Arguments. """

    parse = argparse.ArgumentParser(description="Detect region of nucleotides that transcribe amino acid sequences.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument("file",metavar="FILE",help="Input a FASTA file.",type=argparse.FileType('rt'))

    args = parse.parse_args()
    
    return Args(file=args.file)

def read_fasta_file(file:TextIO) -> Optional[str]:
    """ Read a fasta file. """

    records = SeqIO.parse(file,"fasta")
    sequence = next(records,None)
    if sequence is not None:
        return str(sequence.seq)
    return None

def dna_to_aa(dna:str) -> List[str]:
    """ From DNA sequence translate to aminoacid sequence.  """
    rna = Seq.transcribe(dna)
    rna_reverse = Seq.reverse_complement_rna(rna)
    aa = []
    for seq in rna,rna_reverse:
        for i in range(3):
            if prot := Seq.translate(truncate(seq[i:],3)):
                aa.append(prot)

    return aa

def truncate(seq: str, k: int) -> str:
    """ Truncate a sequence to even division by k """

    length = len(seq)
    end = length - (length % k)
    return seq[:end]
    
def find_orfs(aa: str) -> str:
    """ Find ORFs in AA sequence """

    regex = re.compile('(?=(M[A-Z]*[*$]))')
    coincidence = regex.findall(aa)
    return coincidence

def main() -> None:
    """ Run code. """

    args = get_args()
    sequence = read_fasta_file(args.file)
    aa = dna_to_aa(sequence)
    orfs = set()
    for sequence in aa:
        for orf in (find_orfs(sequence)):
            orfs.add(orf)
    
    print(*orfs,'\n')

if __name__ == "__main__":
    main()