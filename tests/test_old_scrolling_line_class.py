import pytest
from unittest import mock

from pymatrix import pymatrix


def test_init():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        with mock.patch.object(pymatrix.random, "choice", return_value="X"):
            test_line = pymatrix.OldScrollingLine(5, 10, 10)
            assert test_line.height == 8
            assert test_line.width == 9
            assert test_line.y == -1
            assert test_line.x == 5
            assert test_line.length == 3
            assert test_line.lead_y == 0
            assert test_line.lead_char == "X"
            assert test_line.location_list == []
            assert test_line.line_color_number == 3


@pytest.mark.parametrize("value, expected", [
    (1, True), (2, False), (3, False),
])
def test_init_bold(value, expected):
    with mock.patch.object(pymatrix.random,"choice", return_value=["X"]):
        with mock.patch.object(pymatrix.random, "randint", return_value=value):
            test_line = pymatrix.OldScrollingLine(5, 10, 10)
            assert test_line.bold == expected


def test_old_school_char_list_start():
    assert pymatrix.OldScrollingLine.old_scroll_chr_list == []


def test_update_char_list():
    pymatrix.OldScrollingLine.update_char_list(["t", "1"])
    assert pymatrix.OldScrollingLine.old_scroll_chr_list == ["t", "1"]


def test_get_lead_first():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            lead = test_line.get_lead()
            assert lead == (0, 5, "X")


def test_get_lead_second():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            _ = test_line.get_lead()
            lead = test_line.get_lead()
            assert lead == (1, 5, "X")


def test_get_lead_last():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            test_line.lead_y = 3
            lead = test_line.get_lead()
            assert lead == (3, 5, "X")


def test_get_lead_off_screen():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            test_line.lead_y = 4
            lead = test_line.get_lead()
            assert lead is None


def test_get_next_first():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            line_list = test_line.get_next()
            assert line_list == []


def test_get_next_second():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            _ = test_line.get_next()
            line_list = test_line.get_next()
            assert line_list == [[0, 5, "X"]]


def test_get_next_third():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            for x in range(2):
                _ = test_line.get_next()
            line_list = test_line.get_next()
            assert line_list == [[1, 5, "X"], [0, 5, "X"]]


def test_get_next_line_length():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            for x in range(4):
                _ = test_line.get_next()
            line_list = test_line.get_next()
            assert line_list == [[3, 5, "X"], [2, 5, "X"], [1, 5, "X"]]


def test_get_next_off_screen():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            for x in range(5):
                _ = test_line.get_next()
            line_list = test_line.get_next()
            assert line_list == [[3, 5, "X"], [2, 5, "X"]]


def test_delete_last_first():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            remove = test_line.delete_last()
            assert remove is None


def test_delete_last_line_length():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            for x in range(4):
                _ = test_line.get_next()
            remove = test_line.delete_last()
            assert remove == [0, 5]


def test_delete_last_line_length_next():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            for x in range(5):
                _ = test_line.get_next()
            remove = test_line.delete_last()
            assert remove == [1, 5]


def test_okay_to_delete_first():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is False


def test_okay_to_delete_done():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 5)
            test_line.location_list = []
            test_line.y = 4
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is True


def test_full_line_run():
    with mock.patch.object(pymatrix.random, "choice", return_value="X"):
        with mock.patch.object(pymatrix.random, "randint", return_value=3):
            test_line = pymatrix.OldScrollingLine(5, 10, 6)
            # round 1
            remove = test_line.delete_last()
            assert remove is None
            lead = test_line.get_lead()
            assert lead == (0, 5, "X")
            loc_list = test_line.get_next()
            assert loc_list == []
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is False
            # round 2
            remove = test_line.delete_last()
            assert remove is None
            lead = test_line.get_lead()
            assert lead == (1, 5, "X")
            loc_list = test_line.get_next()
            assert loc_list == [[0, 5, "X"]]
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is False
            # round 3
            remove = test_line.delete_last()
            assert remove is None
            lead = test_line.get_lead()
            assert lead == (2, 5, "X")
            loc_list = test_line.get_next()
            assert loc_list == [[1, 5, "X"], [0, 5, "X"]]
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is False
            # round 4
            remove = test_line.delete_last()
            assert remove is None
            lead = test_line.get_lead()
            assert lead == (3, 5, "X")
            loc_list = test_line.get_next()
            assert loc_list == [[2, 5, "X"], [1, 5, "X"], [0, 5, "X"]]
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is False
            # round 5
            remove = test_line.delete_last()
            assert remove == [0, 5]
            lead = test_line.get_lead()
            assert lead == (4, 5, "X")
            loc_list = test_line.get_next()
            assert loc_list == [[3, 5, "X"], [2, 5, "X"], [1, 5, "X"]]
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is False
            # round 6
            remove = test_line.delete_last()
            assert remove == [1, 5]
            lead = test_line.get_lead()
            assert lead is None
            loc_list = test_line.get_next()
            assert loc_list == [[4, 5, "X"], [3, 5, "X"], [2, 5, "X"]]
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is False
            # round 7
            remove = test_line.delete_last()
            assert remove == [2, 5]
            lead = test_line.get_lead()
            assert lead is None
            loc_list = test_line.get_next()
            assert loc_list == [[4, 5, "X"], [3, 5, "X"]]
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is False
            # round 8
            remove = test_line.delete_last()
            assert remove == [3, 5]
            lead = test_line.get_lead()
            assert lead is None
            loc_list = test_line.get_next()
            assert loc_list == [[4, 5, "X"]]
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is False
            # round 9
            remove = test_line.delete_last()
            assert remove == [4, 5]
            lead = test_line.get_lead()
            assert lead is None
            loc_list = test_line.get_next()
            assert loc_list == []
            okay_to_delete = test_line.okay_to_delete()
            assert okay_to_delete is True
