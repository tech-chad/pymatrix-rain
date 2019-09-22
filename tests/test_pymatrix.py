
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


def test_pymatrix_screen_resize_width_very_narrow():
    with Runner(*pymatrix_run(), width=50, height=50) as h:
        h.await_text("a")
        h.tmux.execute_command('split-window', '-ht0', '-l', 48)
        h.await_text("a")


def test_pymatrix_screen_resize_height_very_short():
    with Runner(*pymatrix_run(), width=50, height=50) as h:
        h.await_text("a")
        h.tmux.execute_command('split-window', '-vt0', '-l', 46)
        h.await_text("a")


def test_pymatrix_screen_resize_height_too_short():
    with Runner(*pymatrix_run(), width=50, height=50) as h:
        h.await_text("a")
        h.tmux.execute_command('split-window', '-vt0', '-l', 47)
        h.await_text("Error screen height is to short.")


def test_pymatrix_screen_test_mode():
    with Runner(*pymatrix_run("--test_mode")) as h:
        h.await_text("T")
