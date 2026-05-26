import argparse
from typing import NamedTuple

class Args(NamedTuple):
    """Command line-Arguments"""

    mrna : str

def get_args() -> Args:
    """ Get command line-arguments """

    parse = argparse.ArgumentParser(description="Traduction of mRNA sequences to protein sequence.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument("mRNA",metavar="RNA",type=str,help="Input a mRNA sequence.")

    args = parse.parse_args()

    return Args(mrna=args.mRNA)

def identify_aminoacid(codon:str) -> str:
    """ Translate the codon of nucleotides in their aminoacid """

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

def range_codons(sequence:str) -> list:
    """ Create a range to select the codons in the sequence """

    return list(range(0,len(sequence),3))

def list_codons(sequence:str) -> list:
    """ Generate a codon's list of a RNA sequence """

    num_range = range_codons(sequence)
    codons_sequence = [sequence[i:i+3].upper() for i in num_range]

    return codons_sequence



def main()->None:
    """ Run the code """

    args = get_args()
    
    codons_seguence=list_codons(args.mrna)
    
    protein = list(filter(None,map(identify_aminoacid,codons_seguence)))

    print(protein)


if __name__=="__main__":
    main()


