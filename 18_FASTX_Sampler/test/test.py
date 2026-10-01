from platform import system
from subprocess import getstatusoutput
import os
import re
import random
import string
import os
from shutil import rmtree
from Bio import SeqIO

PRG = "./fastx.py"
RUN = f"python3 {PRG}" if system() == "Windows" else PRG
N1K = './test/input/n1k.fa'
N10K = './test/input/n10k.fa'
N100K = './test/input/n100k.fa'
FASTQ = '../16_Select_Sequences_FASTAX/test/input/lsu.fq'

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

    pattern = random_string()
    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} {bad} {pattern}')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search(f"No such file or directory: '{bad}'", out)

def test_bad_percent():
    """ Dies on bad percent """

    bad = random.randint(1, 10)
    rv, out = getstatusoutput(f'{RUN} -p {bad} {N1K}')
    assert rv != 0
    assert re.match('usage:', out, re.I)
    assert re.search(f'--percent "{float(bad)}" must be between 0 and 1', out)

def test_bad_seed():
    """ Dies on bad seed """

    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} -s {bad} {N1K}')
    assert rv != 0
    assert re.match('usage:', out, re.I)
    assert re.search(f"-s/--seed: invalid int value: '{bad}'", out)

def test_bad_format():
    """ Dies on bad file format """

    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} -f {bad} {N1K}')
    assert rv != 0
    assert re.match('usage:', out, re.I)
    err = (f"-f/--format: invalid choice: '{bad}' "
           r"\(choose from 'fasta', 'fastq'\)")
    assert re.search(err, out)

def test_defaults_one_file():
    """ Runs file """

    out_dir = 'out'
    try:
        if os.path.isdir(out_dir):
            rmtree(out_dir)

        rv, out = getstatusoutput(f'{RUN} -s 10 {N1K}')
        assert rv == 0
        expected = ('Wrote 108 sequences from 1 file to directory "out".')
        assert out == expected
        assert os.path.isdir(out_dir)

        files = os.listdir(out_dir)
        assert len(files) == 1

        out_file = os.path.join(out_dir, os.path.basename(N1K))
        assert os.path.isfile(out_file)

        seqs = list(SeqIO.parse(out_file, 'fasta'))
        assert len(seqs) == 108

    finally:
        if os.path.isdir(out_dir):
            rmtree(out_dir)

def test_fastq_input():
    """ FASTQ file """

    out_dir = 'out'
    try:
        if os.path.isdir(out_dir):
            rmtree(out_dir)

        rv, out = getstatusoutput(f'{RUN} -s 1 -p .8 -f fastq {FASTQ}')
        assert rv == 0
        expected = ('Wrote 3 sequences from 1 file to directory "out".')
        assert out == expected
        assert os.path.isdir(out_dir)

        files = os.listdir(out_dir)
        assert len(files) == 1

        out_file = os.path.join(out_dir, os.path.basename(FASTQ))
        assert os.path.isfile(out_file)

        seqs = list(SeqIO.parse(out_file, 'fasta'))
        assert len(seqs) == 3

    finally:
        if os.path.isdir(out_dir):
            rmtree(out_dir)


def test_defaults_multiple_file():
    """ Runs on input with many files """

    out_dir = random_string()
    try:
        if os.path.isdir(out_dir):
            rmtree(out_dir)

        cmd = f'{RUN} -o {out_dir} -s 1 {N100K} {N10K} {N1K}'
        rv, out = getstatusoutput(cmd)
        assert rv == 0
        status = (f'Wrote 11,075 sequences from 3 files to directory "{out_dir}".')

        assert out == status
        assert os.path.isdir(out_dir)

        files = os.listdir(out_dir)
        assert len(files) == 3

        expected = [('n1k.fa', 106), ('n10k.fa', 995), ('n100k.fa', 9974)]
        for file, num in expected:
            path = os.path.join(out_dir, file)
            assert os.path.isfile(path)
            seqs = list(SeqIO.parse(path, 'fasta'))
            assert len(seqs) == num

    finally:
        if os.path.isdir(out_dir):
            rmtree(out_dir)

def test_max_reads():
    """ Verify max reads """

    out_dir = 'out'
    try:
        if os.path.isdir(out_dir):
            rmtree(out_dir)

        max_reads = random.randint(10, 20)
        rv, out = getstatusoutput(f'{RUN} -s 10 -m {max_reads} {N1K}')
        assert rv == 0
        expected = (f'Wrote {max_reads} sequences from 1 file to directory "out".')
        assert out == expected
        assert os.path.isdir(out_dir)

        files = os.listdir(out_dir)
        assert len(files) == 1

        out_file = os.path.join(out_dir, os.path.basename(N1K))
        assert os.path.isfile(out_file)

        # correct number of seqs
        seqs = list(SeqIO.parse(out_file, 'fasta'))
        assert len(seqs) == max_reads

    finally:
        if os.path.isdir(out_dir):
            rmtree(out_dir)

def test_options():
    """ Runs on input """

    out_dir = random_string()
    try:
        if os.path.isdir(out_dir):
            rmtree(out_dir)

        cmd = f'{RUN} -s 4 -o {out_dir} -p .25 {N1K} {N10K} {N100K}'
        rv, out = getstatusoutput(cmd)
        assert rv == 0
        assert re.search(f'Wrote 27,688 sequences from 3 files to directory "{out_dir}".',out)

        assert os.path.isdir(out_dir)

        files = os.listdir(out_dir)
        assert len(files) == 3

        seqs_written = 0
        for file in files:
            seqs_written += len(
                list(SeqIO.parse(os.path.join(out_dir, file), 'fasta')))

        assert seqs_written == 27688
    finally:
        if os.path.isdir(out_dir):
            rmtree(out_dir)



def random_string() -> str:
    """ Generate a random string """

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
