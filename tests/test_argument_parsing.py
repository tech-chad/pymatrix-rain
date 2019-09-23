
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
