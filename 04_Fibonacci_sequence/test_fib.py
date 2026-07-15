"""Test to fibonacci.py"""

import platform
from subprocess import getstatusoutput
import random
import os
import re

PRG = "./fibonacci.py"
RUN = f'python {PRG}' if platform.system() == 'Windows' else PRG

def test_exist()->None:
    """Identify if the program exists."""

    assert os.path.exists(PRG)

def test_usage()->None:
    """Verify the variable help."""

    for arg in ['-h','--help']:
        rv,out = getstatusoutput(f'{RUN} {arg}')
        assert rv == 0
        assert out.lower().startswith('usage')

def test_no_args()-> None:
    """Verify the answer if not put args."""

    rv,out = getstatusoutput(RUN)
    assert rv!=0
    assert out.lower().startswith('usage:')

def test_bad_generations()->None:
    """Verify if number of generation is out between 1 and 40."""

    n = random.choice(list(range(-10,0))+list(range(41,80)))
    k = random.randint(1,5)
    rv,out = getstatusoutput(f'{RUN} {n} {k}')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search(f'Generations {n} must be between 1 and 40.',out)

def test_bad_litter()->None:
    """Verify if number of litter  is out between 1 and 5."""

    n = random.randint(1,40)
    k = random.choice(list(range(-10,0))+list(range(6,10)))
    rv,out = getstatusoutput(f'{RUN} {n} {k}')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search(f'Litter {k} must be between 1 and 5.',out)

def test_1()->None:
    """Runs on good input."""

    retval,out = getstatusoutput(f'{RUN} 5 3')
    assert retval == 0
    assert out == '19'

def test_2()->None:
    """Runs on good input."""

    retval,out = getstatusoutput(f'{RUN} 30 4')
    assert retval == 0
    assert out == '436390025825'
