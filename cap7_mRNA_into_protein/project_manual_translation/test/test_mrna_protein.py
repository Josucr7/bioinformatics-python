#!/usr/bin/env python3
""" Test for mRNA_protein.py """

import os 
import re
import platform
from subprocess import getstatusoutput


PRG = "./mRNA_protein.py"
RUN = f"python {PRG}" if platform.system() == "Windows" else PRG
INPUT1 = ""
INPUT2 = ""

def test_exists() -> None:
    """ Program exists. """

    assert os.path.exists(PRG)

def test_usage() -> None:
    """ Set usage mesage. """

    for _ in ['-h','--help']:
        rv, out = getstatusoutput(f'{RUN} {_}')
        print(rv)
        assert re.search("usage",out)

def test_without_argument() -> None:
    """ Verify the output without argument. """
    
    rv, out = getstatusoutput(f"{RUN}")
    assert rv != 0
    assert re.search("usage",out)

def test_argument() -> None:
    """ Verify the ouput with mRNA sequence. """

    rv,out = getstatusoutput(f"{RUN} CCCAUGGCUUUUUAA")
    assert rv == 0
    assert out == "MAF"

def test_bad_argument() -> None:
    """ Verify the output withouth mRNA sequence. """

    rv, out = getstatusoutput(f"{RUN} XYZ")
    assert rv == 0
    assert out == ""
    
