
import pytest
from hecate import Runner

import pymatrix


def pymatrix_run(*args):
    options = [a for a in args]
    return ["python3", "pymatrix.py"] + options


@pytest.mark.parametrize("test_key", ["Q", "q"])
def test_pymatrix_quit(test_key):
    with Runner(*pymatrix_run()) as h:
        h.await_text("a")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()
