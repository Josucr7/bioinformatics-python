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

def dna_to_aa(dna:str) -> Tuple[str]:
    """ From DNA sequence translate to aminoacid sequence.  """
    rna = Seq.transcribe(dna)
    rna_reverse = Seq.reverse_complement_rna(rna)
    aa = Seq.translate(rna)
    aa_1 = Seq.translate(rna[1:])
    aa_2 = Seq.translate(rna[2:])
    aar = Seq.translate(rna_reverse)
    aar_1 = Seq.translate(rna_reverse[1:])
    aar_2 = Seq.translate(rna_reverse[2:])
    return aa,aar,aa_1,aar_1,aa_2,aar_2

def truncate(seq: str, k: int) -> str:
    """ Truncate a sequence to even division by k """

    return ''
def find_orfs(aa: str) -> List[str]:
    """ Find ORFs in AA sequence """

    regex = re.compile('(?=(M[A-Z]*[*$]))')
    coincidence = regex.findall(aa)
    return coincidence

def main() -> None:
    """ Run code. """

    args = get_args()
    sequence = read_fasta_file(args.file)
    aa = dna_to_aa(sequence)
    orf = [find_orfs(seq) for seq in aa ] 
    result = set(itertools.chain.from_iterable(orf))
    print(*result)

if __name__ == "__main__":
    main()