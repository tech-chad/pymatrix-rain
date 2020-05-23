from unittest import mock

import pytest

from pymatrix import pymatrix


@pytest.fixture
def set_screen_size():
    yield pymatrix.MatrixLine.set_screen_size(50, 50)

    pymatrix.MatrixLine.set_screen_size(0, 0)


@pytest.fixture
def setup_matrix_line():
    matrix_line = pymatrix.MatrixLine
    matrix_line.set_screen_size(50, 50)
    with mock.patch.object(matrix_line, "char_list", ["T"]):
        yield matrix_line

    matrix_line.set_screen_size(0, 0)


@pytest.mark.parametrize("test_values", [
    [5, 5], [10, 10], [50, 100], [200, 100], [525, 600]
])
def test_matrix_line_set_screen_size(test_values, set_screen_size):
    pymatrix.MatrixLine.set_screen_size(test_values[0], test_values[1])
    assert pymatrix.MatrixLine.screen_size_y == test_values[0] - 1
    assert pymatrix.MatrixLine.screen_size_x == test_values[1]


def test_matrix_line_all_x_locations_list(set_screen_size):
    """ Tests all_x_locations_list is being updated"""
    line_list = []
    for _ in range(2):
        line_list.append(pymatrix.MatrixLine())

    assert len(pymatrix.MatrixLine.all_x_locations_list) == 2

    while True:
        for line in line_list:
            b = line.get_line()
            if b is None:
                line_list.remove(line)
        if len(line_list) == 0:
            break
    assert len(pymatrix.MatrixLine.all_x_locations_list) == 0


def test_matrix_line_reset_lines(set_screen_size):
    line_list = []
    for _ in range(10):
        line_list.append(pymatrix.MatrixLine())

    pymatrix.MatrixLine.reset_lines()
    assert len(pymatrix.MatrixLine.all_x_locations_list) == 0


def test_matrix_line_lines_turn_async_scroll_off(setup_matrix_line):
    line = setup_matrix_line()
    # with mock.patch.object(line, "async_scroll", )
    turn = line.lines_turn()
    assert turn is True


def test_matrix_line_lines_turn_async_scroll_on_first_run():
    pymatrix.MatrixLine.set_screen_size(20, 20)
    line = pymatrix.MatrixLine()
    with mock.patch.object(pymatrix.MatrixLine, "async_scroll", True):
        with mock.patch.object(line, "async_scroll_rate", 2):
            turn = line.lines_turn()
            assert turn is False


def test_matrix_line_lines_turn_async_scroll_on_second_run():
    pymatrix.MatrixLine.set_screen_size(20, 20)
    line = pymatrix.MatrixLine()
    with mock.patch.object(pymatrix.MatrixLine, "async_scroll", True):
        with mock.patch.object(line, "async_scroll_rate", 1):
            _ = line.lines_turn()
            turn = line.lines_turn()
            assert turn is True


def test_matrix_line_get_line_first_run_lead_true(setup_matrix_line):
    """ Lead char is True"""
    line = setup_matrix_line()
    with mock.patch.object(line, "lead_char_on", True):
        with mock.patch.object(line, "x_location", 2):
            lead = line.get_lead()
            body = line.get_line()
            rm = line.get_remove_tail()
            assert lead == (0, 2, "T")
            # assert lead[0] == 0
            assert body is False
            assert rm is False


def test_matrix_line_get_line_first_run_lead_false(set_screen_size):
    """ Lead char is False"""
    line = pymatrix.MatrixLine()
    with mock.patch.object(line, "lead_char_on", False):
        lead = line.get_lead()
        body = line.get_line()
        rm = line.get_remove_tail()
        assert lead is False
        assert body is False
        assert rm is False


def test_matrix_line_get_line_second_run_lead_true(setup_matrix_line):
    line = setup_matrix_line()
    with mock.patch.object(line, "lead_char_on", True):
        with mock.patch.object(line, "x_location", 2):
            line.get_lead()
            line.get_line()  # first run
            line.get_remove_tail()

            lead = line.get_lead()
            body = line.get_line()  # second run1
            rm = line.get_remove_tail()
            assert lead == (1, 2, "T")
            assert body == [0, 2, "T"]
            assert rm is False


def test_matrix_line_get_line_third_run_lead_true(setup_matrix_line):
    line = setup_matrix_line()
    with mock.patch.object(line, "lead_char_on", True):
        with mock.patch.object(line, "x_location", 2):
            for _ in range(2):
                line.get_lead()
                line.get_line()
                line.get_remove_tail()
            lead = line.get_lead()
            body = line.get_line()  # third run
            rm = line.get_remove_tail()
            assert lead == (2, 2, "T")
            assert body == [1, 2, "T"]
            assert rm is False


def test_matrix_line_get_line_lead_off_screen(setup_matrix_line):
    line = setup_matrix_line()
    with mock.patch.object(line, "lead_char_on", True):
        with mock.patch.object(line, "x_location", 2):
            for _ in range(49):
                line.get_lead()
                line.get_line()
                line.get_remove_tail()
            line.get_line()
            lead = line.get_lead()
            line.get_remove_tail()
            assert lead is False


def test_matrix_line_test_mode():
    assert len(pymatrix.MatrixLine.char_list) > 1
    pymatrix.MatrixLine.test_mode()
    assert len(pymatrix.MatrixLine.char_list) == 1
    pymatrix.MatrixLine.test_mode()
    assert len(pymatrix.MatrixLine.char_list) > 1


def test_matrix_line_async_mode():
    assert pymatrix.MatrixLine.async_scroll is False
    pymatrix.MatrixLine.async_mode()
    assert pymatrix.MatrixLine.async_scroll is True
    pymatrix.MatrixLine.async_mode()
    assert pymatrix.MatrixLine.async_scroll is False


def test_matrix_line_async_mode_set():
    pymatrix.MatrixLine.async_mode(set_mode=True)
    assert pymatrix.MatrixLine.async_scroll is True
    pymatrix.MatrixLine.async_mode(set_mode=True)
    assert pymatrix.MatrixLine.async_scroll is True
    pymatrix.MatrixLine.async_mode(set_mode=False)
    assert pymatrix.MatrixLine.async_scroll is False
    pymatrix.MatrixLine.async_mode(set_mode=False)
    assert pymatrix.MatrixLine.async_scroll is False


def test_matrix_line_get_line_color(setup_matrix_line):
    with mock.patch.object(pymatrix, "COLOR_NUMBERS", {"red": 1}):
        line = setup_matrix_line()
        result = line.get_line_color()
        assert result == "red"
