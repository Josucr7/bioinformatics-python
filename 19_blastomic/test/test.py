from platform import system
from subprocess import getstatusoutput
import os
import re
import random
import string
import csv


PRG = "./blastomatic.py"
RUN = f"python3 {PRG}" if system() == "Windows" else PRG
HITS1 = './test/input/hits1.csv'
HITS2 = './test/input/hits2.csv'
META = './test/input/meta.csv'

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

def test_bad_annotations() -> None:
    """ Detect on bad file and generate a answer. """

    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} --annotations {bad} --blasthits {HITS1}')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search(f"No such file or directory: '{bad}'", out)

def test_bad_input_file() -> None:
    """ Answer to bad input file. """

    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} --blasthits {bad} -a {META}')
    assert rv != 0
    assert re.search(f"No such file or directory: '{bad}'", out)


def test_input_file() -> None:
    """ Deetcts a good input. """

    outfile = 'out.csv'
    if os.path.isfile(outfile):
        os.remove(outfile)

    try:
        cmd = f'{RUN} -a {META} -b {HITS1}'
        print(cmd)
        rv, out = getstatusoutput(cmd)
        assert rv == 0
        assert out == 'Exported 500 to "out.csv".'
        assert os.path.isfile(outfile)

        reader = csv.DictReader(open(outfile), delimiter=',')
        assert set(reader.fieldnames
                   or '') == set(['qseqid', 'pident', 'depth', 'lat_lon'])
        records = sorted(list(reader), key=lambda d: d['qseqid'])
        assert len(records) == 500
        assert records[0]['qseqid'] == 'CAM_READ_0234442157'
        assert records[-1]['lat_lon'] == '42.503056,-67.24'
    finally:
        if os.path.isfile(outfile):
            os.remove(outfile)

def test_delimiter() -> None:
    """ Specify delimiter """

    outfile = 'out.xxx'
    if os.path.isfile(outfile):
        os.remove(outfile)

    try:
        delim = ',' if random.choice([0, 1]) else '\t'
        cmd = f'{RUN} -a {META} -b {HITS1} -d "{delim}" -o {outfile}'
        print(cmd)
        rv, out = getstatusoutput(cmd)
        assert rv == 0
        assert out == f'Exported 500 to "{outfile}".'
        assert os.path.isfile(outfile)

        reader = csv.DictReader(open(outfile), delimiter=delim)
        assert set(reader.fieldnames
                   or '') == set(['qseqid', 'pident', 'depth', 'lat_lon'])
        records = sorted(list(reader), key=lambda d: d['qseqid'])
        assert len(records) == 500
        assert records[0]['qseqid'] == 'CAM_READ_0234442157'
    finally:
        if os.path.isfile(outfile):
            os.remove(outfile)

def test_guess_delimiter() -> None:
    """ Guess delimiter """

    tsv_ext = random.choice(['.txt', '.tab', '.tsv'])
    outfile, delim = ('out.csv',
                      ',') if random.choice([0, 1]) else ('out' + tsv_ext,
                                                          '\t')

    if os.path.isfile(outfile):
        os.remove(outfile)

    try:
        cmd = f'{RUN} -a {META} -b {HITS2} -o {outfile}'
        rv, out = getstatusoutput(cmd)
        assert rv == 0
        assert out == f'Exported 252 to "{outfile}".'
        assert os.path.isfile(outfile)

        reader = csv.DictReader(open(outfile), delimiter=delim)
        assert set(reader.fieldnames
                   or '') == set(['qseqid', 'pident', 'depth', 'lat_lon'])
        records = list(reader)
        assert len(records) == 252
        assert records[-1]['qseqid'] == 'JCVI_READ_1100018174123'
    finally:
        if os.path.isfile(outfile):
            os.remove(outfile)

def test_pctid() -> None:
    """ Filter on percent ID """

    outfile = 'out.tsv'
    if os.path.isfile(outfile):
        os.remove(outfile)

    try:
        cmd = f'{RUN} -a {META} -b {HITS2} -p 90 -o {outfile}'
        rv, out = getstatusoutput(cmd)
        assert rv == 0
        assert out == f'Exported 101 to "{outfile}".'
        assert os.path.isfile(outfile)

        reader = csv.DictReader(open(outfile), delimiter='\t')
        assert set(reader.fieldnames
                   or '') == set(['qseqid', 'pident', 'depth', 'lat_lon'])
        records = list(reader)
        assert all(map(lambda r: float(r['pident']) >= 90, records))
    finally:
        if os.path.isfile(outfile):
            os.remove(outfile)



def random_string() -> str:
    """ Generate a random string """

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
