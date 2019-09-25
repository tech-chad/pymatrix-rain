
import pytest

import pymatrix


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
def test_argument_parsing_list_commands(test_values, expected_results):
    result = pymatrix.argument_parsing(test_values)
    assert result.async_scroll == expected_results


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


