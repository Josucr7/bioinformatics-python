#!/usr/bin/env python3
""" Translation of an mRNA sequence into a protein. """

import argparse
from typing import NamedTuple,Optional


class Args(NamedTuple):
    """ Command line-arguments. """

    mrna: str

def get_args() -> Args:
    """ Get command line-arguments. """

    parse = argparse.ArgumentParser(description="Translation of mRNA sequences to protein sequence.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument("mRNA",metavar="RNA",type=str,help="Input a mRNA sequence.")

    args = parse.parse_args()

    return Args(mrna=args.mRNA)

def identify_amino_acid(codon:str) -> Optional[str]:
    """ Translate an RNA codon into its amino acid. """

    rna_codon_to_aminoacid = {
        'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
        'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
        'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
    
        'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }
    if codon not in rna_codon_to_aminoacid:
        return None

    return rna_codon_to_aminoacid[codon]

def range_codons(sequence:str) -> list[int]:
    """ Generate to index positions for codons. """

    return list(range(0,len(sequence),3))

def list_codons(sequence:str) -> list[str]:
    """ Generate a list of codons from an RNA sequence. """

    num_range = range_codons(sequence)
    codons_sequence = [sequence[i:i+3].upper() for i in num_range]

    return codons_sequence


def main() -> None:
    """ Run the code. """

    args = get_args()
    
    codons_sequence=list(enumerate(list_codons(args.mrna)))
    proteins = []
    
    for number,codon in codons_sequence:
        if codon == "AUG":
            codons_sequence = codons_sequence[number:]
            break

    if codons_sequence and "AUG" == codons_sequence[0][1]:
        for number,codon in codons_sequence:
            protein = identify_amino_acid(codon)
            if protein == "*":
                break
            proteins.append(protein)

    print("".join(proteins))


if __name__=="__main__":
    main()