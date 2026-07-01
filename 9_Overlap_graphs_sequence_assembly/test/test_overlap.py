""" Test for overlap.py """

import platform
from subprocess import getstatusoutput
import os
import string
import re
import random

PRG = "./overlap.py"
RUN = f'python3 {PRG}' if platform.system() == 'Windows' else PRG
TEST_1 = 'test/input/1.fa'
TEST_2 = 'test/input/2.fa'
TEST_3 = 'test/input/3.fa'

def test_exist() -> None:
    """" Verify if the file exists. """

    assert os.path.exists(PRG)

def test_usage() -> None:
    """ Verify the usage mesagge. """
    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{RUN} {flag}')
        assert rv == 0
        assert re.search('usage',out)

def test_not_args() -> None:
    """ Verify the output without arguments. """

    rv, out = getstatusoutput(RUN)
    assert rv != 0
    assert re.search('usage',out)

def test_bad_k() -> None:
    """ Die if the number the nucleotides to overlap is bad. """

    k = random.choice(range(-10,1))
    rv, out = getstatusoutput(f'{RUN} -k {k} {TEST_1}')
    assert rv != 0
    assert re.search(f'-k {k} must be > 0',out)

def test_bad_file() -> None:
    """ Detect only the files are exist. """

    bad_file = random_string()
    rv, out = getstatusoutput(f'{RUN} {bad_file}')
    assert rv != 0
    assert re.search(f"No such file or directory: '{bad_file}'",out)

def run(fasta_file: str, k: int) -> None:
    """ Run code with fasta files and compare the answer. """

    outfile = '.'.join([fasta_file, str(k), 'out'])
    assert os.path.isfile(outfile)

    expected = open(outfile).read().rstrip()
    cmd = f'{RUN} -k {k} {fasta_file} | sort'
    rv, out = getstatusoutput(cmd)
    assert rv == 0
    assert out.rstrip() == expected

def test_01():
    """ Runs FASTA file """

    run(TEST_1, 3)

def test_02() -> None:
    """ Runs FASTA file """

    run(TEST_1, 4)


def test_03() -> None:
    """ Runs FASTA file """

    run(TEST_1, 5)


def test_04() -> None:
    """ Runs FASTA file """

    run(TEST_2, 3)


def test_05() -> None:
    """ Runs FASTA file """

    run(TEST_2, 4)


def test_06() -> None:
    """ Runs FASTA file """

    run(TEST_2, 5)


def test_07() -> None:
    """ Runs FASTA file """

    run(TEST_3, 3)


def test_08() -> None:
    """ Runs FASTA file """

    run(TEST_3, 4)


def test_09() -> None:
    """ Runs FASTA file """

    run(TEST_3, 5)

def test_log()-> None:
    """ Verify the log file content."""

    cmd = f"{RUN} -k 3 -d {TEST_1}"
    rv, out = getstatusoutput(cmd)
    assert rv == 0
    assert os.path.exists(".log")
    with open('.log') as file:
        content=file.read().rstrip()

    assert 'DEBUG:root:input file = "test/input/1.fa"' in content

    assert "DEBUG:root:Starts" in content
    assert "'AAA': ['Rosalind_0498', 'Rosalind_2391', 'Rosalind_0442']" in content
    assert "'GGG': ['Rosalind_5013']" in content
    assert "'TTT': ['Rosalind_2323']" in content

    assert "DEBUG:root:Ends" in content
    assert "'AAA': ['Rosalind_0498']" in content
    assert "'CCC': ['Rosalind_2323', 'Rosalind_0442']" in content
    assert "'GGG': ['Rosalind_5013']" in content
    assert "'TTT': ['Rosalind_2391']" in content


def test_graph() -> None:
    """ Verify the graphic file created. """

    out_file = random_string()
    cmd = f"{RUN} -k 3 -o {out_file} {TEST_1}"
    rv, out = getstatusoutput(cmd)
    assert rv == 0
    assert os.path.exists(f"{out_file}.pdf")

    os.remove(f'{out_file}.pdf')
    os.remove('graph_out.pdf')
    os.remove(".log")


def random_string() -> None:
    """ Generate a random string. """

    return "".join(random.sample(string.ascii_letters+string.digits,k=random.randint(5,10)))