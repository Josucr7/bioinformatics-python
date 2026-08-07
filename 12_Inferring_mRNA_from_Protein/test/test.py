from platform import system
from subprocess import getstatusoutput
import random
import string
import os
import re


PRG = "./mrna_protein.py"
RUN = f"python3 {PRG}" if system() == "Windows" else PRG
INPUT = ("MA","12")
INPUT1 = ("./test/input/1.txt",'448832')
INPUT2 = ("./test/input/2.txt",'415872')
INPUT3 = ("./test/input/3.txt","283264")

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


def run(protein:str,result:str) -> None:
    """ Template to eject test code. """

    rv, out = getstatusoutput(f'{RUN} {protein}')
    assert rv == 0
    assert out.rstrip() == result

def test_1() -> None:
    """ Verify that the program calculate and reducte the list of file 1.txt """

    run(*INPUT1)
    
def test_2() -> None:
    """ Verify that the program calculate and reducte the list of file 2.txt """

    run(*INPUT2)

def test_3() -> None:
    """ Verify that the program calculate and reducte the list of file 3.txt """

    run(*INPUT3)
