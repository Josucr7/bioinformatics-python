#!/usr/bin/env python

"""Content Guanine an Cytosine in Fasta Files with DNA sequences."""

import argparse
from typing import NamedTuple,List,TextIO,Iterator, Tuple
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import os

class Args(NamedTuple):
    """Command line Arguments."""

    out_dir: str
    file: List[TextIO]

def get_args()->Args:
    """Get commmand line Arguments."""

    parser = argparse.ArgumentParser(description='Generate outfile(s) with the content of guanine and cytosine for every Fasta file.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('file',metavar='FILE',help='Input Fasta file(s).',nargs='+',type=argparse.FileType('rt'))

    parser.add_argument('--out','-o',metavar='OUT',help='Input output directory.', default='Out',type=str)

    args = parser.parse_args()

    return Args(file=args.file,out_dir=args.out)

def calc_gc(seq:str)->float:
    """Calculate the porcentual content of guanine and cytosine in a DNA sequence."""

    seq = seq.upper()
    return 0.0 if len(seq)==0 else ((seq.count('G') + seq.count('C')) / len(seq)) * 100           

def read_fasta_file(doc:TextIO)->Iterator[SeqRecord]:
    """Detetct the Fasta sequences in a file."""
    
    seq = SeqIO.parse(doc,'fasta')
    return seq
                               
def created_output_file(doc:TextIO,out_dir:str)->str:
    """Create the output file path."""

    out_file = os.path.join(out_dir,os.path.basename(doc.name))
    return out_file

def max_seq_GC(file)->Tuple[str,float]:
    """Select the sequence with more GC porcentual."""

    max_GC=0.0
    seq=''
    for fasta in read_fasta_file(file):
        gc=calc_gc(fasta.seq)
        if gc>max_GC:
            max_GC=gc
            seq=fasta.id
    return (seq,max_GC)
def plural(num:int)->str:
    """Return a sungular or plural depends of number of files and seuquences."""

    return '' if num == 1 else 's'

def main()->None:
    """Run the code."""

    args = get_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    fastas = 0
    files = 0

    for doc in args.file:
        files += 1
        out_file=created_output_file(doc,args.out_dir)
        with open(out_file,'wt') as out_fh:
            max_seq,max_gc=max_seq_GC(doc)
            print(f'The Fasta sequence with highest GC content is {max_seq} with {max_gc:.4f}',file=out_fh)
            doc.seek(0)
            for seq in read_fasta_file(doc):
                fastas += 1
                gc = calc_gc(seq.seq)
                print(f'{seq.id}\t{gc:.2f}',file=out_fh)

    print(f'Done, wrote {fastas} Fasta sequence{plural(fastas)} in {files} file{plural(files)} in directory {args.out_dir}.')


    


if __name__ == '__main__':
    main()



