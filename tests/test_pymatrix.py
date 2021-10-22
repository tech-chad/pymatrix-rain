from unittest import mock
import pytest
from hecate import Runner
from time import sleep

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
        sc = h.screenshot()
        assert "x" not in sc


def test_pymatrix_screen_test_mode_ext():
    with Runner(*pymatrix_run("--test_mode_ext", "-d1")) as h:
        h.await_text(chr(35))
        sc = h.screenshot()
        assert "x" not in sc


def test_pymatrix_screen_test_mode_both():
    with Runner(*pymatrix_run("--test_mode_ext", "--test_mode", "-d1")) as h:
        h.await_text(chr(35))
        h.await_text("T")
        sc = h.screenshot()
        assert "x" not in sc


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


@pytest.mark.parametrize("size", [50, 20, 13, 11, 10])
def test_pymatrix_screen_width_start(size):
    with Runner(*pymatrix_run("--test_mode"), width=size, height=50) as h:
        h.await_text("T")


@pytest.mark.parametrize("size", [9, 8, 7])
def test_pymatrix_screen_width_start_fail(size):
    with Runner(*pymatrix_run("--test_mode"), width=size, height=50) as h:
        h.await_text("Error screen width is to narrow.")


def test_pymatrix_screen_resize_adjust_width():
    with Runner(*pymatrix_run("--test_mode"), width=50, height=50) as h:
        h.await_text("T")
        h.tmux.execute_command('split-window', '-ht0', '-l', 25)
        h.await_text("T")
        h.tmux.execute_command('resize-pane', '-L', 10)
        h.await_text("T")
        h.tmux.execute_command('resize-pane', '-L', 5)
        h.await_text("Error screen width is to narrow.")
        sc = h.screenshot()
        assert "T" not in sc
        assert "Error" in sc


@pytest.mark.parametrize("size", [20, 12, 11, 10])
def test_pymatrix_screen_height_start(size):
    with Runner(*pymatrix_run("--test_mode"), width=50, height=size) as h:
        h.await_text("T")


@pytest.mark.parametrize("size", [9, 8, 5])
def test_pymatrix_screen_height_start_fail(size):
    with Runner(*pymatrix_run("--test_mode"), width=50, height=size) as h:
        h.await_text("Error screen height is to short.")


def test_pymatrix_screen_resize_adjust_height():
    with Runner(*pymatrix_run("--test_mode"), width=50, height=50) as h:
        h.await_text("T")
        h.tmux.execute_command('split-window', '-vt0', '-l', 25)
        h.await_text("T")
        h.tmux.execute_command('resize-pane', '-U', 10)
        h.await_text("T")
        h.tmux.execute_command('resize-pane', '-U', 8)
        h.await_text("Error screen height is to short.")
        sc = h.screenshot()
        assert "T" not in sc
        assert "Error screen height is to short." in sc


def test_pymatrix_screen_resize_height_too_short():
    with Runner(*pymatrix_run("--test_mode"), width=50, height=50) as h:
        h.await_text("T")
        h.tmux.execute_command('split-window', '-vt0', '-l', 40)
        h.await_text("Error screen height is to short.")
        sc = h.screenshot()
        assert "T" not in sc


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
    with Runner(*pymatrix_run("--help"), width=50, height=50) as h:
        h.await_text("usage:")


def test_wakeup_help_suppressed():
    with Runner(*pymatrix_run("--help"), width=50, height=50) as h:
        h.await_text("--version")
        screen_shot = h.screenshot()
        assert "wakeup" not in screen_shot


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


def test_pymatrix_wakeup():
    # this is a long test
    with Runner(*pymatrix_run("--test_mode", "--wakeup")) as h:
        h.await_text("T")
        h.default_timeout = 10
        h.await_text("Wake up, Neo...")
        h.await_text("The Matrix has you...")
        h.await_text("Follow the white rabbit.")
        h.await_text("Knock, knock, Neo.")
        h.await_text("T")


def test_pymatrix_wakeup_do_not_quit_on_q():
    # this is a long test
    with Runner(*pymatrix_run("--test_mode", "--wakeup")) as h:
        h.await_text("T")
        h.default_timeout = 10
        h.await_text("Wake up, Neo...")
        h.write("q")
        h.press("Enter")
        h.await_text("Knock, knock, Neo.")
        h.await_text("T")


@pytest.mark.parametrize("width", [80, 50, 40, 30, 20, 15, 10])
def test_pymatrix_double_space(width):
    with Runner(*pymatrix_run("--test_mode", "-l"), width=width, height=50) as h:
        h.await_text("T")
        sc = h.screenshot()
        assert "Traceback" not in sc


def test_pymatrix_zero_one_command_line():
    with Runner(*pymatrix_run("-z", "-l"), width=75, height=50) as h:
        h.await_text("0")
        h.await_text("1")
        sc = h.screenshot()
        assert "T" not in sc
        assert "5" not in sc


def test_pymatrix_zero_one_running_command():
    with Runner(*pymatrix_run("--test_mode", "-l"), width=100, height=50) as h:
        h.await_text("T")
        h.write("z")
        h.press("Enter")
        h.await_text("0")
        h.await_text("1")
        sc = h.screenshot()
        assert "T" not in sc
        assert "5" not in sc
        h.default_timeout = 4
        h.write("Z")
        h.press("Enter")
        sleep(3)
        h.await_text("T")
        sc = h.screenshot()
        assert "T" in sc
        assert "5" in sc


def test_pymatrix_no_zero_one_running():
    with Runner(*pymatrix_run("--test_mode"), width=100, height=50) as h:
        h.await_text("T")
        h.write("Z")
        h.press("Enter")
        sleep(2)
        h.default_timeout = 3
        h.await_text("T")
        sc = h.screenshot()
        for letter in "AaBbCcDe0987654321ZzRrOoPpQqWweEYyUuIiOoPpKkLlJjmMnNXxSsgGhH":
            assert letter not in sc
