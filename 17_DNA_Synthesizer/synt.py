#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, List, Optional, Dict
import random
from Bio import SeqIO
from collections import Counter
from itertools import chain as ch


class Args(NamedTuple):
    """ Command line arguments. """

    file: List[TextIO]
    out_file: TextIO
    frmt: str
    number: int
    x_max: int
    m_min: int
    k_kmer:int
    seed: Optional[int]



WeightedChoice = Dict[str, float]
Chain = Dict[str, WeightedChoice]

def get_args() -> Args:
    """ Get command line arguments. """

    parse = argparse.ArgumentParser(description="",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('file', metavar='FILE', help="Input training file(s)", nargs= "+", type=argparse.FileType("rt"))

    parse.add_argument('-o','--out_file', metavar='FILE', help="The out_file's name", type=argparse.FileType("wt"), default="out.fa")

    parse.add_argument('-f','--frmt', metavar='format', type=str, help="Input file format", choices=['fasta', 'fastq'], default="fasta")

    parse.add_argument('-n', '--number', metavar='number', type=int, help="Number of sequences to create", default=100)

    parse.add_argument('-x', '--max', metavar='max',help="Maximum sequence length", default=75)

    parse.add_argument('-m', '--min', metavar='min', type=int, help="Minimum sequence length", default=15)
    
    parse.add_argument('-k', '--kmer',metavar='kmer', type=int, help="Size of k_mer", default=15)

    parse.add_argument('-s', '--seed', help='Random seed value', metavar='seed', type=int, default=None)
    args = parse.parse_args()

    return Args(file=args.file, out_file=args.out_file, frmt=args.frmt, number= args.number, x_max=args.max, m_min=args.min, k_kmer=args.kmer, seed=args.seed)


def read_file(files: list[TextIO], frt: str) -> List[str]:
    """ Read the file depends the format. """

    for fh in files:
        seq = [str(sequences.seq) for sequences in SeqIO.parse(fh,frt)]
    return seq

def find_kmers(seq: str, k:int) -> List[str]:
    """ Find k-mers in a sequence. """

    k_mers = [seq[i:i+k] for i in range(len(seq)-k+1)]
    return k_mers

def read_training(sequences:list[str], k:int) -> Chain:
    """ Tranining sequences, return dict of chains. """

    kmers = list(ch.from_iterable([find_kmers(seq,k) for seq in sequences]))

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

def gen_seq(chain: Chain, k:int, min_len: int, max_len: int) -> Optional[str]:
    """ Generate a sequence. """

    seq_leg = random.randint(min_len,max_len)
    sequence=''
    seq_add = random.choice(list(chain.keys()))
    sequence+=seq_add

    while len(sequence)<seq_leg:
        prev = sequence[-1*(k-1):]
        if prev in chain:
            nucleotide = chain[prev]
            letter_n = nucleotide.keys()
            porcent = nucleotide.values()
            select_nucleotide = random.choices(population=list(letter_n), weights= list(porcent), k=1)
            sequence+=select_nucleotide[0]
        else:
            select_nucleotide = random.choices(["A","C","G","T"])
            sequence+=select_nucleotide[0]

    return sequence




def main() -> None:
    """ Run code. """
    
    args = get_args()

    random.seed(args.seed)
    sequences = read_file(args.file, frt=args.frmt)
    chain = read_training(sequences,k=args.k_kmer)
    gen_sequence =[gen_seq(chain=chain,k=args.k_kmer+1,min_len=args.m_min,max_len=args.x_max)
                   for i in range(args.number)]
    print(gen_sequence)

if __name__ == "__main__":
    main()
