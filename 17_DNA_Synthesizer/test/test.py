from platform import system
from subprocess import getstatusoutput
import os
import re
import random
import string
from typing import List, Optional

PRG = "./synt.py"
RUN = f"python3 {PRG}" if system() == "Windows" else PRG
TEST1 = './test/input/CAM_SMPL_GS108.fa'
TEST2 = './test/input/CAM_SMPL_GS112.fa'
TEST3 = './test/input/lsu.fq'

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
    rv, out = getstatusoutput(f'{RUN} {bad} ')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search(f"No such file or directory: '{bad}'", out)

def test_bad_seed():
    """ not int for seed """

    bad = random_string()
    opt = random.choice(['-s', '--seed'])
    rv, out = getstatusoutput(f'{RUN} {opt} {bad} ./tests/inputs*')
    assert rv != 0
    assert re.search(f"invalid int value: '{bad}'", out)

def test_bad_format():
    """ Dies on bad file format """

    bad = random_string()
    opt = random.choice(['-f', '--format'])
    rv, out = getstatusoutput(f'{RUN} {opt} {bad} ./tests/inputs/*')
    assert rv != 0
    assert re.search(f"argument -f/--format: invalid choice: '{bad}'", out)

def run(input_files: List[str], outfile: str, expected_file: str, opts: Optional[List[str]] = None) -> None:
    """ Runs on command-line input """

    assert all(map(os.path.isfile, input_files))
    assert os.path.isfile(expected_file)

    if os.path.isfile(outfile):
        os.remove(outfile)

    try:
        expected = open(expected_file).read().rstrip()
        options = ' '.join(opts) if opts else ''
        cmd = f"{RUN} {options} {' '.join(input_files)}"
        rv, _ = getstatusoutput(cmd)

        assert rv == 0
        assert os.path.isfile(outfile)
        assert open(outfile).read().strip() == expected

    finally:
        if os.path.isfile(outfile):
            os.remove(outfile)

def test_1_num1() -> None:
    """ test to file """

    run([TEST1], 'out.fa', TEST1 + '.n1.out', ['-s 1', '-n 1'])

def test_1_num1_outfile() -> None:
    """ test with other number of sequences. """

    filename = random_string()
    run([TEST1], filename, TEST1 + '.n1.out', ['-s 1', '-n 1', f'-o {filename}'])

def test_1_num1_min20_max40() -> None:
    """ test to specific max and min lenght. """

    run([TEST1], 'out.fa', TEST1 + '.n1.m20.x40.out', ['-s 1', '-n 1', '-m 20', '-x 40'])

def test_1_num1_kmer4() -> None:
    """ test to different k_mer. """

    run([TEST1], 'out.fa', TEST1 + '.n1.k4.out', ['-s 1', '-n 1', '-k 4'])

def test_1_num1_kmer5() -> None:
    """ test to specific k_mer and number of sequences. """

    run([TEST1], 'out.fa', TEST1 + '.n1.k5.out', ['-s 1', '-n 1', '-k 5'])

def test_3_num1_format() -> None:
    """ test the different format. """

    run([TEST3], 'out.fa', TEST3 + '.n1.out', ['-s 1', '-n 1', '-f fastq'])

def test_1_defaults() -> None:
    """ test the file. """

    run([TEST1], 'out.fa', TEST1 + '.default.out', ['-s 1'])

def test_multiple_inputs() -> None:
    """ test to multiple inputs"""

    run([TEST1, TEST2], 'out.fa', './test/input/mult.n10.out', ['-s 1', '-n 10'])


def random_string() -> str:
    """ Generate a random string """

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
