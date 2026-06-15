"""Test by DNA.py"""

import os
import platform
from subprocess import getstatusoutput

PRG='./DNA.py'
RUN=f'python {PRG}' if platform.system() =='Windows' else PRG
Test1=('./tests/input1.txt','3 3 2 2')
Test2=('./tests/input2.txt','21 17 12 21')
Test3=('./tests/input3.txt','238 223 225 224')


def test_exist()->None:
    """Verify if the script exists."""

    assert os.path.exists(PRG)

def test_usage()->None:
    """Print ussage."""

    for arg in ['-h','--help']:
        rv,out=getstatusoutput(f'{RUN} {arg}')
        assert rv == 0
        assert out.lower().startswith('usage:')

def test_no_args()->None:
    """Dies with no arguments."""

    rv,out=getstatusoutput(RUN)
    assert rv != 0
    assert out.lower().startswith('usage:')

def test_args()->None:
    """Execute the code with args."""

    for infile,expected in [Test1,Test2,Test3]:
        if os.path.isfile(infile):
            with open(infile) as doc:
                dir=doc.read().rstrip()
        retval,out=getstatusoutput(f'{RUN} {dir}')
        assert retval == 0
        assert out == expected

def test_files()->None:
    """Execute the code with files."""
    
    for infile,expected in [Test1,Test2,Test3]:
        retval,out=getstatusoutput(f'{RUN} {infile}')
        assert retval == 0
        assert out == expected