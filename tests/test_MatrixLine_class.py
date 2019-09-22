
from unittest import mock
import pytest

import pymatrix


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
            _, b, _ = line.get_line()
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


def test_matrix_line_get_line_first_run_lead_true(setup_matrix_line):
    """ Lead char is True"""
    line = setup_matrix_line()
    with mock.patch.object(line, "lead_char_on", True):
        with mock.patch.object(line, "x_location", 2):
            lead, body, rm = line.get_line()
            assert lead == (0, 2, "T")
            # assert lead[0] == 0
            assert body is False
            assert rm is False


def test_matrix_line_get_line_first_run_lead_false(set_screen_size):
    """ Lead char is False"""
    line = pymatrix.MatrixLine()
    with mock.patch.object(line, "lead_char_on", False):
        lead, body, rm = line.get_line()
        assert lead is False
        assert body is False
        assert rm is False


def test_matrix_line_get_line_second_run_lead_true(setup_matrix_line):
    line = setup_matrix_line()
    with mock.patch.object(line, "lead_char_on", True):
        with mock.patch.object(line, "x_location", 2):
            line.get_line()  # first run
            lead, body, rm = line.get_line()  # second run
            assert lead == (1, 2, "T")
            assert body == [0, 2, "T"]
            assert rm is False


def test_matrix_line_get_line_third_run_lead_true(setup_matrix_line):
    line = setup_matrix_line()
    with mock.patch.object(line, "lead_char_on", True):
        with mock.patch.object(line, "x_location", 2):
            for _ in range(2):
                line.get_line()
            lead, body, rm = line.get_line()  # third run
            assert lead == (2, 2, "T")
            assert body == [1, 2, "T"]
            assert rm is False


def test_matrix_line_get_line_lead_off_screen(setup_matrix_line):
    line = setup_matrix_line()
    with mock.patch.object(line, "lead_char_on", True):
        with mock.patch.object(line, "x_location", 2):
            for _ in range(49):
                line.get_line()
            lead, _, _ = line.get_line()
            assert lead is False









