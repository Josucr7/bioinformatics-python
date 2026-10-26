#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO
import pandas as pd
import os


class Args(NamedTuple):
    """ Command-line Arguments. """

    hits: TextIO
    annotations: TextIO
    outfile: TextIO
    delimiter: str
    pctid: float

def get_args() -> Args:
    """ Get command-line arguments. """

    parse = argparse.ArgumentParser(description="Combine BLAST hits with sequence annotations", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('-b', '--blasthits', metavar='FILE', type=argparse.FileType('rt'), help='BLAST -outfmt 6', required=True)

    parse.add_argument('-a', '--annotations', metavar='FILE', type=argparse.FileType('rt'), help='Annotations file', required=True)

    parse.add_argument('-o', '--outfile', metavar='FILE', type=argparse.FileType('wt'), help='Output file', default='out.csv')

    parse.add_argument('-d', '--delimiter', metavar='DELIM', type=str, help='Output field delimiter', default='')

    parse.add_argument('-p', '--pctid', metavar='PCTID', type=float, help='Minimum percent identity', default=0.)

    args = parse.parse_args()

    return Args(hits=args.blasthits,annotations=args.annotations, outfile=args.outfile, delimiter=args.delimiter or guess_format(args.outfile.name), pctid=args.pctid)


def guess_format(filename:str) -> str:
    """ Determine the output delimiter from the file extension. """

    ext = os.path.splitext(filename)[1].lower()
    return ',' if ext == ".csv" else '\t' 

def read_write_panda(file_annotations:TextIO, file_hits:TextIO, pctid: float, out_file: TextIO, delimiter:str) -> str:
    """ Join BLAST hits with annotations and write filtered results. """

    annots_reader = pd.read_csv(file_annotations,sep=",",index_col='seq_id')

    hits = pd.read_csv(
        file_hits,
        sep=",",
        index_col='qseqid',
        names=['qseqid', 'sseqid', 'pident', 'length','mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
    )
    joined = hits[hits['pident']>= pctid].join(annots_reader,how='inner')

    joined.to_csv(
        out_file,
        index=True,
        columns=['pident', 'depth', 'lat_lon'],
        sep=delimiter
    )

    return f'Exported {joined.shape[0]:,} to "{out_file.name}".'

def main()-> None:
    """ Run code. """

    args = get_args()
    text = read_write_panda(file_annotations=args.annotations,file_hits=args.hits,pctid=args.pctid, out_file=args.outfile, delimiter=args.delimiter)
    print(text)


if __name__ == "__main__":
    main()