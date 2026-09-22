#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, List, Optional, Dict
import random
from Bio import SeqIO
from collections import Counter


class Args(NamedTuple):
    """ Command line arguments. """

    file: List[TextIO]
    out_file: TextIO
    input_format: str
    number: int
    x_max: int
    m_min: int
    k_kmer:int
    seed: Optional[int]

class Markov(NamedTuple):
    """ Machine Learning. """
    

    

def get_args() -> Args:
    """ Get command line arguments. """

    parse = argparse.ArgumentParser(description="",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('file', metavar='FILE', help="Input training file(s)", nargs= "+", type=argparse.FileType("rt"))

    parse.add_argument('-o','--out_file', metavar='FILE', help="The out_file's name", type=argparse.FileType("wt"), default="out.fa")

    parse.add_argument('-f','--format', metavar='format', type=str, help="Input file format", choices=['fasta', 'fastq'], default="fasta")

    parse.add_argument('-n', '--number', metavar='number', type=int, help="Number of sequences to create", default=100)

    parse.add_argument('-x', '--max', metavar='max',help="Maximum sequence length", default=75)

    parse.add_argument('-m', '--min', metavar='min', type=int, help="Minimum sequence length", default=15)
    
    parse.add_argument('-k', '--kmer',metavar='kmer', type=int, help="Size of k_mer", default=15)

    parse.add_argument('-s', '--seed', help='Random seed value', metavar='seed', type=int, default=None)
    args = parse.parse_args()

    return Args(file=args.file, out_file=args.out_file, input_format=args.format, number= args.number, x_max=args.max, m_min=args.min, k_kmer=args.kmer, seed=args.seed)


def read_file(file: TextIO, frt: str)  :
    """ Read the file depends the format. """

    seq = [str(sequences.seq) for sequences in SeqIO.parse(file,'fasta')]
    return seq

def find_kmers(seq: str, k:int) -> List[str]:
    """ Find k-mers in a sequence. """

    k_mers = [seq[i:i+k] for i in range(len(seq)-k+1)]
    return k_mers

def read_training(seq:str, k:int) -> Dict[str,Dict[str,float]]:
    """ Tranining sequences, return dict of chains. """

    kmers = find_kmers(seq,k)

    chain = {}
    for i in range(len(kmers)-1):
        if kmers[i] in chain:
            chain[kmers[i]].append(kmers[i+1][-1])
        else:
            chain[kmers[i]]=[]
            chain[kmers[i]].append(kmers[i+1][-1])

    for key,value in chain.items():
        choices = Counter(value)
        total = choices.total()
        porcent = {nucleotide: value/total for nucleotide,value in choices.items()}
        chain[key]=porcent
    return chain 



def main() -> None:
    """ Run code. """
    
    args = get_args()

    #random.seed(args.seed)
    for fh in args.file:
        seq = read_file(fh, frt='fasta')
        print(read_training(seq=seq[0],k=3))

if __name__ == "__main__":
    main()
