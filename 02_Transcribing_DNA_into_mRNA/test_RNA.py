"""Test to RNA.py"""
import platform
from subprocess import getstatusoutput
import os
import re
import shutil
import random 
import string

PRG = './RNA.py'
RUN = f'python {PRG}' if platform.system()=='Windows' else PRG
TEST1 = './tests/input1.txt'
TEST2 = './tests/input2.txt'
TEST3 = './tests/input3.txt'

def test_exist()->None:
    """Verify if exists the script."""

    assert os.path.exists(PRG)

def test_usage()->None:
    """Analize if code run with help."""

    for arg in ['-h','--help']:
        rv,out = getstatusoutput(f'{RUN} {arg}')
        assert rv == 0
        assert out.lower().startswith('usage:')

def test_no_args()->None:
    """Verify if run without args."""

    rv,out = getstatusoutput(RUN)
    assert rv != 0
    assert out.lower().startswith('usage:')

def test_bad_file()->None:
    """Verify if put a directory that no exist."""

    bad=random_name()
    rv,out = getstatusoutput(f'{RUN} {bad}')
    assert rv != 0
    assert re.match('usage:',out,re.IGNORECASE)
    assert re.search(F"No such file or directory: '{bad}'",out)

def test_test1()->None:
    """Verify if run a file with one sequence."""
    
    out_dir = 'Out'
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
    
        retval,out = getstatusoutput(f'{RUN} {TEST1}')
        assert retval == 0
        assert out == 'Done, wrote 1 sequence in 1 file.'
        assert os.path.isdir(out_dir)
        out_file=os.path.join(out_dir,'input1.txt')
        assert os.path.isfile(out_file)
        with open(out_file) as fh:
            out_file = fh.read().rstrip()
        assert out_file == 'AACAAGGUUUCCGUAGGUGAACCUGCGGAA'

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
def test_test2()->None:
    """Verify if run a file with two sequences."""
    out_dir = random_name()
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
    
        retval,out = getstatusoutput(f'{RUN} {TEST2} -o{out_dir}')
        assert retval == 0
        assert out == 'Done, wrote 2 sequences in 1 file.'
        assert os.path.isdir(out_dir)
        out_file = os.path.join(out_dir,'input2.txt')
        assert os.path.isfile(out_file)
        with open(out_file) as fh:
            out_file = fh.read().rstrip()
        assert out_file == 'UGCAAAAGUAAGACUGACUGUUCGCCGUUAUACA''\n''GAGACACACCUAAUUUUUUUCUCACAGACUAUCGUCG'
    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
def test_multiple_inputs()->None:
    """Generate directory of DNA files."""
    
    out_dir = random_name()
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
            
        retval,out = getstatusoutput(f'{RUN} {TEST1} {TEST2} {TEST3} -o{out_dir}')
        assert retval == 0
        assert out == 'Done, wrote 5 sequences in 3 files.'
        assert os.path.isdir(out_dir)
        out_file1 = os.path.join(out_dir,'input1.txt')
        out_file2 = os.path.join(out_dir,'input2.txt')
        out_file3 = os.path.join(out_dir,'input3.txt')
        assert os.path.isfile(out_file1)
        assert os.path.isfile(out_file2)
        assert os.path.isfile(out_file3)
        with open(out_file3) as fh:
            out_file3 = fh.read().rstrip()
        assert out_file3 == out3()
    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
            
def out3()->str:
    """RNA sequences generate in the input3."""
    
    return ('AACAAGGUUUCCGUAGGUGAACCUGCGGAAGGAUCAUUAAUGAAUAACUAUGGUGUUGGUUGUUGCUGGCUCUAGGAGCAUGUGCACACCCACCAUUCUUAUCUGUCCACCUGUGAACACUAUGUAGGUCUGGAUAACUCUCGCUUUCGGGCGGAUACAGGGAUUGUCGCUUGCGGCUCUCCUUGAAUUUCCAGAUCUAUGUAUUUACAUACCCCAAUUGAAUGUUGAAGAAUGCAGUCAAUGGGCUUUAAGCCUAUAAAACAAUAUACAACUUUCAGCAACGGAUCUCUUGGCUCUCGCAUCGAUGAAGAACGCAGCGAAAUGCGAUAAGUAAUGUGAAUUGC''\n''AGAAUUCAGUGAAUCAUCGAAUCUUUGAACGCACCUUGCGCUCCUUGGUAUUCCGAGGAGCAUGCCUGUUUGAGUGUCAUUAAAUUCUCAACUUCAUCAUUUUUUGUUGAAGCUUGGAUGUGGGGGUUGUGCAGAACACUUUGGUGGUCUGCUCCCCUUAAAUGAAUUAGCGAGUUCAAACUGAGCUCCGUCUAUUGGUGUGAUAAUUAUCUACGCUGUGGAUGGGACUUAGACUUGCUUCUAAACUGUCCGCAAGGACAAUUCUUGACAAUUUGACCUCAAAUCAGGUAGGACUACCCGCUGAACUUAAGCAUAUCAA')

def random_name()->str:
    """Generate a random name to directory or files"""
    
    return ''.join(random.choices(string.ascii_uppercase+string.digits,k=6))