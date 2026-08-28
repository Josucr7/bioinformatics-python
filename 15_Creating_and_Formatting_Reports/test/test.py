from platform import system
from subprocess import getstatusoutput
import os
import re
import random
import string

PRG = "./seq.py"
RUN = f"python3 {PRG}" if system() == "Windows" else PRG
EMPTY = './test/input/empty.fa'
INPUT1 = './test/input/1.fa'
INPUT2 = './test/input/2.fa'
ALL = ('./test/input/*.fa','./test/input/all.fa.out')

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
    """ Detect on bad file and generate a answer. """

    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} {bad}')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search(f"No such file or directory: '{bad}'", out)


def run(file:str) -> None:
    """ Template to eject test code. """
    expected_file = file + '.out'
    rv, out = getstatusoutput(f'{RUN} {file}')
    expected = open(expected_file).read().rstrip()

    assert rv == 0
    assert out == expected

def test_1() -> None:
    """ Verify that the program gives the correct values of file 1.fa """

    run(INPUT1)
    
def test_2() -> None:
    """ Verify that the program gives the correct values of file 2.fa """

    run(INPUT2)

def test_many_files() -> None:
     """ Verify that the program can execute some files. """
     expected_file = ALL[1] 
     rv, out = getstatusoutput(f'{RUN} {ALL[0]}')
     expected = open(expected_file).read().rstrip()

     assert rv == 0
     assert out == expected

def test_empty() -> None:
    """ Verify that the program identify a empty file empty.fa """

    run(EMPTY)

def test_styles() -> None:
    """ Test table styles """

    styles = [
        'plain', 'simple', 'grid', 'pipe', 'orgtbl', 'rst', 'mediawiki',
        'latex', 'latex_raw', 'latex_booktabs'
    ]

    for file in [INPUT1, INPUT2]:
        for style in styles:
            expected_file = file + '.' + style + '.out'
            assert os.path.isfile(expected_file)
            expected = open(expected_file).read().rstrip()
            flag = '--tablefmt' if random.choice([0, 1]) else '-t'
            rv, out = getstatusoutput(f'{RUN} {flag} {style} {file}')
            assert rv == 0
            assert out == expected



def random_string() -> str:
    """ Generate a random string """

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
