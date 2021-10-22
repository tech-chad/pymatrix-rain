from unittest import mock

import pytest

from pymatrix import pymatrix


# @pytest.fixture
# def set_screen_size():
#     yield pymatrix.MatrixLine.set_screen_size(50, 50)
#
#     pymatrix.MatrixLine.set_screen_size(0, 0)


# @pytest.fixture
# def setup_matrix_line():
#     matrix_line = pymatrix.MatrixLine
#     matrix_line.set_screen_size(50, 50)
#     with mock.patch.object(matrix_line, "char_list", ["T"]):
#         yield matrix_line
#
#     matrix_line.set_screen_size(0, 0)


def test_increment():
    line = pymatrix.SingleLine(5, 20, 20)
    line.increment()
    assert line.lead_y == 1
    assert line.y == 0
    line.increment()
    assert line.lead_y == 2
    assert line.y == 1


def test_increment_past_height():
    line = pymatrix.SingleLine(5, 20, 6)
    for _ in range(5):
        line.increment()
    assert line.lead_y == 5
    assert line.y == 4
    line.increment()
    assert line.lead_y == 5
    assert line.y == 5
    line.increment()
    assert line.lead_y == 5
    assert line.y == 5


def test_async_scroll_turn():
    line = pymatrix.SingleLine(5, 20, 20)
    line.async_scroll_rate = 1
    result = line.async_scroll_turn()
    assert result is False
    result = line.async_scroll_turn()
    assert result is True
    result = line.async_scroll_turn()
    assert result is False


def test_add_char():
    line = pymatrix.SingleLine(5, 20, 20)
    line.add_char()
    assert len(line.data) == 0
    line.increment()
    with mock.patch.object(pymatrix, "choice", return_value="T"):
        line.add_char()
    assert len(line.data) == 1
    assert line.data == [(0, "T")]


def test_get_new():
    line = pymatrix.SingleLine(5, 20, 20)
    new = line.get_new()
    assert new is None
    line.increment()
    with mock.patch.object(pymatrix, "choice", return_value="T"):
        line.add_char()
        new = line.get_new()
    assert new == (0, 5, "T")


def test_get_lead():
    line = pymatrix.SingleLine(5, 20, 6)
    with mock.patch.object(pymatrix, "choice", return_value="T"):
        lead = line.get_lead()
    assert lead == (0, 5, "T")
    for _ in range(6):
        line.increment()
    lead = line.get_lead()
    assert lead is None


def test_get_remove_first_loop():
    line = pymatrix.SingleLine(5, 20, 6)
    line.add_char()
    rm = line.get_remove()
    assert rm is None


def test_get_remove_data_length():
    line = pymatrix.SingleLine(5, 20, 6)
    line.length = 3
    line.data = [(0, "T"), (1, "T"), (2, "T")]
    rm = line.get_remove()
    assert len(line.data) == 2
    assert rm == (0, 5, " ")


def test_get_remove_y_length():
    line = pymatrix.SingleLine(5, 20, 6)
    line.length = 5
    line.y = 5
    line.data = [(0, "T"), (1, "T"), (2, "T")]
    rm = line.get_remove()
    assert len(line.data) == 2
    assert rm == (0, 5, " ")


def test_get_remove_past_height():
    line = pymatrix.SingleLine(5, 20, 6)
    line.length = 5
    line.y = 5
    line.data = [(4, "T"), (5, "T")]
    rm = line.get_remove()
    assert len(line.data) == 1
    assert rm == (4, 5, " ")


def test_set_test_mode():
    pymatrix.SingleLine.set_test_mode(True, False)
    assert pymatrix.SingleLine.char_list == ["T"]
    pymatrix.SingleLine.set_test_mode(False, False)


@pytest.mark.parametrize("mode, ext, expected_result", [
    (True, False, ["T"]), (True, True, ["T", chr(35)]), (False, True, [chr(35)])
])
def test_set_test_mode_ext(mode, ext, expected_result):
    pymatrix.SingleLine.set_test_mode(mode, ext)
    assert pymatrix.SingleLine.char_list == expected_result
    pymatrix.SingleLine.set_test_mode(False, False)


@pytest.mark.parametrize("state, expected", [
    ("off", pymatrix.CHAR_LIST),
    ("on", pymatrix.CHAR_LIST + pymatrix.EXT_CHAR_LIST),
    ("only", pymatrix.EXT_CHAR_LIST),
])
def test_set_extended_chars(state, expected):
    pymatrix.SingleLine.set_extended_chars(state)
    assert pymatrix.SingleLine.char_list == expected


def test_zero_and_one():
    pymatrix.SingleLine.set_zero_one(True)
    assert pymatrix.SingleLine.char_list == ["0", "1"]
    pymatrix.SingleLine.set_zero_one(False)
    assert pymatrix.SingleLine.char_list == pymatrix.CHAR_LIST
