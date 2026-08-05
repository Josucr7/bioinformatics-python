#!/usr/bin/env python3
from typing import NamedTuple, TextIO, List, Tuple
import argparse
import subprocess
from Bio import SeqIO
import re
from pprint import pformat
class Args(NamedTuple):
    """Command-line Arguments."""

    file: TextIO
    out_file:str

def get_args() -> Args:
    """ Get command-line Arguments. """

    parse = argparse.ArgumentParser(argument_default="Finding the protein N-glycosylation motif of a FASTA file contains lists ID protein.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('file',help="Input a FASTA file with ID proteins.",metavar='FILE',type=argparse.FileType('rt'))

    parse.add_argument('-d','--download_dir',help='Directory for downloads',metavar='DIR',type=str,default='fasta')

    args = parse.parse_args()

    return Args(file=args.file,out_file=args.download_dir)

def download_sequences_proteins(file:str,directory:str) -> str:
    """ Download aminoacid sequences from a file that contains ID proteins. """
    
    result = subprocess.run(
        ["bash","script.sh",file,directory],
        capture_output=True,
        text=True
    )
    return result.stdout

def return_ID_proteins(file:TextIO) -> str:
    """ Get ID proteins from a file. """

    proteins = [prot_id for prot_id in map(str.rstrip,file)]
    return proteins

def get_sequenece_protein(directory:str,id:str) -> List[str]:
    """ Get sequence protein from a FASTA file. """

    out_file=f"test/{directory}/{id}.fasta"
    records = SeqIO.parse(out_file,'fasta')
    sequence=[str(record.seq) for record in records]
    return sequence

def glycosylation_motif(seq:str) -> Tuple[List[str],List[int]]:
    """ Find N-glycosylation motif from a protein sequence. """
    regex = re.compile(('N[^P][ST][^P]'))
    coincidence = regex.findall(seq)
    locations = [match.start()+1 for match in regex.finditer(seq)]
    return coincidence,locations


def main() -> None:
    """ Run the code. """
    args = get_args()
    prot_ids = return_ID_proteins(args.file)
    for prot_id in prot_ids:
        print(f'http://www.uniprot.org/uniprot/{prot_id}.fasta')

    result = download_sequences_proteins(file=args.file.name,directory=args.out_file)
    print(result)
    for id in prot_ids:
        sequences=get_sequenece_protein(directory=args.out_file,id=id)
        for seq in sequences:
            ans = glycosylation_motif(seq)
            print(ans)

if __name__=="__main__":
    main()