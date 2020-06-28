from unittest import mock
import pytest
from hecate import Runner

from pymatrix import pymatrix


def pymatrix_run(*args):
    options = [a for a in args]
    return ["python3", "pymatrix/pymatrix.py"] + options


# def pymatrix_run_inside(*args):
#     options = [a for a in args]
#     return "python3", "pymatrix/pymatrix.py"] + options


def test_pymatrix_screen_test_mode():
    with Runner(*pymatrix_run("--test_mode", "-d1")) as h:
        h.await_text("T")


def test_pymatrix_screen_test_mode_ext():
    with Runner(*pymatrix_run("--test_mode_ext"), "-d1") as h:
        h.await_text(chr(35))


@pytest.mark.parametrize("test_key", ["Q", "q"])
def test_pymatrix_quit(test_key):
    with Runner(*pymatrix_run("--test_mode", "-d1")) as h:
        h.await_text("T")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("test_key", ["Q", "q", " ", "8", ":", "*", "M", "b", "I"])
def test_pymatrix_quit_screen_saver_mode(test_key):
    with Runner(*pymatrix_run("--test_mode", "-s", "-d1")) as h:
        h.default_timeout = 2
        h.await_text("T")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


def test_pymatrix_screen_resize_width_very_narrow():
    # note test can be flaky
    with Runner(*pymatrix_run("--test_mode", "-d1"), width=50, height=50) as h:
        h.default_timeout = 3
        h.await_text("T")
        h.tmux.execute_command('split-window', '-ht0', '-l', 45)
        h.await_text("T")


def test_pymatrix_screen_resize_height_very_short():
    with Runner(*pymatrix_run("--test_mode", "-d1"), width=50, height=50) as h:
        h.default_timeout = 3
        h.await_text("T")
        h.tmux.execute_command('split-window', '-vt0', '-l', 43)
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
    with Runner(*pymatrix_run("--test_mode", "-R3", "-d1")) as h:
        h.await_text("T")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


def test_pymatrix_list_colors():
    with Runner(*pymatrix_run("--list_colors")) as h:
        h.default_timeout = 2
        h.await_text("red green blue yellow magenta cyan white")


def test_pymatrix_list_commands():
    with Runner(*pymatrix_run("--list_commands")) as h:
        h.await_text("Commands available during run")


def test_pymatrix_version():
    with Runner(*pymatrix_run("--version")) as h:
        h.await_text(f"Version: {pymatrix.version}")


def test_pymatrix_help():
    with Runner(*pymatrix_run("--help"), width=50, height=38) as h:
        h.await_text("usage: pymatrix.py")


def test_pymatrix_setup_curses_colors():
    with mock.patch.object(pymatrix.curses, "init_pair", return_value=None) as mock_pair:
        pymatrix.setup_curses_colors("random")
        assert mock_pair.call_count == 7


def test_curses_lead_color():
    with mock.patch.object(pymatrix.curses, "init_pair", return_value=None) as mock_pair:
        pymatrix.curses_lead_color("blue")
        assert mock_pair.call_count == 1


def test_pymatrix_display_commands(capsys):
    pymatrix.display_commands()
    captured_output = capsys.readouterr().out
    expected_text = "Commands available during run"
    assert expected_text in captured_output


@pytest.mark.parametrize("password",
                         ["test", "499823", "asdfwwef", " ", "", "  3432sdfe   "])
def test_pymatrix_password(password):
    with Runner(*pymatrix_run("--test_mode", "-p", "-d1")) as h:
        h.await_text("Enter password:")
        h.write(password)
        h.press("Enter")
        h.await_text("T")
        h.write("Q")
        h.await_text("Enter password:")
        h.write(password)
        h.press("Enter")
        h.press("Enter")
        h.await_exit()


def test_pymatrix_control_c_running():
    with Runner("bash") as h:
        h.await_text("$")
        h.write("clear")
        h.press("Enter")
        h.write("python3 pymatrix/pymatrix.py --test_mode -d1")
        h.press("Enter")
        h.default_timeout = 2
        h.await_text("T")
        h.press("C-c")
        captured = h.screenshot()
        assert "Traceback" not in captured


def test_pymatrix_control_c_with_password():
    with Runner("bash") as h:
        h.await_text("$")
        h.write("clear")
        h.press("Enter")
        h.write("python3 pymatrix/pymatrix.py --test_mode -p")
        h.press("Enter")
        h.await_text("Enter password:")
        h.write("blueTOWN")
        h.press("Enter")
        h.await_text("T")
        h.press("C-c")
        h.await_text("Enter password:")
        h.write("blueTOWN")
        h.press("Enter")
        h.press("Enter")
        captured = h.screenshot()
        assert "Traceback" not in captured
        assert "$" in captured
