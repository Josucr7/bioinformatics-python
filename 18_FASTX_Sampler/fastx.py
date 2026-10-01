import argparse
from typing import NamedTuple, TextIO, List, Optional

class Args(NamedTuple):
    """ Command-line Arguments. """

    file: List[TextIO]
    i_format: str
    percent: float
    n_max: int
    seed: Optional[int]
    out_d:str


def get_args() -> Args:
    """ Get command-line arguments. """

    parse = argparse.ArgumentParser(description="Probabilistically subset FASTA files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parse.add_argument('file', metavar='FILE', help="Input FASTA/Q file(s)", type=argparse.FileType('rt'), nargs= '+')

    parse.add_argument('-f', '--format', metavar="format", type=str, help='Input file format', choices=['fasta','fastq'], default='fasta')

    parse.add_argument('-p', '--percent', metavar='percent', type=float, help='Percent of reads', default=0.1)

    parse.add_argument('-m', '-- max', metavar='max', type=int, help='Maximum number of reads', default=0)

    parse.add_argument('-s', '--seed', metavar='seed', type=int, help='Random seed value', default=None)

    parse.add_argument('-o', '--outdir', metavar='DIR', type=str, help='Output directory', default='out')

    args =  parse.parse_args()

    return Args(file=args.file, i_format=args.format, percent=args.percent, n_max=args.max, seed=args.seed, out_d=args.outdir)


def main() -> None:
    """ Run code. """

    args = get_args()


if __name__ == "__main__":
    main()