#!/usr/bin/env python3

import argparse
from typing import NamedTuple, List
import os
import math
from functools import reduce
class Args(NamedTuple):
    """ Command lina-arguments. """

    protein: str
    modulo: int
    all:bool

def get_args() -> Args:
    """ Get command line arguments. """

    parse = argparse.ArgumentParser(description='Find the number of mRNA could produce a given protein sequence.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('protein',help="Input a file with protein sequence.",metavar="str",type=str)

    parse.add_argument('-m','--modulo',help="Modulo value",metavar="INT",type=int,default=1000000)

    parse.add_argument('-a','--all',help="Show all combinations.",action='store_true')

    args = parse.parse_args()

    if os.path.isfile(args.protein):
        args.protein = open(args.protein).read().rstrip()

    return Args(protein=args.protein,modulo=args.modulo,all=args.all)

aa_to_mrna = {
    '*': ['UAA', 'UAG', 'UGA'],  # Stop Codons
    'A': ['GCA', 'GCC', 'GCG', 'GCU'],
    'C': ['UGC', 'UGU'],
    'D': ['GAC', 'GAU'],
    'E': ['GAA', 'GAG'],
    'F': ['UUC', 'UUU'],
    'G': ['GGA', 'GGC', 'GGG', 'GGU'],
    'H': ['CAC', 'CAU'],
    'I': ['AUA', 'AUC', 'AUU'],
    'K': ['AAA', 'AAG'],
    'L': ['CUA', 'CUC', 'CUG', 'CUU', 'UUA', 'UUG'],
    'M': ['AUG'],  # Start Codon
    'N': ['AAC', 'AAU'],
    'P': ['CCA', 'CCC', 'CCG', 'CCU'],
    'Q': ['CAA', 'CAG'],
    'R': ['AGA', 'AGG', 'CGA', 'CGC', 'CGG', 'CGU'],
    'S': ['AGC', 'AGU', 'UCA', 'UCC', 'UCG', 'UCU'],
    'T': ['ACA', 'ACC', 'ACG', 'ACU'],
    'V': ['GUA', 'GUC', 'GUG', 'GUU'],
    'W': ['UGG'],
    'Y': ['UAC', 'UAU']
}

def detect_codon(aa:str) -> int:
    """ From a amino acid detect the posible codon's combinations . """

    if aa.upper() in aa_to_mrna:
        return len(aa_to_mrna[aa.upper()])

def posibles_mrna(seq:str) -> list:
    """ Detect every posible codon for a sequences, there add the stop codons. """

    values = [detect_codon(aa) for aa in seq]
    values.append(3)
    return values

def product(values:list) -> int:
    """ Calculate the number of combinations of every codon to mrna. """

    return math.prod(values)

def mulmod(a: int, b: int, mod: int) -> int:
    """ Multiplication with modulo """

    def maybemod(x):
        ret = (x % mod) if mod > 1 and x > mod else x
        return ret or x
    res = 0
    a = maybemod(a)
    while b > 0:
        if b % 2 == 1:
            res = maybemod(res + a)
        a = maybemod(a * 2)
        b //= 2
    return res

def modprod(xs: List[int], modulo: int) -> int:
    """ Return the product modulo a value """

    return reduce(lambda x, y: mulmod(x, y, modulo), xs, 1)

def main() -> None:
    """ Run code. """

    args = get_args ()
    values = posibles_mrna(args.protein)
    res=modprod(xs=values,modulo=args.modulo)
    result = product(values)
    if args.all:
        print(result)
    print(res)

if __name__ == "__main__":
    main()