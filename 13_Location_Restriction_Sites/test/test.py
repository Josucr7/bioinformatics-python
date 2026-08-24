from platform import system
from subprocess import getstatusoutput
import os
import re


PRG = "./rev.py"
RUN = f"python3 {PRG}" if system() == "Windows" else PRG
INPUT1 = "./test/input/1.fa"
INPUT2 = "./test/input/2.fa"
EMPTY = "./test/input/empty.fa"

def test_file() -> None:
    """ Verify that the program file exists. """

    assert os.path.exists(PRG)

def test_usage() -> None:
    """ Verify the usage message. """

    for flag in ['-h','--help']:
        rv, out = getstatusoutput(f'{RUN} {flag}')
        assert rv == 0
        assert re.search('usage:',out)

def test_no_args() -> None:
    """ Verify the output without arguments. """

    rv, out = getstatusoutput(RUN)
    assert rv != 0
    assert re.search('usage',out)


def run(file:str) -> None:
    """ Template to eject test code. """
    expected_file = file + '.out'
    rv, out = getstatusoutput(f'{RUN} {file}')
    expected = set(open(expected_file).read().splitlines())

    assert rv == 0
    assert set(out.splitlines()) == expected

def test_1() -> None:
    """ Verify that the program locate the restriction sites of file 1.fa """

    run(INPUT1)
    
def test_2() -> None:
    """ Verify that the program locate the restriction sites of file 2.fa """

    run(INPUT2)

def test_3() -> None:
    """ Verify that the program identify a empty file empty.fa """

    run(EMPTY)
