""" Matrix style rain using Python 3 and curses. """
import argparse
import curses
import sys
from random import choice, randint
from time import sleep

version = "0.1"

char_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
             "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B",
             "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
             "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3",
             "4", "5", "6", "7", "8", "9", "!", "#", "$", "%", "^", "&", "(", ")",
             "-", "+", "=", "[", "]", "{", "}", "|", ";", ":", "<", ">", ",", ".",
             "?", ]

delay_speed = {0: 0.005, 1: 0.01, 2: 0.025, 3: 0.04, 4: 0.055, 5: 0.07,
               6: 0.085, 7: 0.1, 8: 0.115, 9: 0.13}


class PyMatrixError(Exception):
    pass


class MatrixLine:
    all_x_locations_list = []
    screen_size_y = 0
    screen_size_x = 0
    char_list = char_list

    def __init__(self):
        self.x_location = 0
        self._set_random_x_location()
        self.line_length = randint(5, MatrixLine.screen_size_y) - 3
        self.lead_char_on = False if randint(0, 9) < 2 else True
        self.y_location_lead = 0
        self.y_location_tail = 0 - self.line_length

    def get_line(self):
        if self.lead_char_on and self.y_location_lead < MatrixLine.screen_size_y:
            lead = self.y_location_lead, self.x_location, choice(MatrixLine.char_list)
        else:
            lead = False
        if self.y_location_lead == 0:
            loc_char = False
        elif self.line_length >= self.y_location_lead >= 1:
            loc_char = [self.y_location_lead - 1, self.x_location, choice(MatrixLine.char_list)]

        elif self.y_location_lead <= MatrixLine.screen_size_y:
            if self.x_location in MatrixLine.all_x_locations_list:
                # Free up the x location
                MatrixLine.all_x_locations_list.remove(self.x_location)

            loc_char = [self.y_location_lead - 1, self.x_location, choice(MatrixLine.char_list)]

        elif self.y_location_tail < MatrixLine.screen_size_y:
            loc_char = False
        else:
            return False, None, False

        if self.y_location_tail >= 0:
            remove = self.y_location_tail, self.x_location
        else:
            remove = False

        self.y_location_lead += 1
        self.y_location_tail += 1
        return lead, loc_char, remove

    def _set_random_x_location(self):
        while True:
            x = randint(0, MatrixLine.screen_size_x - 1)
            if x not in MatrixLine.all_x_locations_list:
                MatrixLine.all_x_locations_list.append(x)
                self.x_location = x
                break

    @classmethod
    def set_screen_size(cls, y, x):
        MatrixLine.screen_size_y = y - 1
        MatrixLine.screen_size_x = x

    @classmethod
    def reset_lines(cls):
        MatrixLine.all_x_locations_list.clear()


def matrix_loop(screen, delay):
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    size_y, size_x = screen.getmaxyx()
    if size_y <= 3:
        raise PyMatrixError("Error screen height is to short.")

    MatrixLine.set_screen_size(size_y, size_x)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    line_list = []

    while True:
        if len(line_list) < size_x:
            line_list.append(MatrixLine())

        resize = curses.is_term_resized(size_y, size_x)
        if resize is True:
            size_y, size_x = screen.getmaxyx()
            if size_y <= 3:
                raise PyMatrixError("Error screen height is to short.")
            MatrixLine.reset_lines()
            MatrixLine.set_screen_size(size_y, size_x)
            line_list.clear()
            screen.clear()
            screen.refresh()
            continue

        remove_list = []
        for line in line_list:
            lead, current, rm = line.get_line()
            if lead:
                screen.addstr(lead[0], lead[1], lead[2], curses.color_pair(1) + curses.A_BOLD)
            if current:
                screen.addstr(current[0], current[1], current[2], curses.color_pair(2))

            if current is None:
                remove_list.append(line)
            if rm:
                screen.addstr(rm[0], rm[1], " ")

        for r in remove_list:
            line_list.remove(r)

        screen.refresh()
        ch = screen.getch()
        if ch in [81, 113]:
            screen.clear()
            screen.refresh()
            break
        sleep(delay_speed[delay])


def positive_int_zero_to_nine(value):
    """
    Used with argparse module.
    Checks to see if value is positive int between 0 and 10.
    """
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= 10:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive "
                                             f"int value 0 to 9")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int "
                                         f"value 0 to 9")


def argument_parsing(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="delay", type=positive_int_zero_to_nine,
                        default=4, help="Set the delay (speed) 0: Fast, 4: Default, 9: Slow")
    return parser.parse_args(argv)


def main(argv):
    args = argument_parsing(argv)
    try:
        curses.wrapper(matrix_loop, args.delay)
    except PyMatrixError as e:
        print(e)
        return


if __name__ == "__main__":
    main(sys.argv[1:])
