#!/usr/bin/env python3
"""Overlap Graphs: Sequence assembly using shared k-mers."""
import argparse
from typing import NamedTuple, Optional, List, TextIO, Tuple
from collections import defaultdict
from Bio import SeqIO
import logging
from graphviz import Digraph
from pprint import pformat

class Args(NamedTuple):
    """Command-line arguments."""

    k_mers: Optional[int]
    fasta_file: TextIO
    debug: bool
    view: bool
    outfile:TextIO

def get_args() -> Args:
    """Get command-line."""

    parse = argparse.ArgumentParser(description="Overlap the sequences by the number common bases.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('file',metavar='FILE',help="Input FASTA file containing sequences to overlap.",type=argparse.FileType('rt'))

    parse.add_argument('-k','--k_mers',metavar='INT',type=int,help='Number of nucleotides to overlap the sequences.',default=3)

    parse.add_argument('-d','--debug',help="Debug",action='store_true')

    parse.add_argument('-o','--outfile',metavar='FILE',help="Output file name",default='graph_out')

    parse.add_argument('-v','--view',help="Display graphic.",action='store_true')
    
    args = parse.parse_args()

    if args.k_mers <1:
        parse.error(f'-k {args.k_mers} must be > 0')

    return Args(k_mers=args.k_mers,fasta_file=args.file,debug=args.debug,view=args.view,outfile=args.outfile)


def read_fasta_file(file:TextIO) -> List[Tuple[str,str]]:
    """ Read all sequences from a FASTA file. """
    
    records = SeqIO.parse(file,'fasta')
    sequeces = [ (record.id,record.seq) for record in records]
    return sequeces

def get_terminal_kmers(seq:str,k_mers:int) -> List[str]:
    """ Get the first and last k-mers of a sequence. """

    return [seq[0:k_mers],seq[-k_mers:]]

def match_sequences(seq1:list,seq2:list) -> Optional[list[str]]:
    """ Check whether two sequences overlap. """

    if seq1[1][0] == seq2[1][1]:
        return [seq2[0],seq1[0]]
    
def build_overlap_data(fasta:TextIO,k_mers:int) -> Tuple[
    dict[str, list[str]],
    dict[str, list[str]],
    list]:
    """ Generate dictionaires containing k-mers for each sequences. """

    sequences=[]
    starts,ends = defaultdict(list), defaultdict(list)
    fasta = read_fasta_file(fasta)
    for seq_id,seq in fasta:
        y=seq_id,get_terminal_kmers(str(seq),k_mers)
        starts[y[1][0]].append(seq_id)
        ends[y[1][1]].append(seq_id)
        sequences.append(y)
        
    return (starts,ends,sequences)
def find_overlaps(sequences:list) -> List[list[str]]:
    """ Find overlaps between all sequences. """

    overlaps = []
    for seq1 in sequences:
        for seq2 in sequences:
            if seq1[0] == seq2[0]:
                continue
            seq_id = match_sequences(seq1,seq2)
            if seq_id is not None:
                overlaps.append(seq_id)

    return overlaps

def create_logs(debug:bool,file:TextIO)->None:
    """ Create a log file to save the content about sequences. """

    logging.basicConfig(
        filename='.log',
        filemode='w',
        level=logging.DEBUG if debug else logging.CRITICAL
    )

    logging.debug('input file = "%s"',file.name)


def create_graph(overlap:list,outfile,view:bool)->None:
    """ Generate an overlap graph for the sequences. """

    dot = Digraph()
    for seq_ids in overlap: 
        dot.node(seq_ids[0])
        dot.node(seq_ids[1])
        dot.edge(seq_ids[0],seq_ids[1])
    dot.render(outfile,view=view,cleanup=True)

def main()->None:
    """ Run the code. """
    args = get_args() 

    create_logs(debug=args.debug,file=args.fasta_file)

    starts, ends, sequences=build_overlap_data(args.fasta_file,args.k_mers)

    logging.debug(f'Starts\n{pformat(starts)}')
    logging.debug(f'Ends\n{pformat(ends)}')

    overlap = find_overlaps(sequences)

    create_graph(overlap,outfile=args.outfile,view=args.view)

    for pair in overlap:
            print(pformat(pair))

    
if __name__ == "__main__":
    main()
