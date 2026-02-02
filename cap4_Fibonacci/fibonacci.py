#!/usr/bin/env python3

import argparse
from typing import NamedTuple,Generator



class Args(NamedTuple):
    """Command line argumnets."""

    generations:int

    litter:int

def get_args()->Args:
    """Get commmand line arguments."""

    parser = argparse.ArgumentParser(description="Generation of last number of a Fibonacci sequence.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('gen',metavar='gen',help='Input the number to grow of sequence.',type=int)

    parser.add_argument('lit',metavar='lit',help='Input the last number of sequence.',type=int)

    args = parser.parse_args()

    if not 1 <= args.gen <= 40:

        parser.error(f'Generations {args.gen} must be between 1 and 40.')

    if not 1 <= args.lit <= 5:

        parser.error(f'Litter {args.lit} must be between 1 and 5.')

    return Args(generations=args.gen,litter=args.lit)

def fib(lit:int)->Generator[int,None,None]:
    """Generate the Fibonacci sequence indefinitely."""
    
    x,y=0,1
    
    yield x
    
    while True:
        yield y
        
        x,y = y*lit, y+x
        
def main()->None:
    """Show the value generate."""

    args = get_args()

    answer = None
    
    seq = fib(args.litter)

    for _ in  range(args.generations+1):
        answer = next(seq)

    print (answer)

if __name__=='__main__':
    main()