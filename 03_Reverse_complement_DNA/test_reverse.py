"""Test to reverse.py"""

import platform
from subprocess import getstatusoutput
import re
import os

PRG = './reverse.py'
RUN = f'python {PRG}' if platform.system()=='Windows' else PRG
TEST1 = ('./Tests/input1.txt','ACCGGGTTTT')
TEST2 = ('./Tests/input2.txt','GTTGTAGCTCTCTCGTACTCTGTTAGGATCGTGTTAAGCAGCCTAAAAACAGCGAGCATAGGGGAGTTCGCCAGACCTCCCCATGCTCCAACACGTGCTGTGTGTAAAGACCGTGTTCGTAGCCACTGCGGCTTAATTTCTGGCTGGCTCAGCTTGTCCCCGAAGGGGTCCATTCTCGACACATCGAATCTGTGGATATCTTCCGCGTGCTGGTATCATTATTATCGGAAGGGCGTCGGCAATTGGATATTTGATGCTTGACAGTCCAACTACCCTAGCAAGATTATGCTTGGAGTATAAGTAACCTCTATTTTTACTGTCTGTCGGTAACAGGTTTAGCTCAGATGGTGAATCACAGCAGAATAAGTCTGGTACAGCTTGTCCAATTTGAGATGATGAAAGCTCCATGCTCTTGAGGAGACTGTTAGAATTTCTAAGCTTCGGGCCACTGACGTCTCAAATGCCCAGCATGCTGTTGGCCCTTTGTACACGGGGAACAGCTGTATACACACCGTGTATGGAAAGACCTTTATCTCCTATCCGTAGCTAGCAAAGCCCTCTACTGACTGGTTGCACCGTGATTTCCTCTTACAGAGCAGCCCGGCCGTGCCTAAAAAAGCAGTACACACGCCGTGAACATCATAGTCTATGCCCCAGAGTCAGAGCGGAGCAGTGGACCAATGGTCGGTCGATAATTAGCGGTTCGGATGTCATGGCCTCACATAGGGCAAGTGCATAGATTACGGGGTCGAACCAGTAGTGTTCTCCACATCCTCCGTACTCTCCGGGCCTGAACGCTCTACACGGGCGGTGTCAAGGGTGCCGCTGTATAATAAGAGTCCACTGCAACATTCGTCAACTTTTATAGAACGGAAGGGCTACAGACACCTACCGTAGAGCAGCTGATTCCCTCAAATACGGCTAAGTTCTAGGGGATTGACCCCCGTCCGCCGCATTGAGGGACCTATCGAAGGCGTCTTACCCAGCGACTGTAATGTA')


def test_exists()->None:
    """Verify if the script exist."""
    
    assert os.path.exists(PRG)

def test_usage()->None:
    """Analize if the code run with help."""

    for arg in ['-h','--help']:
        rv,out = getstatusoutput(f'{RUN} {arg}')
        assert rv == 0
        assert out.lower().startswith('usage:')

def test_no_args()->None:
    """Verify that not args."""

    rv,out = getstatusoutput(f"{RUN}")
    assert rv != 0
    assert re.match('usage',out,re.IGNORECASE)

def test_lower()->None:
    """Verify if run lowercase inputs."""

    retval,out = getstatusoutput(f"{RUN} AAAcccct")
    assert retval == 0
    assert out == 'aggggTTT'

def test_args()->None:
    """Verify the output."""

    for infile,expected in [TEST1,TEST2]:
        if os.path.isfile(infile):
            with open(infile) as fh:
                infile= fh.read().rstrip()
        retval,out = getstatusoutput(f'{RUN} {infile}')
        assert retval == 0
        assert out == expected

def test_files()->None:
    """Verify the run files."""

    for infile,expected in [TEST1,TEST2]:
        retval,out = getstatusoutput(f'{RUN} {infile}')
        assert retval == 0
        assert out == expected
