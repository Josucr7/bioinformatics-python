""" Test for mrna_proteins_bio.py"""

import platform
import os
from subprocess import getstatusoutput
import re


PRG = "./mrna_proteins_bio.py"
RUN = f"python3 {PRG}" if platform.system() == "Windows" else PRG
INPUT1 = ("./test/input/1.fa","[Seq('MAMAPRTEINSTRING')]")
INPUT2 = ("./test/input/2.fa","[Seq('MAF'), Seq('MKG')]")

def test_exists() -> None:
    """ Verify if the file exists. """

    assert os.path.exists(PRG)

def test_not_arguments() -> None:
    """ Verify the output without arguments. """

    rv, out = getstatusoutput(RUN)
    assert rv != 0
    assert re.search('ValueError',out)

def test_usage() -> None:
    """ Verify the usage message. """

    for flag in ['-h',"--help"]:
        rv, out = getstatusoutput(f"{RUN} {flag}")
        assert rv == 0
        assert re.search('usage',out)

def test_argument() -> None:
    """ Verify the output for an mRNA sequence. """
    
    rv, out = getstatusoutput(f"{RUN} -s CCCAUGGCUUUUUAA")
    assert rv == 0
    assert out == "[Seq('PMAF')]"


def test_input() -> None:
    """ Verify the output for a FASTA file. """

    for file,seq in [INPUT1,INPUT2]:
        rv,out = getstatusoutput(f"{RUN} -f {file}")
        assert rv == 0
        assert out == seq

def test_bad_argument() -> None:
    
    """ Verify the output for an invalid mRNA sequence. """

    rv, out = getstatusoutput(f"{RUN} -s XYZ")
    assert rv == 1
    assert re.search("Codon 'XYZ' is invalid",out)