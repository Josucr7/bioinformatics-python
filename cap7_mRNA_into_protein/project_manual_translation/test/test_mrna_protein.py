""" Tests for mRNA_protein.py """

import os 
import re
import platform
from subprocess import getstatusoutput


PRG = "./mRNA_protein.py"
RUN = f"python {PRG}" if platform.system() == "Windows" else PRG


def test_exists() -> None:
    """ Verify if the file exists. """

    assert os.path.exists(PRG)

def test_usage() -> None:
    """ Verify the usage message. """

    for flag in ['-h','--help']:
        rv, out = getstatusoutput(f'{RUN} {flag}')
        assert rv == 0
        assert re.search("usage",out)

def test_not_argument() -> None:
    """ Verify the output without arguments. """
    
    rv, out = getstatusoutput(f"{RUN}")
    assert rv != 0
    assert re.search("usage",out)

def test_argument() -> None:
    """ Verify the output for an mRNA sequence. """

    rv, out = getstatusoutput(f"{RUN} CCCAUGGCUUUUUAA")
    assert rv == 0
    assert out == "MAF"

def test_bad_argument() -> None:
    """ Verify the output for an invalid mRNA sequence. """

    rv, out = getstatusoutput(f"{RUN} XYZ")
    assert rv == 0
    assert out == ""
    
