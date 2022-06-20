from unittest import mock
import pytest
from hecate import Runner
from time import sleep

from pymatrix import pymatrix


def pymatrix_run(*args):
    options = [a for a in args]
    return ["python3", "pymatrix/pymatrix.py"] + options


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
    with Runner(*pymatrix_run("--list_commands"), width=80, height=80) as h:
        h.await_text("Commands available during run")


def test_pymatrix_version():
    with Runner(*pymatrix_run("--version")) as h:
        h.await_text(f"Version: {pymatrix.version}")


def test_pymatrix_help():
    with Runner(*pymatrix_run("--help"), width=80, height=80) as h:
        h.await_text("usage:")


def test_wakeup_help_suppressed():
    with Runner(*pymatrix_run("--help"), width=50, height=50) as h:
        h.await_text("--version")
        screen_shot = h.screenshot()
        assert "wakeup" not in screen_shot


def test_pymatrix_setup_curses_colors():
    with mock.patch.object(pymatrix.curses, "init_pair", return_value=None) as mock_pair:
        pymatrix.setup_curses_colors("random", "black", False)
        assert mock_pair.call_count == 9


def test_curses_lead_color():
    with mock.patch.object(pymatrix.curses, "init_pair", return_value=None) as mock_pair:
        pymatrix.curses_lead_color("blue", "black", False)
        assert mock_pair.call_count == 1


def test_pymatrix_setup_curses_colors_override():
    with mock.patch.object(pymatrix.curses, "init_pair", return_value=None) as mock_pair:
        pymatrix.setup_curses_colors("random", "black", True)
        assert mock_pair.call_count == 9


def test_curses_lead_color_override():
    with mock.patch.object(pymatrix.curses, "init_pair", return_value=None) as mock_pair:
        pymatrix.curses_lead_color("blue", "black", True)
        assert mock_pair.call_count == 1


def test_pymatrix_setup_color_number():
    with mock.patch.object(pymatrix.curses, "init_pair", return_value=None) as mock_pair:
        pymatrix.setup_curses_color_number(50, "black", False)
        assert mock_pair.call_count == 8


def test_pymatrix_setup_color_number_override():
    with mock.patch.object(pymatrix.curses, "init_pair", return_value=None) as mock_pair:
        pymatrix.setup_curses_color_number(50, "black", True)
        assert mock_pair.call_count == 8


def test_pymatrix_setup_color_number_color():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_color_number(60, "black", False)
    assert pymatrix.curses.pair_content(1) == (60, 0)
    assert pymatrix.curses.pair_content(7) == (60, 0)


def test_pymatrix_setup_color_number_color_override():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_color_number(60, "black", True)
    assert pymatrix.curses.pair_content(1) == (60, 16)
    assert pymatrix.curses.pair_content(7) == (60, 16)


def test_pymatrix_setup_curses_colors_call():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("green", "black", False)
    assert pymatrix.curses.pair_content(1) == (2, 0)
    assert pymatrix.curses.pair_content(7) == (2, 0)


def test_pymatrix_setup_curses_colors_call_background():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("green", "blue", False)
    assert pymatrix.curses.pair_content(1) == (2, 4)
    assert pymatrix.curses.pair_content(7) == (2, 4)


def test_pymatrix_setup_curses_colors_wake_up():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("green", "black", False)
    assert pymatrix.curses.pair_content(21) == (2, 0)


def test_pymatrix_setup_curses_colors_wake_up_other_colors():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("blue", "white", False)
    assert pymatrix.curses.pair_content(21) == (2, 0)


def test_pymatrix_setup_curses_colors_wake_up_override():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("green", "black", True)
    assert pymatrix.curses.pair_content(21) == (40, 16)


def test_pymatrix_setup_curses_colors_wake_up_other_colors_override():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("blue", "white", True)
    assert pymatrix.curses.pair_content(21) == (40, 16)


def test_pymatrix_setup_curses_color_number_wake_up():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_color_number(176, "black", False)
    assert pymatrix.curses.pair_content(21) == (2, 0)


def test_pymatrix_setup_curses_color_number_wake_up_background():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_color_number(188, "yellow", False)
    assert pymatrix.curses.pair_content(21) == (2, 0)


def test_pymatrix_setup_curses_colors_random():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("random", "black", False)
    assert pymatrix.curses.pair_content(1) == (1, 0)
    assert pymatrix.curses.pair_content(2) == (2, 0)
    assert pymatrix.curses.pair_content(7) == (7, 0)
    assert pymatrix.curses.pair_content(8) == (0, 0)


def test_pymatrix_setup_curses_colors_random_background():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("random", "cyan", False)
    assert pymatrix.curses.pair_content(1) == (1, 6)
    assert pymatrix.curses.pair_content(2) == (2, 6)
    assert pymatrix.curses.pair_content(7) == (7, 6)
    assert pymatrix.curses.pair_content(8) == (0, 6)


def test_pymatrix_setup_curses_colors_random_override():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("random", "black", True)
    assert pymatrix.curses.pair_content(1) == (160, 16)
    assert pymatrix.curses.pair_content(2) == (40, 16)
    assert pymatrix.curses.pair_content(7) == (255, 16)
    assert pymatrix.curses.pair_content(8) == (16, 16)


def test_pymatrix_setup_curses_colors_random_background_override():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.setup_curses_colors("random", "cyan", True)
    assert pymatrix.curses.pair_content(1) == (160, 44)
    assert pymatrix.curses.pair_content(2) == (40, 44)
    assert pymatrix.curses.pair_content(7) == (255, 44)
    assert pymatrix.curses.pair_content(8) == (16, 44)


def test_pymatrix_curses_lead_color():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.curses_lead_color("white", "black", False)
    assert pymatrix.curses.pair_content(10) == (7, 0)


def test_pymatrix_curses_lead_color_blue():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.curses_lead_color("blue", "black", False)
    assert pymatrix.curses.pair_content(10) == (4, 0)


def test_pymatrix_curses_lead_color_background():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.curses_lead_color("white", "cyan", False)
    assert pymatrix.curses.pair_content(10) == (7, 6)


def test_pymatrix_curses_lead_color_blue_background():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.curses_lead_color("blue", "white", False)
    assert pymatrix.curses.pair_content(10) == (4, 7)


def test_pymatrix_curses_lead_color_override():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.curses_lead_color("white", "black", True)
    assert pymatrix.curses.pair_content(10) == (255, 16)


def test_pymatrix_curses_lead_color_blue_override():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.curses_lead_color("blue", "black", True)
    assert pymatrix.curses.pair_content(10) == (21, 16)


def test_pymatrix_curses_lead_color_background_override():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.curses_lead_color("white", "cyan", True)
    assert pymatrix.curses.pair_content(10) == (255, 44)


def test_pymatrix_curses_lead_color_blue_background_override():
    pymatrix.curses.initscr()
    pymatrix.curses.start_color()
    pymatrix.curses_lead_color("blue", "white", True)
    assert pymatrix.curses.pair_content(10) == (21, 255)


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


def test_pymatrix_wakeup_key_command():
    # this is a long test
    with Runner(*pymatrix_run("--test_mode")) as h:
        h.await_text("T")
        h.press("C-w")
        h.default_timeout = 10
        h.await_text("Wake up, Neo...")
        h.await_text("The Matrix has you...")
        h.await_text("Follow the white rabbit.")
        h.await_text("Knock, knock, Neo.")
        h.await_text("T")


def test_pymatrix_wakeup_now_keys():
    # this is a long test
    with Runner(*pymatrix_run("--test_mode")) as h:
        h.await_text("T")
        h.default_timeout = 10
        h.write("w")
        h.write("A")
        h.write("k")
        h.write("e")
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


def test_pymatrix_wakeup_ignore_multiple_key_presses():
    # this is a long test
    with Runner(*pymatrix_run("--test_mode", "--wakeup")) as h:
        h.await_text("T")
        h.default_timeout = 10
        h.await_text("Wake up, Neo...")
        h.write("q")
        h.await_text("The Matrix has you...")
        h.write("q")
        h.await_text("Knock, knock, Neo.")
        h.await_text("T")


def test_pymatrix_wakeup_ignore_alot_of_key_presses():
    # this is a long test
    with Runner(*pymatrix_run("--test_mode", "--wakeup")) as h:
        h.await_text("T")
        h.default_timeout = 10
        h.await_text("Wake up, Neo...")
        h.write("q")
        h.await_text("The Matrix has you...")
        h.write("q")
        h.await_text("Follow the white rabbit.")
        h.write("q")
        h.write("q")
        h.write("q")
        h.write("q")
        h.write("q")
        h.await_text("Knock, knock, Neo.")
        h.await_text("T")


def test_pymatrix_wakeup_now_ignore_keys_multiple_key_presses():
    # this is a long test
    with Runner(*pymatrix_run("--test_mode")) as h:
        h.await_text("T")
        h.default_timeout = 10
        h.write("w")
        h.write("A")
        h.write("k")
        h.write("e")
        h.await_text("Wake up, Neo...")
        h.write("q")
        h.await_text("The Matrix has you...")
        h.write("q")
        h.await_text("Follow the white rabbit.")
        h.write("q")
        h.write("q")
        h.await_text("Knock, knock, Neo.")
        h.await_text("T")


@pytest.mark.parametrize("width", [80, 50, 40, 30, 20, 15, 10])
def test_pymatrix_double_space(width):
    with Runner(*pymatrix_run("--test_mode", "-l"), width=width, height=50) as h:
        h.await_text("T")
        sc = h.screenshot()
        assert "Traceback" not in sc


def test_pymatrix_zero_one_command_line_double_space():
    with Runner(*pymatrix_run("-z", "-l"), width=75, height=50) as h:
        h.await_text("0")
        h.await_text("1")
        sc = h.screenshot()
        assert "T" not in sc
        assert "5" not in sc


def test_pymatrix_zero_one_command_line():
    with Runner(*pymatrix_run("-z"), width=75, height=50) as h:
        h.await_text("0")
        h.await_text("1")
        sc = h.screenshot()
        assert "T" not in sc
        assert "5" not in sc


def test_pymatrix_zero_one_running_command():
    with Runner(*pymatrix_run("--test_mode", "-l"), width=100, height=50) as h:
        h.default_timeout = 4
        h.await_text("T")
        sleep(0.5)
        h.write("z")
        h.press("Enter")
        sleep(0.5)
        sc = h.screenshot()
        assert "T" in sc
        assert "0" in sc
        assert "1" in sc
        sleep(3)
        sc = h.screenshot()
        assert "T" not in sc
        sleep(0.5)
        h.write("Z")
        h.press("Enter")
        sleep(0.5)
        sc = h.screenshot()
        assert "T" in sc
        assert "0" in sc
        assert "1" in sc
        sleep(3)
        sc = h.screenshot()
        h.default_timeout = 6
        assert "T" in sc


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


def test_pymatrix_disable_keys():
    with Runner(*pymatrix_run("--test_mode", "--disable_keys")) as h:
        h.default_timeout = 2
        h.await_text("T")
        h.write("z")
        h.press("Enter")
        sleep(0.2)
        h.await_text("T")
        sc = h.screenshot()
        assert "1" not in sc


def test_pymatrix_disable_keys_quit():
    with Runner(*pymatrix_run("--test_mode", "--disable_keys")) as h:
        h.await_text("T")
        h.write("Q")
        h.await_exit()


def test_pymatrix_disable_keys_and_screen_saver():
    with Runner(*pymatrix_run("--test_mode", "-s", "--disable_keys")) as h:
        h.await_text("T")
        h.write("d")
        h.await_exit()


def test_pymatrix_disable_keys_check_running_keys():
    # not the best test
    with Runner(*pymatrix_run("--test_mode", "--disable_keys")) as h:
        h.default_timeout = 3
        h.await_text("T")
        h.await_text(chr(35))
        for k in "abcdefghijklmnoprstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ" \
                 "1234567890{[}]!@#$%^&*()_+=-~` ":
            h.write(k)
            h.press("Enter")
            sleep(0.05)
            h.await_text("T")
            h.await_text(chr(35))
        h.write("Q")
        h.press("Enter")
        h.await_exit()


def test_pymatrix_freeze():
    with Runner(*pymatrix_run("--test_mode"), width=100, height=10) as h:
        h.default_timeout = 2
        h.await_text("T")
        h.write("f")
        sleep(0.05)
        sc = h.screenshot()
        sleep(1)
        sc2 = h.screenshot()
        assert sc == sc2
        h.write("f")
        sleep(0.5)
        sc3 = h.screenshot()
        assert sc3 != sc2


def test_pymatrix_freeze_quit():
    with Runner(*pymatrix_run("--test_mode"), width=100, height=10) as h:
        h.default_timeout = 2
        h.await_text("T")
        h.write("f")
        sleep(0.05)
        h.write("q")
        h.await_exit()


def test_pymatrix_freeze_no_other_keys():
    with Runner(*pymatrix_run("--test_mode"), width=100, height=10) as h:
        h.default_timeout = 2
        h.await_text("T")
        h.write("f")
        sleep(0.05)
        sc = h.screenshot()
        h.write("z")
        sleep(0.5)
        assert h.screenshot() == sc


@pytest.mark.parametrize("test_value", ["-v", "--reverse"])
def test_pymatrix_reverse(test_value):
    with Runner(*pymatrix_run("--test_mode", test_value), width=100, height=10) as h:
        h.await_text("T")


def test_pymatrix_reverse_key():
    with Runner(*pymatrix_run("--test_mode"), width=100, height=10) as h:
        h.await_text("T")
        h.press("v")
        h.await_text("T")


def test_pymatrix_clear_screen():
    with Runner(*pymatrix_run("--test_mode"), width=80, height=20) as h:
        h.default_timeout = 3
        h.await_text("T")
        h.press("w")
        h.press("Enter")
        sleep(0.5)
        sc = h.screenshot()
        assert "T" not in sc
        h.await_text("T")


@pytest.mark.parametrize("test_value", ["1", "100", "40", "255", "128"])
def test_pymatrix_valid_color_number(test_value):
    cmd = f"TERM=xterm-256color python3 pymatrix/pymatrix.py --test_mode" \
          f" --color_number {test_value}"
    with Runner("bash") as h:
        h.await_text("$")
        h.write("clear")
        h.press("Enter")
        h.write(cmd)
        h.press("Enter")
        h.await_text("T")
        h.await_text(chr(35))


@pytest.mark.parametrize("test_value", ["0", "A", "blue", "256"])
def test_pymatrix_invalid_color_number(test_value):
    cmd = f"TERM=xterm-256color python3 pymatrix/pymatrix.py --test_mode" \
          f" --color_number {test_value}"
    with Runner("bash") as h:
        h.await_text("$")
        h.write("clear")
        h.press("Enter")
        h.write(cmd)
        h.press("Enter")
        h.await_text(f"{test_value} is an invalid positive int between 1 and 255")


def test_pymatrix_command_line_italic():
    cmd = f"TERM=xterm-256color python3 pymatrix/pymatrix.py --test_mode -j"
    with Runner("bash") as h:
        h.await_text("$")
        h.write("clear")
        h.press("Enter")
        h.write(cmd)
        h.press("Enter")
        h.await_text("T")
        h.await_text(chr(35))


def test_pymatrix_command_line_italic_reverse():
    cmd = f"TERM=xterm-256color python3 pymatrix/pymatrix.py --test_mode -j -v"
    with Runner("bash") as h:
        h.await_text("$")
        h.write("clear")
        h.press("Enter")
        h.write(cmd)
        h.press("Enter")
        h.await_text("T")
        h.await_text(chr(35))


def test_pymatrix_command_line_italic_zero_one():
    cmd = f"TERM=xterm-256color python3 pymatrix/pymatrix.py -z -j -v"
    with Runner("bash") as h:
        h.await_text("$")
        h.write("clear")
        h.press("Enter")
        h.write(cmd)
        h.press("Enter")
        h.await_text("0")
        h.await_text("1")


def test_pymatrix_default():
    with Runner(*pymatrix_run("--test_mode")) as h:
        h.await_text("T")
        h.await_text(chr(35))
        h.press("q")
        h.await_exit()


@pytest.mark.parametrize("args", [
    pytest.param(("-d", "9"), id="delay slow"),
    pytest.param(("-d", "1"), id="delay fast"),
    pytest.param(("-b", ), id="bold on"),
    pytest.param(("-B", ), id="bold all"),
    pytest.param(("-C", "blue"), id="color blue"),
    pytest.param(("-C", "yellow"), id="color yellow"),
    pytest.param(("-L", "red"), id="lead color red"),
    pytest.param(("-m", ), id="Multiple colors"),
    pytest.param(("-M", ), id="Multiple random colors"),
    pytest.param(("-c", ), id="cycle colors"),
    pytest.param(("--background", "white"), id="background color white"),
    pytest.param(("--reverse", ), id="reverse"),
    pytest.param(("-v", ), id="reverse -v"),
    pytest.param(("-W", ), id="do not clear -W"),
    pytest.param(("--do_not_clear", ), id="do not clear"),
    pytest.param(("--disable_keys", ), id="disable keys"),
    pytest.param(("-C", "black", "-L", "green", "--background", "white"),
                 id="color, lead and background"),
    pytest.param(("-C", "red", "-L", "yellow", "--background", "cyan", "-B"),
                 id="color, lead, background and bold all"),
    pytest.param(("--background", "white", "-M"),
                 id="background white and multiple random colors"),
])
def test_pymatrix_command_line_options(args):
    arguments = ("--test_mode", *args)
    with Runner(*pymatrix_run(*arguments)) as h:
        h.await_text("T")
        h.await_text(chr(35))
        h.press("q")
        h.await_exit()


def test_build_character_set_all():
    test_set = pymatrix.build_character_set(["all"])
    assert "A" in test_set
    assert "1" in test_set
    assert "*" in test_set
    assert "a" in test_set
    assert chr(199) in test_set


def test_build_character_set_zero():
    test_set = pymatrix.build_character_set(["zero"])
    assert "1" in test_set
    assert "0" in test_set
    assert "B" not in test_set
    assert "$" not in test_set
    assert chr(199) not in test_set


def test_build_character_set_test():
    test_set = pymatrix.build_character_set(["test"])
    assert "T" in test_set
    assert chr(35) in test_set
    assert "r" not in test_set
    assert "@" not in test_set
    assert "9" not in test_set
    assert chr(199) not in test_set


def test_build_character_set_char():
    test_set = pymatrix.build_character_set(["char"])
    assert "A" in test_set
    assert "1" in test_set
    assert "#" in test_set
    assert "a" in test_set
    assert chr(199) not in test_set


def test_build_character_set_ext():
    test_set = pymatrix.build_character_set(["ext"])
    assert "A" not in test_set
    assert "1" not in test_set
    assert ")" not in test_set
    assert "a" not in test_set
    assert chr(199) in test_set


def test_pymatrix_main_list_colors(capsys):
    pymatrix.main(["--list_colors"])
    captured_output = capsys.readouterr().out
    assert "red green blue yellow magenta cyan white black" in captured_output


def test_pymatrix_main_list_commands(capsys):
    pymatrix.main(["--list_commands"])
    captured_output = capsys.readouterr().out
    assert "Commands available during run" in captured_output
    assert "Delay" in captured_output
    assert "Cycle color delay" in captured_output
