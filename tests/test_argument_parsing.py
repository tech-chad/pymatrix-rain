
import pytest

from pymatrix import pymatrix


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 4), (["-d0"], 0), (["-d1"], 1), (["-d", "2"], 2), (["-d3"], 3),
    (["-d4"], 4), (["-d 5"], 5), (["-d6"], 6), (["-d7"], 7),
    (["-d8"], 8), (["-d9"], 9)
])
def test_argument_parsing_delay(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.delay == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["--test_mode"], True)
])
def test_argument_parsing_test_mode(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.test_mode == expected_results


# @pytest.mark.parametrize("test_values, expected_results", [
#     ([], False), (["--test_mode_ext"], True)
# ])
# def test_argument_parsing_test_mode_ext(test_values, expected_results):
#     result = pymatrix.argument_parsing(test_values)
#     assert result.test_mode_ext == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-b"], True)
])
def test_argument_parsing_bold_on(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.bold_on == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-B"], True)
])
def test_argument_parsing_bold_all(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.bold_all == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-s"], True)
])
def test_argument_parsing_screen_save_mode(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.screen_saver == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    (["-Cred"], "red"), (["-C", "Green"], "green"), (["-C", "BLUE"], "blue"),
    (["-CyeLLOW"], "yellow"), (["-C", "magenta"], "magenta"),
    (["-CCyan"], "cyan"), (["-Cwhite"], "white"), ([], "green")
])
def test_argument_parsing_color(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.color == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    (["-Lred"], "red"), (["-L", "Green"], "green"), (["-L", "BLUE"], "blue"),
    (["-LyeLLOW"], "yellow"), (["-L", "magenta"], "magenta"),
    (["-LCyan"], "cyan"), (["-Lwhite"], "white"), ([], "white")
])
def test_argument_parsing_lead_color(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.lead_color == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 0), (["-S1"], 1), (["-S5"], 5), (["-S", "20"], 20)
])
def test_argument_parsing_start_timer(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.start_timer == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 0), (["-R1"], 1), (["-R5"], 5), (["-R", "20"], 20)
])
def test_argument_parsing_run_timer(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.run_timer == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["--list_colors"], True)
])
def test_argument_parsing_list_colors(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.list_colors == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["--list_commands"], True)
])
def test_argument_parsing_list_commands(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.list_commands == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-a"], True)
])
def test_argument_parsing_async_scroll(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.async_scroll == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-m"], True)
])
def test_argument_parsing_multiple_color_mode(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.multiple_mode == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-M"], True)
])
def test_argument_parsing_multiple_random_color_mode(test_values,
                                                     expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.random_mode == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-c"], True)
])
def test_argument_parsing_cycle_through_colors(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.cycle == expected_results


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-e"], True)
])
def test_argument_parsing_extended_char(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.ext == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-E"], True)
])
def test_argument_parsing_extended_char(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.ext_only == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-l"], True),
])
def test_argument_parsing_double_space_lines(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.double_space == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["--wakeup"], True)
])
def test_argument_parsing_wakeup(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.wakeup == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-z"], True),
])
def test_argument_parsing_zero_one(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.zero_one == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["--disable_keys"], True)
])
def test_argument_parsing_disable_keys(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.disable_keys == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], "black",), (["--background", "blue"], "blue")
])
def test_argument_parsing_background_color(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.background == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-v"], True), (["--reverse"], True)
])
def test_argument_parsing_reverse(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.reverse == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-O"], True)
])
def test_argument_parsing_over_ride(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.over_ride == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-W"], True), (["--do_not_clear"], True)
])
def test_argument_parsing_do_not_clear(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.do_not_clear == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ("1", 1), ("40", 40), ("100", 100), ("156", 156), ("255", 255),
])
def test_argument_parsing_color_number(test_value, expected_result):
    result = pymatrix.argument_parsing(["--color_number", test_value])
    assert result.color_number == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-j"], True), (["--italic"], True)
])
def test_argument_parsing_italic(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.italic == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-K"], True), (["--Katakana_only"], True),
])
def test_argument_parsing_katakana_only(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.Katakana_only == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-k"], True), (["--katakana"], True),
])
def test_argument_parsing_katakana(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.katakana == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["--scroll_right"], True),
])
def test_argument_parsing_scroll_right(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.scroll_right == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["--scroll_left"], True),
])
def test_argument_parsing_scroll_right(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.scroll_left == expected_result


@pytest.mark.parametrize("test_value, expected_result", [
    ([], False), (["-o"], True), (["--old_school_scrolling"], True)
])
def test_argument_paring_old_school_scrolling(test_value, expected_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.old_school_scrolling == expected_result


@pytest.mark.parametrize("test_value, expect_result", [
    ([], " "), (["--bg_char", "-"], "-"), (["--bg_char", "+"], "+"),
    (["--bg_char", "*"], "*")
])
def test_argument_parsing_background_character(test_value, expect_result):
    result = pymatrix.argument_parsing(test_value)
    assert result.bg_char == expect_result


# testing helper functions
@pytest.mark.parametrize("test_values, expected_results", [
    ("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4),
    ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9)
])
def test_positive_int_zero_to_nine_normal(test_values, expected_results):
    """ Tests that the delay time conversion formula is working. """
    result = pymatrix.positive_int_zero_to_nine(test_values)
    assert result == expected_results


@pytest.mark.parametrize("test_values", [
    "-5", "10", "100", "2.5", " ", "Test", "test&*#", "",
])
def test_positive_int_zero_to_nine_error(test_values):
    """ Testing delay_positive_int will raise an error. """
    with pytest.raises(pymatrix.argparse.ArgumentTypeError):
        pymatrix.positive_int_zero_to_nine(test_values)


@pytest.mark.parametrize("test_values, expected_results", [
    ("red", "red"), ("Green", "green"), ("BLUE", "blue"),
    ("yeLLOW", "yellow"), ("magenta", "magenta"),
    ("Cyan", "cyan"), ("whiTe", "white")
])
def test_color_type_normal(test_values, expected_results):
    result = pymatrix.color_type(test_values)
    assert result


@pytest.mark.parametrize("test_values", [
    "orange", "12", "who", "<>", "", " ", "ter8934", "834DFD"
])
def test_color_type_error(test_values):
    with pytest.raises(pymatrix.argparse.ArgumentTypeError):
        pymatrix.color_type(test_values)


@pytest.mark.parametrize("test_values, expected_results", [
    ("1", 1), ("2", 2), ("6", 6), ("20", 20), ("500", 500)
])
def test_positive_int_normal(test_values, expected_results):
    result = pymatrix.positive_int(test_values)
    assert result == expected_results


@pytest.mark.parametrize("test_values", [
    "0", "-3", "1.3", "0.4", "10.4", "a", "b", "", " ", "$", "time32"
])
def test_positive_int_error(test_values):
    with pytest.raises(pymatrix.argparse.ArgumentTypeError):
        pymatrix.positive_int(test_values)


@pytest.mark.parametrize("test_value, expected_result", [
    ("1", 1), ("30", 30), ("100", 100), ("167", 167), ("200", 200),
    ("250", 250), ("255", 255)
])
def test_int_between_1_and_255(test_value, expected_result):
    result = pymatrix.int_between_1_and_255(test_value)
    assert result == expected_result


@pytest.mark.parametrize("test_values", [
    "0", "256", "34.4", "Blue", "test", "-4", "1001", "", " ", "c40", "30c",
    "*", "-C", "&",
])
def test_int_between_1_and_255_error(test_values):
    with pytest.raises(pymatrix.argparse.ArgumentTypeError):
        pymatrix.int_between_1_and_255(test_values)


@pytest.mark.parametrize("value", [
    " ", "-", "+", "_", "?", "=", "X", "6", "["
])
def test_background_character(value):
    result = pymatrix.background_character(value)
    assert result == value


@pytest.mark.parametrize("test_value", [
    "--", "__", "xy", "11", "x1", " 1", "=-", "[]"
])
def test_background_character_error(test_value):
    with pytest.raises(pymatrix.argparse.ArgumentTypeError):
        pymatrix.background_character(test_value)

