from unittest import mock

from pymatrix import pymatrix


def test_get_lead_down():
    line = pymatrix.SingleLine(0, 5, 20, 20, "down")
    lead_char = line.get_lead()
    assert lead_char is not None
    assert lead_char[0] == 0
    assert lead_char[1] == 5


def test_get_lead_down_off_screen():
    line = pymatrix.SingleLine(50, 5, 20, 20, "down")
    line.lead_y = 18
    line.get_lead()
    lead_char = line.get_lead()
    assert lead_char is None


def test_get_lead_down_increment():
    line = pymatrix.SingleLine(0, 5, 20, 20, "down")
    line.get_lead()
    assert line.lead_y == 1
    assert line.x == 5
    assert line.y == -1


def test_get_lead_up():
    line = pymatrix.SingleLine(0, 5, 20, 20, "up")
    lead_char = line.get_lead()
    assert lead_char is not None
    assert lead_char[0] == 18
    assert lead_char[1] == 5


def test_get_lead_up_off_screen():
    line = pymatrix.SingleLine(0, 5, 20, 20, "up")
    line.lead_y = 0
    line.get_lead()
    lead_char = line.get_lead()
    assert lead_char is None


def test_get_lead_up_increment():
    line = pymatrix.SingleLine(0, 5, 20, 20, "up")
    line.get_lead()
    assert line.lead_y == 17
    assert line.x == 5
    assert line.y == 19


def test_get_lead_right():
    line = pymatrix.SingleLine(5, 0, 20, 20, "right")
    lead_char = line.get_lead()
    assert lead_char is not None
    assert lead_char[0] == 5
    assert lead_char[1] == 0


def test_get_lead_right_off_screen():
    line = pymatrix.SingleLine(5, 0, 20, 20, "right")
    line.lead_x = 18
    line.get_lead()
    lead_char = line.get_lead()
    assert lead_char is None


def test_get_lead_right_increment():
    line = pymatrix.SingleLine(5, 0, 20, 20, "right")
    line.get_lead()
    assert line.lead_x == 1
    assert line.x == -1
    assert line.y == 5


def test_get_lead_left():
    line = pymatrix.SingleLine(5, 0, 20, 20, "left")
    lead_char = line.get_lead()
    assert lead_char is not None
    assert lead_char[0] == 5
    assert lead_char[1] == 18


def test_get_lead_left_off_screen():
    line = pymatrix.SingleLine(5, 0, 20, 20, "left")
    line.lead_x = 0
    line.get_lead()
    lead_char = line.get_lead()
    assert lead_char is None


def test_get_lead_left_increment():
    line = pymatrix.SingleLine(5, 0, 20, 20, "left")
    line.get_lead()
    assert line.lead_x == 17
    assert line.x == 19
    assert line.y == 5


def test_get_next_down():
    line = pymatrix.SingleLine(0, 5, 20, 20, "down")
    next_char = line.get_next()
    assert next_char is None


def test_get_next_down_second_loop():
    line = pymatrix.SingleLine(0, 5, 20, 20, "down")
    line.get_next()  # first loop
    next_char = line.get_next()
    assert next_char is not None
    assert next_char[0] == 0
    assert next_char[1] == 5


def test_get_next_down_off_screen():
    line = pymatrix.SingleLine(0, 5, 20, 20, "down")
    line.y = 18
    line.get_next()
    next_char = line.get_next()
    assert next_char is None


def test_get_next_down_increment():
    line = pymatrix.SingleLine(0, 5, 20, 20, "down")
    line.get_next()
    assert line.x == 5
    assert line.y == 0
    assert line.lead_y == 0


def test_get_next_right():
    line = pymatrix.SingleLine(5, 0, 20, 20, "right")
    next_char = line.get_next()
    assert next_char is None


def test_get_next_right_second_loop():
    line = pymatrix.SingleLine(5, 0, 20, 20, "right")
    line.get_next()  # first loop
    next_char = line.get_next()
    assert next_char is not None
    assert next_char[0] == 5
    assert next_char[1] == 0


def test_get_next_right_increment():
    line = pymatrix.SingleLine(5, 0, 20, 20, "right")
    line.get_next()
    assert line.x == 0
    assert line.y == 5
    assert line.lead_x == 0


def test_get_next_right_off_screen():
    line = pymatrix.SingleLine(0, 5, 20, 20, "right")
    line.x = 18
    line.get_next()
    next_char = line.get_next()
    assert next_char is None


def test_get_next_left():
    line = pymatrix.SingleLine(5, 0, 20, 20, "left")
    next_char = line.get_next()
    assert next_char is None


def test_get_next_left_second_loop():
    line = pymatrix.SingleLine(5, 0, 20, 20, "left")
    line.get_next()  # first loop
    next_char = line.get_next()
    assert next_char is not None
    assert next_char[0] == 5
    assert next_char[1] == 18


def test_get_next_left_increment():
    line = pymatrix.SingleLine(5, 0, 20, 20, "left")
    line.get_next()
    assert line.x == 18
    assert line.y == 5
    assert line.lead_x == 18


def test_get_next_left_off_screen():
    line = pymatrix.SingleLine(0, 5, 20, 20, "left")
    line.x = 0
    line.get_next()
    next_char = line.get_next()
    assert next_char is None


def test_get_next_up():
    line = pymatrix.SingleLine(0, 5, 20, 20, "up")
    next_char = line.get_next()
    assert next_char is None


def test_get_next_up_second_loop():
    line = pymatrix.SingleLine(0, 5, 20, 20, "up")
    line.get_next()  # first loop
    next_char = line.get_next()
    assert next_char is not None
    assert next_char[0] == 18
    assert next_char[1] == 5


def test_get_next_up_off_screen():
    line = pymatrix.SingleLine(0, 5, 20, 20, "up")
    line.y = 0
    line.get_next()
    next_char = line.get_next()
    assert next_char is None


def test_get_next_up_increment():
    line = pymatrix.SingleLine(0, 5, 20, 20, "up")
    line.get_next()
    assert line.x == 5
    assert line.y == 18
    assert line.lead_y == 18


def test_delete_last_down_none():
    line = pymatrix.SingleLine(0, 5, 20, 6, "down")
    delete_last = line.delete_last()
    assert delete_last is None


def test_delete_last_down_delete():
    line = pymatrix.SingleLine(0, 5, 20, 6, "down")
    line.last_y = 0  # patch
    delete_last = line.delete_last()
    assert delete_last is not None
    assert delete_last[0] == 0
    assert delete_last[1] == 5


def test_delete_last_down_stop():
    line = pymatrix.SingleLine(0, 5, 20, 6, "down")
    line.last_y = 4  # patch
    line.delete_last()
    delete_last = line.delete_last()
    assert delete_last is None


def test_delete_last_down_last_y_increment():
    line = pymatrix.SingleLine(0, 5, 20, 6, "down")
    line.delete_last()
    assert line.y == -1
    assert line.lead_y == 0
    assert line.last_y == -2


def test_delete_last_up_none():
    line = pymatrix.SingleLine(0, 5, 20, 6, "up")
    delete_last = line.delete_last()
    assert delete_last is None


def test_delete_last_up_delete():
    line = pymatrix.SingleLine(0, 5, 20, 6, "up")
    line.last_y = 4  # patch
    delete_last = line.delete_last()
    assert delete_last is not None
    assert delete_last[0] == 4
    assert delete_last[1] == 5


def test_delete_last_up_stop():
    line = pymatrix.SingleLine(0, 5, 20, 6, "up")
    line.last_y = 0  # patch
    line.delete_last()
    delete_last = line.delete_last()
    assert delete_last is None


def test_delete_last_up_last_y_increment():
    line = pymatrix.SingleLine(0, 5, 20, 6, "up")
    line.delete_last()
    assert line.y == 5
    assert line.lead_y == 4
    assert line.last_y == 5


def test_delete_last_right_none():
    line = pymatrix.SingleLine(5, 0, 20, 6, "right")
    delete_last = line.delete_last()
    assert delete_last is None


def test_delete_last_right_delete():
    line = pymatrix.SingleLine(5, 0, 20, 6, "right")
    line.last_x = 0  # patch
    delete_last = line.delete_last()
    assert delete_last is not None
    assert delete_last[0] == 5
    assert delete_last[1] == 0


def test_delete_last_right_stop():
    line = pymatrix.SingleLine(5, 0, 6, 20, "right")
    line.last_x = 4  # patch
    line.delete_last()
    delete_last = line.delete_last()
    assert delete_last is None


def test_delete_last_right_last_x_increment():
    line = pymatrix.SingleLine(5, 0, 6, 20, "right")
    line.delete_last()
    assert line.x == -1
    assert line.lead_x == 0
    assert line.last_x == -2


def test_delete_last_left_none():
    line = pymatrix.SingleLine(5, 0, 20, 6, "left")
    delete_last = line.delete_last()
    assert delete_last is None


def test_delete_last_left_delete():
    line = pymatrix.SingleLine(5, 0, 20, 6, "left")
    line.last_x = 18  # patch
    delete_last = line.delete_last()
    assert delete_last is not None
    assert delete_last[0] == 5
    assert delete_last[1] == 18


def test_delete_last_left_stop():
    line = pymatrix.SingleLine(5, 0, 6, 20, "left")
    line.last_x = 6  # patch
    line.delete_last()
    delete_last = line.delete_last()
    assert delete_last is None


def test_delete_last_left_last_x_increment():
    line = pymatrix.SingleLine(5, 0, 6, 20, "left")
    line.delete_last()
    assert line.x == 5
    assert line.lead_x == 4
    assert line.last_x == 6


def test_okay_to_delete_down_false():
    line = pymatrix.SingleLine(0, 5, 20, 6, "down")
    ok_delete = line.okay_to_delete()
    assert ok_delete is False


def test_okay_to_delete_down_true():
    line = pymatrix.SingleLine(0, 5, 20, 6, "down")
    line.last_y = 5  # patch
    line.delete_last()
    ok_delete = line.okay_to_delete()
    assert ok_delete is True


def test_okay_to_delete_up_false():
    line = pymatrix.SingleLine(0, 5, 20, 6, "up")
    ok_delete = line.okay_to_delete()
    assert ok_delete is False


def test_okay_to_delete_up_true():
    line = pymatrix.SingleLine(0, 5, 20, 6, "up")
    line.last_y = 0  # patch
    line.delete_last()
    ok_delete = line.okay_to_delete()
    assert ok_delete is True


def test_okay_to_delete_right_false():
    line = pymatrix.SingleLine(5, 0, 20, 6, "right")
    ok_delete = line.okay_to_delete()
    assert ok_delete is False


def test_okay_to_delete_right_true():
    line = pymatrix.SingleLine(5, 0, 6, 20, "right")
    line.last_x = 5  # patch
    line.delete_last()
    ok_delete = line.okay_to_delete()
    assert ok_delete is True


def test_okay_to_delete_left_false():
    line = pymatrix.SingleLine(5, 0, 20, 6, "left")
    ok_delete = line.okay_to_delete()
    assert ok_delete is False


def test_okay_to_delete_left_true():
    line = pymatrix.SingleLine(5, 0, 6, 20, "left")
    line.last_x = 0  # patch
    line.delete_last()
    ok_delete = line.okay_to_delete()
    assert ok_delete is True


def test_async_scroll_turn():
    line = pymatrix.SingleLine(0, 5, 20, 6, "down")
    line.async_scroll_rate = 1
    turn = line.async_scroll_turn()
    assert turn is False
    turn = line.async_scroll_turn()
    assert turn is True
    turn = line.async_scroll_turn()
    assert turn is False


def test_async_scroll_turn_right():
    line = pymatrix.SingleLine(0, 5, 20, 6, "right")
    line.async_scroll_rate = 1
    turn = line.async_scroll_turn()
    assert turn is False
    turn = line.async_scroll_turn()
    assert turn is True
    turn = line.async_scroll_turn()
    assert turn is False


def test_single_line_class_down_init():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(0, 5, 20, 6, "down")
        assert line.direction == "down"
        assert line.height == 4
        assert line.x == 5
        assert line.async_scroll_count == 0
        assert line.async_scroll_rate == 3
        assert line.line_color_number == 3
        assert line.lead_y == 0
        assert line.y == -1
        assert line.last_y == -3


def test_single_line_class_up_init():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(0, 5, 20, 6, "up")
        assert line.direction == "up"
        assert line.height == 4
        assert line.x == 5
        assert line.async_scroll_count == 0
        assert line.async_scroll_rate == 3
        assert line.line_color_number == 3
        assert line.lead_y == 4
        assert line.y == 5
        assert line.last_y == 6


def test_single_line_class_right_init():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(5, 0, 6, 20, "right")
        assert line.direction == "right"
        assert line.height == 18
        assert line.width == 5
        assert line.x == -1
        assert line.y == 5
        assert line.async_scroll_count == 0
        assert line.async_scroll_rate == 3
        assert line.line_color_number == 3
        assert line.lead_x == 0
        assert line.last_x == -3
        assert line.lead_y == 0
        assert line.last_y == 0


def test_single_line_class_left_init():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(5, 0, 6, 20, "left")
        assert line.direction == "left"
        assert line.height == 18
        assert line.width == 5
        assert line.x == 5
        assert line.y == 5
        assert line.async_scroll_count == 0
        assert line.async_scroll_rate == 3
        assert line.line_color_number == 3
        assert line.lead_y == 0
        assert line.last_y == 0
        assert line.lead_x == 4
        assert line.last_x == 7


def test_single_line_class_down_one_turn():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(0, 5, 20, 6, "down")
        lead_char = line.get_lead()
        assert lead_char == (0, 5)
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False


def test_single_line_class_up_one_turn():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(0, 5, 20, 6, "up")
        lead_char = line.get_lead()
        assert lead_char == (4, 5)
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False


def test_single_line_class_right_one_turn():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(5, 0, 6, 20, "right")
        lead_char = line.get_lead()
        assert lead_char == (5, 0)
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False


def test_single_line_class_left_one_turn():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(5, 0, 6, 20, "left")
        lead_char = line.get_lead()
        assert lead_char == (5, 4)
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False


def test_single_line_class_down_multiple():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(0, 5, 20, 6, "down")
        line.get_lead()
        line.get_next()
        line.delete_last()
        line.okay_to_delete()
        lead_char = line.get_lead()
        assert lead_char == (1, 5)
        next_char = line.get_next()
        assert next_char == (0, 5)
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (2, 5)
        next_char = line.get_next()
        assert next_char == (1, 5)
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (3, 5)
        next_char = line.get_next()
        assert next_char == (2, 5)
        delete_last = line.delete_last()
        assert delete_last == (0, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (4, 5)
        next_char = line.get_next()
        assert next_char == (3, 5)
        delete_last = line.delete_last()
        assert delete_last == (1, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char == (4, 5)
        delete_last = line.delete_last()
        assert delete_last == (2, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last == (3, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last == (4, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is True


def test_single_line_class_up_multiple():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(0, 5, 20, 6, "up")
        line.get_lead()
        line.get_next()
        line.delete_last()
        line.okay_to_delete()
        lead_char = line.get_lead()
        assert lead_char == (3, 5)
        next_char = line.get_next()
        assert next_char == (4, 5)
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (2, 5)
        next_char = line.get_next()
        assert next_char == (3, 5)
        delete_last = line.delete_last()
        assert delete_last == (4, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (1, 5)
        next_char = line.get_next()
        assert next_char == (2, 5)
        delete_last = line.delete_last()
        assert delete_last == (3, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (0, 5)
        next_char = line.get_next()
        assert next_char == (1, 5)
        delete_last = line.delete_last()
        assert delete_last == (2, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char == (0, 5)
        delete_last = line.delete_last()
        assert delete_last == (1, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last == (0, 5)
        ok_delete = line.okay_to_delete()
        assert ok_delete is True


def test_single_line_class_right_multiple():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(5, 0, 6, 20, "right")
        line.get_lead()
        line.get_next()
        line.delete_last()
        line.okay_to_delete()
        lead_char = line.get_lead()
        assert lead_char == (5, 1)
        next_char = line.get_next()
        assert next_char == (5, 0)
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (5, 2)
        next_char = line.get_next()
        assert next_char == (5, 1)
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (5, 3)
        next_char = line.get_next()
        assert next_char == (5, 2)
        delete_last = line.delete_last()
        assert delete_last == (5, 0)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (5, 4)
        next_char = line.get_next()
        assert next_char == (5, 3)
        delete_last = line.delete_last()
        assert delete_last == (5, 1)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char == (5, 4)
        delete_last = line.delete_last()
        assert delete_last == (5, 2)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last == (5, 3)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last == (5, 4)
        ok_delete = line.okay_to_delete()
        assert ok_delete is True


def test_single_line_class_left_multiple():
    with mock.patch.object(pymatrix.random, "randint", return_value=3):
        line = pymatrix.SingleLine(5, 0, 6, 20, "left")
        line.get_lead()
        line.get_next()
        line.delete_last()
        line.okay_to_delete()
        lead_char = line.get_lead()
        assert lead_char == (5, 3)
        next_char = line.get_next()
        assert next_char == (5, 4)
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (5, 2)
        next_char = line.get_next()
        assert next_char == (5, 3)
        delete_last = line.delete_last()
        assert delete_last is None
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (5, 1)
        next_char = line.get_next()
        assert next_char == (5, 2)
        delete_last = line.delete_last()
        assert delete_last == (5, 4)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char == (5, 0)
        next_char = line.get_next()
        assert next_char == (5, 1)
        delete_last = line.delete_last()
        assert delete_last == (5, 3)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char == (5, 0)
        delete_last = line.delete_last()
        assert delete_last == (5, 2)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last == (5, 1)
        ok_delete = line.okay_to_delete()
        assert ok_delete is False

        lead_char = line.get_lead()
        assert lead_char is None
        next_char = line.get_next()
        assert next_char is None
        delete_last = line.delete_last()
        assert delete_last == (5, 0)
        ok_delete = line.okay_to_delete()
        assert ok_delete is True
