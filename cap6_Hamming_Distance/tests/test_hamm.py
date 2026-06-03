#!/usr/bin/env python3
"""Test for hamm.py"""

import os 
import platform 
import random
import re
import string
from subprocess import getstatusoutput

PRG = "./hamm.py"
RUN = f"python {PRG}" if platform.system() == "Windows" else PRG
INPUT1 = "./tests/inputs/1.fa"
INPUT2 = "./tests/inputs/2.fa"

def test_exist() -> None:
    """ Program exits """

    assert os.path.isfile(PRG)

def test_usage() -> None:
    """ Usage """

    for flag in ['-h','--help']:
        rv, out = getstatusoutput(f'{RUN} {flag}')
        assert rv == 0
        assert out.lower().startswith("usage")

def test_no_args() -> None:
    """Verify behavior with no arguments """
    rv, out = getstatusoutput(f"{RUN}")
    assert rv != 0
    assert re.search("Provide two sequences or a FASTA file",out) 


def test_bad_input() -> None:
    """ Fails on bad input """
    
    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} -f {bad}')
    assert rv != 0
    assert out.lower().startswith("usage:")
    assert re.search(f"No such file or directory: '{bad}'",out)


def test_string() -> None:
    """ Run with string input """
    rv,out = getstatusoutput(f'{RUN} -s1 GAGCCTACTAACGGGAT -s2 CATCGTAATGACGGCCT')
    assert rv == 0
    assert out == "7"

def test_good_input1() -> None:
    """ Run with FASTA file input """

    rv,out = getstatusoutput(f'{RUN} -f {INPUT1}')
    assert rv == 0
    assert out == "7"

def test_good_input2() -> None:
    """ Run with FASTA file input """

    rv,out = getstatusoutput(f'{RUN} -f {INPUT2}')
    assert rv == 0
    assert out == "503"


def random_string() -> str:
    """ Generate a random string """

    k =  random.randint(5,10)
    return "".join(random.choices(string.ascii_letters+string.digits,k=k))