#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, List, Optional, Dict
import random
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from collections import Counter
from itertools import chain as ch
import sys


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

    parse.add_argument('-f','--format', metavar='format', type=str, help="Input file format", choices=['fasta', 'fastq'], default="fasta")

    parse.add_argument('-n', '--number', metavar='number', type=int, help="Number of sequences to create", default=100)

    parse.add_argument('-x', '--max', metavar='max',help="Maximum sequence length", type= int, default=75)

    parse.add_argument('-m', '--min', metavar='min', type=int, help="Minimum sequence length", default=50)
    
    parse.add_argument('-k', '--kmer',metavar='kmer', type=int, help="Size of k_mer", default=10)

    parse.add_argument('-s', '--seed', help='Random seed value', metavar='seed', type=int, default=None)

    args = parse.parse_args()

    return Args(file=args.file, out_file=args.out_file, frmt=args.format, number= args.number, x_max=args.max, m_min=args.min, k_kmer=args.kmer, seed=args.seed)


def read_file(files: list[TextIO], frt: str) -> List[str]:
    """ Read the file depends the format. """

    seq = []
    for fh in files:
        seq.extend(str(record.seq) for record in SeqIO.parse(fh, frt))
    return seq

def find_kmers(seq: str, k:int) -> List[str]:
    """ Find k-mers in a sequence. """

    k_mers = [seq[i:i+k] for i in range(len(seq)-k+1)]
    return [] if len(seq)-k+1 < 1 else k_mers

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

    return sequence if len(sequence) >= min_len else None

def write_file(sequences:list[str], outfile:str, fmt: str) -> None:
    """ Generate a file. """
    record = []
    for value, seq in enumerate(filter(None,sequences)):
        seq_r = SeqRecord(Seq(seq),id=str(value+1),description="")

        if fmt.lower() == 'fastq':
            seq_r.letter_annotations["phred_quality"] = [40] * len(seq)
        
        record.append(seq_r)
    
    SeqIO.write(record,outfile,fmt)


def main() -> None:
    """ Run code. """
    
    args = get_args()

    if args.seed is not None:
        random.seed(args.seed)

    sequences = read_file(args.file, frt=args.frmt)

    if chain := read_training(sequences,k=args.k_kmer):
        gen_sequence =[gen_seq(chain=chain,k=args.k_kmer+1,min_len=args.m_min,max_len=args.x_max)
                       for i in range(args.number)]
        write_file(sequences=gen_sequence,outfile=args.out_file,fmt=args.frmt)
        print(f'Done, see output in "{args.out_file.name}"')
    else:
        sys.exit(f'No {args.k_kmer}-mers in input sequences.')

if __name__ == "__main__":
    main()
