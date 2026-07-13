#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO, List, Dict,Callable
from Bio import SeqIO
from functools import partial
from math import ceil
from collections import Counter
from itertools import chain
from pprint import pformat
class Args(NamedTuple):
    """ Command-line Arguments."""

    file: TextIO

def get_args()-> None:
    """Get command-line arguments. """

    parse = argparse.ArgumentParser(description='The project finding the longest shared subsequence in a FASTA file',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('file',help='Input a FASTA file containing DNA sequences',metavar='FASTA',type=argparse.FileType('rt'))

    args = parse.parse_args()

    return Args(file=args.file)

def read_fasta_file(file:TextIO) -> List[str]:
    """ Read a FASTA file and take their ID and DNA sequences. """

    records=SeqIO.parse(file,'fasta')
    sequences = [(str(record.seq)) for record in records]
    return sequences

def shorter_seq(sequences:list[str]) -> int:
    """ Identify the lenght for every sequence. """
    if len(sequences) != 0:
        return min(list(map(len,sequences)))
    else:
        return 0

def find_kmers(sequence:str,k_mer:int) -> List[str]:
    """ Extract the k_mers of a DNA sequences. """

    n = len(sequence) - k_mer + 1
    return [] if n<1 else [sequence[i:i+k_mer] for i in range(n)]

def frequency_subseq(k_mers:list)->Dict[str,int]:
    """ Return a dictionary containig the frequency of k_mers. """

    return Counter(chain.from_iterable(k_mers))

def find_max_subseq(sequences:list,k_mer:int) -> List[str]:
    """ Return the subsequences that are in all sequences. """

    k_mers = [set(find_kmers(sequence,k_mer)) for sequence in sequences]
    counts = frequency_subseq(k_mers)
    n = len(sequences)
    return [kmer for kmer,freq in counts.items() if freq == n]

def binary_search(f:Callable,low:int,high:int) -> int:
    """ Find the value where have common subsequnces by binary search. """

    h, l = f(high), f(low)
    mid = (high+low) // 2

    if h and l:
        return high

    if h and not l:
        return (binary_search(f,low=mid,high=high))

    if l and not h:
        return (binary_search(f,low=low,high=mid))

    return -1

def start(sequences:List[str],short:int) -> int:
    """ Return starting point to earch common sequences. """

    common = partial(find_max_subseq,sequences)
    return binary_search(common,low=1,high=short)

def main () -> None:
    """ Run the code. """

    args = get_args()
    sequences = read_fasta_file(args.file)
    value_min = shorter_seq(sequences)
    value_start = start(sequences,value_min)
    if value_min >=0 and value_min != 0:
        candidates=[]
        common = partial(find_max_subseq,sequences)
        for k in range(value_start,value_min+1):
            if k_mers:= common(k):
                candidates.append(k_mers)
            else:
                break
        if len(candidates[0][0])==0:
            print("No common subsequences.")
        else:
            print(f'The subsequences are {pformat(candidates)}')
            print(f'The longest common subsequences are {max(candidates,key=len)}')
    else:
        print("Don't have sequences the FASTA file.")

if __name__ == "__main__":
    main()