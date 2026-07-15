from platform import system
from subprocess import getstatusoutput
import random
import string
import os
import re


PRG = "./lcsm.py"
RUN = f"python3 {PRG}" if system() == "Windows" else PRG
FILE_EMPTY = "./test/input/empty.fa"
FILE_NONE = "./test/input/none.fa"
INPUT1 = "./test/input/1.fa"

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

def test_bad_file() -> None:
    """ Verify that the program rejects a nonexistent file. """

    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} {bad}')
    assert rv != 0
    assert re.search('usage',out)
    assert re.search(f"No such file or directory: '{bad}'", out)

def test_empty_file() -> None:
    """ Verify the output for an empty FASTA file. """

    rv, out = getstatusoutput(f'{RUN} {FILE_EMPTY}')
    assert rv == 0
    assert out == "Don't have sequences the FASTA file."

def test_no_common() -> None:
    """ Verify the output when no common subsequences are found. """

    rv, out = getstatusoutput(f'{RUN} {FILE_NONE}')
    assert rv == 0
    assert out == "No common subsequences."

def test_short() -> None:
    """ Verify that the program finds the correct common subsequences. """

    rv, out = getstatusoutput(f'{RUN} {INPUT1}')
    assert rv == 0
    assert "AC" in out
    assert "CA" in out
    assert "TA" in out

def random_string()->str:
    """Create a random string. """

    return "".join(random.sample(string.ascii_letters+string.digits,k=random.randint(5,10))) 
