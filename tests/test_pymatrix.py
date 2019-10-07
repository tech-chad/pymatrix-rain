
import pytest
from hecate import Runner

import pymatrix


def pymatrix_run(*args):
    options = [a for a in args]
    return ["python3", "pymatrix.py"] + options


def test_pymatrix_screen_test_mode():
    with Runner(*pymatrix_run("--test_mode")) as h:
        h.await_text("T")


@pytest.mark.parametrize("test_key", ["Q", "q"])
def test_pymatrix_quit(test_key):
    with Runner(*pymatrix_run("--test_mode")) as h:
        h.await_text("T")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("test_key", ["Q", "q", " ", "8", ":", "*", "M", "b", "I"])
def test_pymatrix_quit_screen_saver_mode(test_key):
    with Runner(*pymatrix_run("--test_mode", "-s")) as h:
        h.await_text("T")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


def test_pymatrix_screen_resize_width_very_narrow():
    with Runner(*pymatrix_run("--test_mode"), width=50, height=50) as h:
        h.await_text("T")
        h.tmux.execute_command('split-window', '-ht0', '-l', 47)
        h.await_text("T")


def test_pymatrix_screen_resize_height_very_short():
    with Runner(*pymatrix_run("--test_mode"), width=50, height=50) as h:
        h.await_text("T")
        h.tmux.execute_command('split-window', '-vt0', '-l', 46)
        h.await_text("T")


def test_pymatrix_screen_resize_height_too_short():
    with Runner(*pymatrix_run("--test_mode"), width=50, height=50) as h:
        h.await_text("T")
        h.tmux.execute_command('split-window', '-vt0', '-l', 47)
        h.await_text("Error screen height is to short.")


def test_pymatrix_start_timer():
    with Runner(*pymatrix_run("--test_mode", "-S2")) as h:
        h.default_timeout = 3
        h.await_text("T")


def test_pymatrix_run_timer():
    with Runner(*pymatrix_run("--test_mode", "-R2")) as h:
        h.default_timeout = 3
        h.await_text("T")
        h.await_exit()


@pytest.mark.parametrize("test_key", ["Q", "q"])
def test_pymatrix_quit_with_run_timer(test_key):
    with Runner(*pymatrix_run("--test_mode", "-R3")) as h:
        h.await_text("T")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


def test_pymatrix_list_colors():
    with Runner(*pymatrix_run("--list_colors")) as h:
        h.await_text("red green blue yellow magenta cyan white")


def test_pymatrix_list_commands():
    with Runner(*pymatrix_run("--list_commands")) as h:
        h.await_text("Commands available during run")


def test_pymatrix_version():
    with Runner(*pymatrix_run("--version")) as h:
        h.await_text(f"Version: {pymatrix.version}")
