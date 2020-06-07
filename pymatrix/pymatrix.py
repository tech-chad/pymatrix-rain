#! /usr/bin/python3
""" Matrix style rain using Python 3 and curses. """
import argparse
import curses
import datetime
import getpass
import hashlib
import sys

from random import choice
from random import randint
from time import sleep

from typing import Tuple
from typing import Union

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

version = importlib_metadata.version("pymatrix-rain")

CHAR_LIST = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
             "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B",
             "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
             "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3",
             "4", "5", "6", "7", "8", "9", "!", "#", "$", "%", "^", "&", "(", ")",
             "-", "+", "=", "[", "]", "{", "}", "|", ";", ":", "<", ">", ",", ".",
             "?", "~", "`", "@", "*", "_", "'", "\\", "/", '"']

DELAY_SPEED = {0: 0.005, 1: 0.01, 2: 0.025, 3: 0.04, 4: 0.055, 5: 0.07,
               6: 0.085, 7: 0.1, 8: 0.115, 9: 0.13}

COLOR_NUMBERS = {"red": 1, "green": 2, "blue": 3, "yellow": 4, "magenta": 5,
                 "cyan": 6, "white": 7}

CURSES_COLOR = {"red": curses.COLOR_RED, "green": curses.COLOR_GREEN,
                "blue": curses.COLOR_BLUE, "yellow": curses.COLOR_YELLOW,
                "magenta": curses.COLOR_MAGENTA, "cyan": curses.COLOR_CYAN,
                "white": curses.COLOR_WHITE}

CURSES_CH_CODES = {48: 0, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7, 56: 8, 57: 9}

CURSES_CH_CODES_COLOR = {114: "red", 82: "red", 116: "green", 84: "green",
                         121: "blue", 89: "blue", 117: "yellow", 85: "yellow",
                         105: "magenta", 73: "magenta", 111: "cyan",
                         79: "cyan", 112: "white", 80: "white"}


class PyMatrixError(Exception):
    pass


class SingleLine:
    async_scroll = False
    char_list = CHAR_LIST

    def __init__(self, x: int, width: int, height: int) -> None:
        self.y = -1
        self.x = x
        self.length = randint(3, height - 3)
        self.data = []
        self.lead_y = 0
        self.width = width
        self.height = height - 2
        self.line_color_number = randint(1, 7)
        self.async_scroll_rate = randint(0, 3)
        self.async_scroll_position = 0

    def increment(self) -> None:
        """ moves the lead y position and y position """
        if self.lead_y <= self.height:
            self.lead_y += 1
        if self.y <= self.height:
            self.y += 1

    def async_scroll_turn(self) -> bool:
        """ Checks to see if lines turn when async like scrolling is on"""
        if self.async_scroll_position == self.async_scroll_rate:
            self.async_scroll_position = 0
            return True
        else:
            self.async_scroll_position += 1
            return False

    def add_char(self) -> None:
        """ Adds a random char to the line """
        if 0 <= self.y <= self.height:
            self.data.append((self.y, choice(SingleLine.char_list)))
        else:
            return None

    def get_new(self) -> Union[Tuple[int, int, str], None]:
        """ Gets the last char that was added"""
        if 0 <= self.y <= self.height and len(self.data) > 0:
            new = (self.data[-1][0], self.x, self.data[-1][1])
            return new
        else:
            return None

    def get_lead(self) -> Union[Tuple[int, int, str], None]:
        """ Gets the lead char """
        if self.lead_y < self.height:
            return self.lead_y, self.x, choice(SingleLine.char_list)
        else:
            return None

    def get_remove(self) -> Union[Tuple[int, int, str], None]:
        """ Remove char from list and returns the location to erase """
        if len(self.data) >= self.length or self.y >= self.height and len(self.data) >= 0:
            rm = (self.data[0][0], self.x, " ")
            self.data.pop(0)
            return rm
        elif len(self.data) > 0 and self.data[0][0] >= self.height:
            rm = (self.data[0][0], self.x, " ")
            self.data.pop(0)
            return rm
        return None

    @classmethod
    def set_test_mode(cls) -> None:
        SingleLine.char_list = ["T"]


def matrix_loop(screen, delay: int, bold_char: bool, bold_all: bool, screen_saver: bool,
                color: str, run_timer: int, lead_color: str, color_mode: str) -> None:
    """ Main loop. """
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    setup_curses_colors(color)
    curses_lead_color(lead_color)
    line_list = []
    count = cycle = 0  # used for cycle through colors mode

    if color_mode == "multiple" or color_mode == "random":
        setup_curses_colors("random")

    size_y, size_x = screen.getmaxyx()
    if size_y <= 3:
        raise PyMatrixError("Error screen height is to short.")

    x_list = [x for x in range(0, size_x)]

    end_time = datetime.datetime.now() + datetime.timedelta(seconds=run_timer)
    while True:
        if len(line_list) < size_x - 3:
            x = choice(x_list)
            x_list.pop(x_list.index(x))
            line_list.append(SingleLine(x, size_x, size_y))
            x = choice(x_list)
            x_list.pop(x_list.index(x))
            line_list.append(SingleLine(x, size_x, size_y))

        resize = curses.is_term_resized(size_y, size_x)
        if resize is True:
            size_y, size_x = screen.getmaxyx()
            if size_y <= 3:
                raise PyMatrixError("Error screen height is to short.")
            x_list = [x for x in range(0, size_x)]

            line_list.clear()
            screen.clear()
            screen.refresh()
            continue
        remove_list = []

        if color_mode == "cycle":
            if count <= 0:
                setup_curses_colors(list(CURSES_COLOR.keys())[cycle])
                count = 500
                cycle = 0 if cycle == 6 else cycle + 1
            else:
                count -= 1

        for line in line_list:
            if SingleLine.async_scroll and not line.async_scroll_turn():
                continue
            line.add_char()
            rm = line.get_remove()
            if rm:
                screen.addstr(rm[0], rm[1], rm[2])

            if bold_all:
                bold = curses.A_BOLD
            elif bold_char:
                bold = curses.A_BOLD if randint(1, 3) <= 1 else curses.A_NORMAL
            else:
                bold = curses.A_NORMAL

            new_line = line.get_new()
            if new_line:
                if color_mode == "random":
                    screen.addstr(new_line[0], new_line[1], new_line[2],
                                  curses.color_pair(randint(1, 7)) + bold)
                else:
                    screen.addstr(new_line[0], new_line[1], new_line[2],
                                  curses.color_pair(line.line_color_number) + bold)

            lead_char = line.get_lead()
            if lead_char:
                screen.addstr(lead_char[0], lead_char[1], lead_char[2],
                              curses.color_pair(10) + bold)

            line.increment()
            if len(line.data) <= 0 and line.y >= size_y - 2:
                remove_list.append(line)
        screen.refresh()

        for rem in remove_list:
            line_list.pop(line_list.index(rem))
            x_list.append(rem.x)

        if run_timer and datetime.datetime.now() >= end_time:
            break
        ch = screen.getch()
        if screen_saver and ch != -1:
            break
        elif ch != -1:
            # Commands:
            if ch == 98:  # b
                bold_char = True
                bold_all = False
            elif ch == 66:  # B
                bold_all = True
                bold_char = False
            elif ch in [78, 110]:  # n or N
                bold_char = False
                bold_all = False
            elif ch in [114, 116, 121, 117, 105, 111, 112]:
                # r, t, y, u, i, o, p
                setup_curses_colors(CURSES_CH_CODES_COLOR[ch])
                color_mode = "normal"
            elif ch in [82, 84, 89, 85, 73, 79, 80]:
                # R, T, Y, U, I, O, P
                curses_lead_color(CURSES_CH_CODES_COLOR[ch])
            elif ch == 97:  # a
                SingleLine.async_scroll = not SingleLine.async_scroll
            elif ch == 109:  # m
                if color_mode in ["random", "normal", "cycle"]:
                    color_mode = "multiple"
                    setup_curses_colors("random")
                else:
                    color_mode = "normal"
                    setup_curses_colors("green")

            elif ch == 77:  # M
                if color_mode in ["multiple", "normal", "cycle"]:
                    color_mode = "random"
                    setup_curses_colors("random")
                else:
                    color_mode = "normal"
                    setup_curses_colors("green")

            elif ch == 99:  # c
                if color_mode in ["random", "multiple", "normal"]:
                    color_mode = "cycle"
                else:
                    color_mode = "normal"
            elif ch in [100, 68]:  # d, D
                bold_char = False
                bold_all = False
                setup_curses_colors("green")
                curses_lead_color("white")
                color_mode = "normal"
                SingleLine.async_scroll = False
                delay = 4
            elif ch in [81, 113]:  # q, Q
                break
            elif ch in CURSES_CH_CODES.keys():
                delay = CURSES_CH_CODES[ch]
        sleep(DELAY_SPEED[delay])

    screen.erase()
    screen.refresh()


def curses_lead_color(color: str) -> None:
    curses.init_pair(10, CURSES_COLOR[color], curses.COLOR_BLACK)


def setup_curses_colors(color: str) -> None:
    """ Init colors pairs in the curses. """
    if color == "random":
        color_list = list(CURSES_COLOR.keys())
    else:
        color_list = [color for _ in range(7)]

    for x, c in enumerate(color_list):
        curses.init_pair(x + 1, CURSES_COLOR[c], curses.COLOR_BLACK)


def get_password():
    """ Gets the password and returns a hash of that password. """
    h = hashlib.sha3_512(b'ter34123fgfg')
    h.update(bytes(getpass.getpass("Enter password: "), "utf-8"))
    return h.hexdigest()


def positive_int_zero_to_nine(value: str) -> int:
    """
    Used with argparse.
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


def color_type(value: str) -> str:
    """
    Used with argparse
    Checks to see if the value is a valid color and returns
    the lower case color name.
    """
    lower_value = value.lower()
    if lower_value in COLOR_NUMBERS.keys():
        return lower_value
    raise argparse.ArgumentTypeError(f"{value} is an invalid color name")


def positive_int(value: str) -> int:
    """
    Used by argparse.
    Checks to see if the value is positive.
    """
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    else:
        if int_value <= 0:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return int_value


def display_commands() -> None:
    print("Commands available during run")
    print("0 - 9  Delay time (0-Fast, 4-Default, 9-Slow")
    print("b      Bold characters on")
    print("B      Bold all characters")
    print("n      Bold off (Default)")
    print("a      Asynchronous like scrolling")
    print("m      Multiple color mode")
    print("M      Multiple random color mode")
    print("c      Cycle colors")
    print("d      Restore all defaults")
    print("r,t,y,u,i,o,p   Set color")
    print("R,T,Y,U,I,O,P   Set lead character color")


def argument_parsing(argv: list) -> argparse.Namespace:
    """ Command line argument parsing. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="delay", type=positive_int_zero_to_nine, default=4,
                        help="Set the delay (speed) 0: Fast, 4: Default, 9: Slow")
    parser.add_argument("-b", dest="bold_on", action="store_true",
                        help="Bold characters on")
    parser.add_argument("-B", dest="bold_all", action="store_true",
                        help="All bold characters (overrides -b)")
    parser.add_argument("-s", dest="screen_saver", action="store_true",
                        help="Screen saver mode.  Any key will exit.")
    parser.add_argument("-a", dest="async_scroll", action="store_true",
                        help="enable asynchronous like scrolling")
    parser.add_argument("-S", dest="start_timer", type=positive_int, default=0,
                        metavar="SECONDS", help="Set start timer in seconds")
    parser.add_argument("-R", dest="run_timer", type=positive_int, default=0,
                        metavar="SECONDS", help="Set run timer in seconds")
    parser.add_argument("-C", dest="color", type=color_type, default="green",
                        help="Set color.  Default is green")
    parser.add_argument("-L", dest="lead_color", type=color_type, default="white",
                        help="Set the lead character color.  Default is white")
    parser.add_argument("-m", dest="multiple_mode", action="store_true",
                        help="Multiple color mode")
    parser.add_argument("-M", dest="random_mode", action="store_true",
                        help="Multiple random color mode")
    parser.add_argument("-c", dest="cycle", action="store_true",
                        help="cycle through the colors")
    parser.add_argument("-p", dest="use_password", action="store_true",
                        help="Password protect exit")
    parser.add_argument("--list_colors", action="store_true",
                        help="Show available colors and exit. ")
    parser.add_argument("--list_commands", action="store_true",
                        help="List Commands and exit")
    parser.add_argument("--version", action="version", version=f"Version: {version}")

    parser.add_argument("--test_mode", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: list = None) -> None:
    args = argument_parsing(argv)
    password = None

    if args.list_colors:
        print(*COLOR_NUMBERS.keys())
        return
    if args.list_commands:
        display_commands()
        return

    if args.use_password:
        password = get_password()

    if args.test_mode:
        SingleLine.set_test_mode()

    sleep(args.start_timer)

    if args.async_scroll:
        SingleLine.async_scroll = True

    if args.multiple_mode:
        color_mode = "multiple"
    elif args.random_mode:
        color_mode = "random"
    elif args.cycle:
        color_mode = "cycle"
    else:
        color_mode = "normal"

    while True:
        try:
            try:
                curses.wrapper(matrix_loop, args.delay, args.bold_on, args.bold_all,
                               args.screen_saver, args.color, args.run_timer,
                               args.lead_color, color_mode)
            except KeyboardInterrupt:
                pass
            if args.use_password:
                exit_pass = get_password()
                if exit_pass == password:
                    break
            else:
                break
        except PyMatrixError as e:
            print(e)
            return

        except KeyboardInterrupt:
            if args.use_password:
                continue
            break


if __name__ == "__main__":
    main()
