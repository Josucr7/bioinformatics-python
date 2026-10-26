#!/usr/bin/env python3

import argparse
from typing import NamedTuple, TextIO
import csv
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

def read_write_csv(file_annotations:TextIO, file_hits:TextIO, pctid: float, out_file: TextIO, delimiter:str) -> int:
    """ Join BLAST hits with annotations and write filtered results. """

    annots_reader = csv.DictReader(file_annotations,delimiter=",")
    annots = {annot['seq_id']:annot for annot in annots_reader}

    writer = csv.DictWriter(out_file, fieldnames=['qseqid', 'pident', 'depth', 'lat_lon'], delimiter=delimiter)
    writer.writeheader()

    hits = csv.DictReader(
        file_hits,
        delimiter=",",
        fieldnames=['qseqid', 'sseqid', 'pident', 'length','mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
    )
    num_written = 0
    for hit in hits:
        if float(hit.get('pident', -1)) < pctid:
            continue
        if seq_id := hit.get("qseqid"):
            if seq := annots.get(seq_id):
                num_written+=1
                writer.writerow({'qseqid': seq_id,
                                  'pident': hit.get('pident'),
                                    'depth': seq.get('depth'),
                                      'lat_lon': seq.get('lat_lon')

                })
    return num_written

def main()-> None:
    """ Run code. """

    args = get_args()
    value = read_write_csv(file_annotations=args.annotations,file_hits=args.hits,pctid=args.pctid, out_file=args.outfile, delimiter=args.delimiter)
    print(f'Exported {value:,} to "{args.outfile.name}".')


if __name__ == "__main__":
    main()