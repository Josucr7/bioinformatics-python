#!/usr/bin/env python3
from typing import NamedTuple, TextIO, List, Tuple, Optional
import argparse
import subprocess
from Bio import SeqIO
import re

class Args(NamedTuple):
    """Command-line Arguments."""

    file: TextIO
    out_file:str
    sequence:bool

def get_args() -> Args:
    """ Get command-line Arguments. """

    parse = argparse.ArgumentParser(argument_default="Finding protein N-glycosylation motifs from a file containing protein IDs.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('file',help="Input a FASTA file with ID proteins.",metavar='FILE',type=argparse.FileType('rt'))

    parse.add_argument('-d','--download_dir',help='Directory for downloads',metavar='DIR',type=str,default='fasta')

    parse.add_argument('-v','--view',help='Display sequences',action='store_true')

    args = parse.parse_args()

    return Args(file=args.file,out_file=args.download_dir,sequence=args.view)

def download_sequences_proteins(file:str,directory:str) -> str:
    """ Download protein amino acid sequences from a file containing protein IDs. """
    
    result = subprocess.run(
        ["bash","script.sh",file,directory],
        capture_output=True,
        text=True
    )
    return result.stdout

def return_ID_proteins(file:TextIO) -> List[str]:
    """ Get protein IDs from a file. """

    proteins = [prot_id for prot_id in map(str.rstrip,file)]
    return proteins

def get_sequence_protein(directory:str,id:str) -> Optional[str]:
    """ Get a protein sequence from a FASTA file. """

    out_file=f"test/{directory}/{id}.fasta"
    records = SeqIO.parse(out_file,'fasta')
    if rec := next(records,None):
        return str(rec.seq)

    return None

def glycosylation_motif(seq:str) -> Optional[Tuple[List[str],List[int]]]:
    """ Find N-glycosylation motifs in a protein sequence. """
    regex = re.compile('(?=(N[^P][ST][^P]))')
    coincidence = regex.findall(seq)
    locations = [match.start()+1 for match in regex.finditer(seq)]
    if coincidence and locations:
        return coincidence,locations
    return None

def main() -> None:
    """ Run the code. """
    args = get_args()
    prot_ids = return_ID_proteins(args.file)
    result = download_sequences_proteins(file=args.file.name,directory=args.out_file)
    print(result)
    for id in prot_ids:
        seq=get_sequence_protein(directory=args.out_file,id=id)
        if seq is not None:
            if ans := glycosylation_motif(seq):
                print(id)
                print(*ans[1])
                if args.sequence==True:
                    print(*ans[0])

if __name__=="__main__":
    main()