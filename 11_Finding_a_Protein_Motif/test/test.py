from platform import system
from subprocess import getstatusoutput
import random
import string
import os
import re
import shutil


PRG = "./protein_motif.py"
RUN = f"python3 {PRG}" if system() == "Windows" else PRG
INPUT1 = "./test/input/1.txt"
INPUT2 = "./test/input/2.txt"

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

def test_1() -> None:
    """ Verify that the program finds the correct proteins motif. """
    try:
        if os.path.isdir("test/fasta"):
            shutil.rmtree("test/fasta")
        expect_file = INPUT1+'.out'
        expect = open(expect_file).read().rstrip()
        rv, out = getstatusoutput(f'{RUN} {INPUT1}')
        assert rv == 0
        assert out.rstrip() == expect
    finally:
        if os.path.isdir("test/fasta"):
            shutil.rmtree("test/fasta")
    
def test_2() -> None:
    """ Verify that the program finds the correct proteins motif. """
    try:
        if os.path.isdir("test/fasta"):
            shutil.rmtree("test/fasta")
        expect_file = INPUT2+'.out'
        expect = open(expect_file).read().rstrip()
        rv, out = getstatusoutput(f'{RUN} {INPUT2}')
        assert rv == 0
        assert out.rstrip() == expect
    finally:
        if os.path.isdir("test/fasta"):
            shutil.rmtree("test/fasta")

def test_correct_dir() -> None:
    """ Verify that the program create a correct directory to save the sequences. """
    out_dir = random_string()
    try:
        if os.path.isdir(f"test/{out_dir}"):
            shutil.rmtree(f"test/{out_dir}")
        expect = f'Done, see output in "test/{out_dir}", there contains protein sequences.'
        rv, out = getstatusoutput(f'{RUN} {INPUT1} -d {out_dir}')
        assert os.path.isdir(f"test/{out_dir}")
        assert rv == 0
        assert expect in out.rstrip()
    finally:
            if os.path.isdir(f"test/{out_dir}"):
                shutil.rmtree(f"test/{out_dir}")
def random_string()->str:
    """Create a random string. """

    return "".join(random.sample(string.ascii_letters+string.digits,k=random.randint(5,10))) 
