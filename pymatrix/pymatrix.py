#! /usr/bin/python3
""" Matrix style rain using Python 3 and curses. """
import argparse
import curses
import datetime
import random
import sys
import time

from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

version = importlib_metadata.version("pymatrix-rain")

CHAR_LIST = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
             "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
             "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
             "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "#", "$",
             "%", "^", "&", "(", ")", "-", "+", "=", "[", "]", "{", "}", "|",
             ";", ":", "<", ">", ",", ".", "?", "~", "`", "@", "*", "_", "'",
             "\\", "/", '"']

EXT_CHAR_LIST = ["Ç", "È", "Ì", "Í", "Ð", "Ñ", "Ò", "×", "Ø", "Ù", "Ú", "Ý",
                 "Þ", "ß", "à", "£", "¤", "¥", "§", "ª", "¶", "º", "»", "¿",
                 "Ä", "Å", "é", "ê", "í", "ï", "å", "æ", "ç", "è", "ð", "ñ",
                 "ò", "ö", "ø", "ù", "ý", "þ", "ā", "ć", "ĉ", "ė", "ě", "ĝ",
                 "ģ", "ħ", "ī", "ı", "ķ", "Ľ", "Ł", "ł", "ń", "ň", "ō", "Œ",
                 "œ", "ŕ", "ŗ", "ś", "ŝ", "š", "ť", "ū", "ų", "Ÿ", "ź", "ż",
                 "Ž", "ž", "ș", "ț", "ë", "Ĉ", "Ď", "ď", "Ġ", "Ř", "°", "«",
                 "±", "Δ", "Ξ", "Λ", ]

KATAKANA_CHAR_LIST = ["ｦ", "ｱ", "ｳ", "ｴ", "ｵ", "ｶ", "ｷ", "ｹ", "ｺ", "ｻ", "ｼ",
                      "ｽ", "ｾ", "ｿ", "ﾀ", "ﾂ", "ﾃ", "ﾅ", "ﾆ", "ﾇ", "ﾈ", "ﾊ",
                      "ﾋ", "ﾎ", "ﾏ", "ﾐ", "ﾑ", "ﾒ", "ﾓ", "ﾔ", "ﾕ", "ﾗ", "ﾘ",
                      "ﾜ", "ﾍ", "ｲ", "ｸ", "ﾁ", "ﾄ", "ﾉ", "ﾌ", "ﾖ", "ﾙ", "ﾚ",
                      "ﾛ", "ﾝ"]

KATAKANA_CHAR_LIST_ADDON = ["0", "1", "2", "3", "4", "5", "7", "8", "9", "Z",
                            ":", ".", "=", "*", "+", "-", "<", ">"]


DELAY_SPEED = {0: 0.005, 1: 0.01, 2: 0.025, 3: 0.04, 4: 0.055, 5: 0.07,
               6: 0.085, 7: 0.1, 8: 0.115, 9: 0.13}

CURSES_CH_CODES_CYCLE_DELAY = {41: 1, 33: 2, 64: 3, 35: 4, 36: 5, 37: 6,
                               94: 7, 38: 8, 42: 9, 40: 10}

CURSES_COLOR = {"red": curses.COLOR_RED, "green": curses.COLOR_GREEN,
                "blue": curses.COLOR_BLUE, "yellow": curses.COLOR_YELLOW,
                "magenta": curses.COLOR_MAGENTA, "cyan": curses.COLOR_CYAN,
                "white": curses.COLOR_WHITE, "black": curses.COLOR_BLACK}

CURSES_OVER_RIDE_COLORS = {"red": 160, "green": 40, "blue": 21,
                           "yellow": 184, "magenta": 164, "cyan": 44,
                           "white": 255, "black": 16}

CURSES_CH_CODES_COLOR = {114: "red", 82: "red", 116: "green", 84: "green",
                         121: "blue", 89: "blue", 117: "yellow", 85: "yellow",
                         105: "magenta", 73: "magenta", 111: "cyan",
                         79: "cyan", 112: "white", 80: "white", 18: "red",
                         20: "green", 25: "blue", 21: "yellow", 9: "magenta",
                         15: "cyan", 16: "white", 27: "black", 91: "black",
                         123: "black"}
WAKE_UP_PAIR = 21
MIN_SCREEN_SIZE_Y = 10
MIN_SCREEN_SIZE_X = 10


class PyMatrixError(Exception):
    pass


class SingleLine:
    def __init__(self, y: int, x: int, width: int, height: int, direction: str):
        self.direction = direction
        self.height = height - 2
        self.width = width - 1
        self.async_scroll_count = 0
        self.async_scroll_rate = random.randint(0, 4)
        self.line_color_number = random.randint(1, 7)  # keep for now
        if direction == "down":
            self.lead_y = 0
            self.y = -1
            self.x = x
            length = random.randint(3, height - 3)
            self.last_y = -length  # track when to start removing characters
        elif direction == "up":
            self.lead_y = height - 2
            self.y = height - 1
            self.x = x
            length = random.randint(3, height - 3)
            self.last_y = height - 3 + length
        elif direction == "right":
            self.lead_x = 0
            self.x = -1
            length = random.randint(3, width - 3)
            self.last_x = -length
            self.y = y
            self.lead_y = 0
            self.last_y = 0
        elif direction == "left":
            self.lead_x = width - 2
            self.x = width - 1
            length = random.randint(3, width - 3)
            self.last_x = width - 2 + length
            self.y = y
            self.lead_y = 0
            self.last_y = 0

    def get_lead(self) -> Union[Tuple[int, int], None]:
        if self.direction == "down":
            if self.lead_y > self.height:
                return None
            else:
                lead_y = self.lead_y
                self.lead_y += 1
                return lead_y, self.x
        elif self.direction == "up":
            if self.lead_y < 0:
                return None
            else:
                lead_y = self.lead_y
                self.lead_y -= 1
                return lead_y, self.x
        elif self.direction == "right":
            if self.lead_x >= self.width:
                return None
            else:
                lead_x = self.lead_x
                self.lead_x += 1
                return self.y, lead_x
        elif self.direction == "left":
            if self.lead_x < 0:
                return None
            else:
                lead_x = self.lead_x
                self.lead_x -= 1
                return self.y, lead_x

    def get_next(self) -> Union[Tuple[int, int], None]:
        if self.direction == "down":
            if self.y < 0 or self.y > self.height:
                self.y += 1
                return None
            else:
                y = self.y
                self.y += 1
                return y, self.x
        elif self.direction == "up":
            if self.y > self.height or self.y < 0:
                self.y -= 1
                return None
            else:
                y = self.y
                self.y -= 1
                return y, self.x
        elif self.direction == "right":
            if self.x < 0 or self.x >= self.width:
                self.x += 1
                return None
            x = self.x
            self.x += 1
            return self.y, x
        elif self.direction == "left":
            if self.x >= self.width or self.x < 0:
                self.x -= 1
                return None
            x = self.x
            self.x -= 1
            return self.y, x

    def delete_last(self) -> Union[Tuple[int, int], None]:
        if self.direction == "down":
            if self.last_y < 0 or self.last_y > self.height:
                self.last_y += 1
                return None
            else:
                last_y = self.last_y
                self.last_y += 1
                return last_y, self.x
        elif self.direction == "up":
            if self.last_y > self.height or self.last_y < 0:
                self.last_y -= 1
                return None
            else:
                last_y = self.last_y
                self.last_y -= 1
                return last_y, self.x
        elif self.direction == "right":
            if self.last_x < 0 or self.last_x >= self.width:
                self.last_x += 1
                return None
            else:
                last_x = self.last_x
                self.last_x += 1
                return self.y, last_x
        elif self.direction == "left":
            if self.last_x >= self.width:
                self.last_x -= 1
                return None
            else:
                last_x = self.last_x
                self.last_x -= 1
                return self.y, last_x

    def okay_to_delete(self) -> bool:
        if self.direction == "down":
            if self.last_y > self.height:
                return True
            else:
                return False
        elif self.direction == "up":
            if self.last_y < 0:
                return True
            else:
                return False
        elif self.direction == "right":
            if self.last_x >= self.width:
                return True
            else:
                return False
        elif self.direction == "left":
            if self.last_x < 0:
                return True
            else:
                return False

    def async_scroll_turn(self) -> bool:
        if self.async_scroll_count == self.async_scroll_rate:
            self.async_scroll_count = 0
            return True
        else:
            self.async_scroll_count += 1
            return False


class OldScrollingLine:
    old_scroll_chr_list = []

    def __init__(self, x: int, width: int, height: int):
        self.height = height - 2
        self.width = width - 1
        self.y = -1
        self.x = x
        self.length = random.randint(3, height - 3)
        self.lead_y = 0
        self.lead_char = random.choice(OldScrollingLine.old_scroll_chr_list)
        self.location_list = []
        self.line_color_number = random.randint(1, 7)
        self.bold = True if random.randint(1, 3) <= 1 else False

    @classmethod
    def update_char_list(cls, updated_char_list: List[str]) -> None:
        OldScrollingLine.old_scroll_chr_list = updated_char_list

    def delete_last(self) -> Union[None, List[int]]:
        if len(self.location_list) == self.length or self.y >= self.length:
            return self.location_list[-1][0:2]
        else:
            return None

    def get_lead(self) -> Union[Tuple[int, int, str], None]:
        if self.lead_y <= self.height:
            lead_y = self.lead_y
            self.lead_y += 1
            return lead_y, self.x, self.lead_char
        else:
            return None

    def get_next(self) -> List[List]:
        if len(self.location_list) != 0 and self.y >= 0:
            for cell in self.location_list:
                cell[0] += 1
        if len(self.location_list) < self.length and 0 <= self.y < self.height:
            self.location_list.append(
                [0, self.x, random.choice(OldScrollingLine.old_scroll_chr_list)]
            )
        if self.y > self.height:
            self.location_list.pop(0)
        self.y += 1
        return self.location_list

    def okay_to_delete(self) -> bool:
        if len(self.location_list) == 0 and self.y > self.height:
            return True
        else:
            return False


def build_character_set2(args: argparse.Namespace):
    if args.zero_one:
        new_list = ["0", "1"]
    elif args.ext_only:
        if args.test_mode:
            new_list = ["Ä"]
        else:
            new_list = EXT_CHAR_LIST
    elif args.Katakana_only:
        if args.test_mode:
            new_list = ["ﾎ", "0"]
        else:
            new_list = KATAKANA_CHAR_LIST + KATAKANA_CHAR_LIST_ADDON
    elif args.katakana and args.ext:
        if args.test_mode:
            new_list = ["T", "ﾎ", "Ä"]
        else:
            new_list = KATAKANA_CHAR_LIST + EXT_CHAR_LIST + CHAR_LIST
    elif args.ext:
        if args.test_mode:
            new_list = ["Ä", "T"]
        else:
            new_list = CHAR_LIST + EXT_CHAR_LIST
    elif args.katakana:
        if args.test_mode:
            new_list = ["T", "ﾎ"]
        else:
            new_list = CHAR_LIST + KATAKANA_CHAR_LIST
    else:
        if args.test_mode:
            new_list = ["T"]
        else:
            new_list = CHAR_LIST
    OldScrollingLine.update_char_list(new_list)
    return new_list


def matrix_loop(screen, args: argparse.Namespace) -> None:
    """ Main loop. """
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    setup_curses_wake_up_colors(args.over_ride)
    if args.color_number is not None:
        setup_curses_color_number(args.color_number, args.background,
                                  args.over_ride)
    else:
        setup_curses_colors(args.color, args.background, args.over_ride)
    curses_lead_color(args.lead_color, args.background, args.over_ride)
    screen.bkgd(" ", curses.color_pair(1))
    count = cycle = 0  # used for cycle through colors mode
    cycle_delay = 500
    line_list = []
    spacer = 2 if args.double_space else 1
    keys_pressed = 0
    if args.reverse:
        direction = "up"
    elif args.scroll_right:
        direction = "right"
    elif args.scroll_left:
        direction = "left"
    elif args.old_school_scrolling:
        direction = "old scrolling"
    else:
        direction = "down"

    char_set = build_character_set2(args)

    wake_up_time = 20 if args.test_mode else random.randint(2000, 3000)

    if args.multiple_mode:
        color_mode = "multiple"
        setup_curses_colors("random", args.background, args.over_ride)
    elif args.random_mode:
        color_mode = "random"
        setup_curses_colors("random", args.background, args.over_ride)
    elif args.cycle:
        color_mode = "cycle"
    else:
        color_mode = "normal"

    size_y, size_x = screen.getmaxyx()
    if size_y < MIN_SCREEN_SIZE_Y:
        raise PyMatrixError("Error screen height is to short.")
    if size_x < MIN_SCREEN_SIZE_X:
        raise PyMatrixError("Error screen width is to narrow.")
    x_list = [x for x in range(0, size_x, spacer)]
    y_list = [y for y in range(1, size_y)]

    time_delta = datetime.timedelta(seconds=args.run_timer)
    end_time = datetime.datetime.now() + time_delta
    while True:
        remove_list = []
        if direction == "right" or direction == "left":
            y = random.choice(y_list)
            line_list.append(SingleLine(y, 0, size_x, size_y, direction))
        else:
            if len(line_list) < size_x - 1 and len(x_list) > 3:
                for _ in range(2):
                    x = random.choice(x_list)
                    x_list.pop(x_list.index(x))
                    if direction == "old scrolling":
                        line_list.append(OldScrollingLine(x, size_x, size_y))
                    else:
                        line_list.append(
                            SingleLine(0, x, size_x, size_y, direction))

        resize = curses.is_term_resized(size_y, size_x)
        if resize is True:
            size_y, size_x = screen.getmaxyx()
            if size_y < MIN_SCREEN_SIZE_Y:
                raise PyMatrixError("Error screen height is to short.")
            if size_x < MIN_SCREEN_SIZE_X:
                raise PyMatrixError("Error screen width is to narrow.")
            x_list = [x for x in range(0, size_x, spacer)]
            y_list = [y for y in range(0, size_y)]

            line_list.clear()
            screen.clear()
            screen.refresh()
            continue

        if color_mode == "cycle":
            if count <= 0:
                setup_curses_colors(list(CURSES_COLOR.keys())[cycle],
                                    args.background, args.over_ride)
                count = cycle_delay
                cycle = 0 if cycle == 6 else cycle + 1
            else:
                count -= 1
        if direction == "old scrolling":
            for line in line_list:
                if args.bold_all:
                    bold = curses.A_BOLD
                elif args.bold_on and line.bold:
                    bold = curses.A_BOLD
                else:
                    bold = curses.A_NORMAL

                italic = curses.A_ITALIC if args.italic else curses.A_NORMAL

                color = curses.color_pair(line.line_color_number)
                remove = line.delete_last()
                lead = line.get_lead()
                if lead is not None:
                    screen.addstr(lead[0], lead[1], lead[2],
                                  curses.color_pair(10) + bold + italic)
                if remove is not None:
                    screen.addstr(remove[0], remove[1], " ")
                    if line.x not in x_list:
                        x_list.append(line.x)
                location_char_list = line.get_next()
                for cell in location_char_list:
                    screen.addstr(*cell, color + bold + italic)
                okay_to_delete = line.okay_to_delete()
                if okay_to_delete:
                    remove_list.append(line)
        else:
            for line in line_list:
                if args.async_scroll and not line.async_scroll_turn():
                    # Not the line's turn in async scroll mode then
                    # continue to the next line.
                    continue
                remove_line = line.delete_last()
                if remove_line is not None:
                    if args.do_not_clear is False:
                        screen.addstr(remove_line[0], remove_line[1], " ")
                    if line.x not in x_list:
                        x_list.append(line.x)

                if args.bold_all:
                    bold = curses.A_BOLD
                elif args.bold_on:
                    if random.randint(1, 3) <= 1:
                        bold = curses.A_BOLD
                    else:
                        bold = curses.A_NORMAL
                else:
                    bold = curses.A_NORMAL

                italic = curses.A_ITALIC if args.italic else curses.A_NORMAL

                if color_mode == "random":
                    color = curses.color_pair(random.randint(1, 7))
                else:
                    color = curses.color_pair(line.line_color_number)
                new_char = line.get_next()
                if new_char is not None:
                    screen.addstr(new_char[0],
                                  new_char[1],
                                  random.choice(char_set),
                                  color + bold + italic)
                lead_char = line.get_lead()
                if lead_char is not None:
                    screen.addstr(lead_char[0], lead_char[1],
                                  random.choice(char_set),
                                  curses.color_pair(10) + bold + italic)
                if line.okay_to_delete():
                    remove_list.append(line)
            screen.refresh()

        for rem in remove_list:
            line_list.pop(line_list.index(rem))

        if args.wakeup:
            if wake_up_time <= 0:
                wake_up_neo(screen, args.test_mode)
                wake_up_time = random.randint(2000, 3000)
                while screen.getch() != -1:  # clears out the buffer
                    ...
                screen.bkgd(" ", curses.color_pair(1))
                continue
            else:
                wake_up_time -= 1

        if args.run_timer and datetime.datetime.now() >= end_time:
            break
        time.sleep(DELAY_SPEED[args.delay])
        ch = screen.getch()
        if ch == -1:
            continue
        elif args.screen_saver:
            break
        elif ch in [81, 113]:  # q, Q
            break
        elif args.disable_keys:
            continue
        # Commands:
        elif ch == 119 and keys_pressed == 0:  # w
            keys_pressed = 1
        elif ch == 65 and keys_pressed == 1:  # A
            keys_pressed = 2
        elif ch == 107 and keys_pressed == 2:  # k
            keys_pressed = 3
            continue
        elif ch == 101 and keys_pressed == 3:  # e
            wake_up_neo(screen, args.test_mode)
            while screen.getch() != -1:  # clears out the buffer
                pass
            keys_pressed = 0
            screen.bkgd(" ", curses.color_pair(1))
            continue
        else:
            keys_pressed = 0
        if ch == 98:  # b
            args.bold_on = True
            args.bold_all = False
        elif ch == 66:  # B
            args.bold_all = True
            args.bold_on = False
        elif ch in [78, 110]:  # n or N
            args.bold_on = False
            args.bold_all = False
        elif ch in [114, 116, 121, 117, 105, 111, 112, 91]:
            # r, t, y, u, i, o, p, [
            args.color = CURSES_CH_CODES_COLOR[ch]
            setup_curses_colors(args.color, args.background, args.over_ride)
            color_mode = "normal"
        elif ch in [82, 84, 89, 85, 73, 79, 80, 123]:
            # R, T, Y, U, I, O, P, {
            args.lead_color = CURSES_CH_CODES_COLOR[ch]
            curses_lead_color(args.lead_color, args.background, args.over_ride)
        elif ch in [18, 20, 25, 21, 9, 15, 16, 27]:
            # ctrl R, T, Y, U, I, O, P, [
            args.background = CURSES_CH_CODES_COLOR[ch]
            setup_curses_colors(args.color, args.background, args.over_ride)
            curses_lead_color(args.lead_color, args.background, args.over_ride)
            screen.bkgd(" ", curses.color_pair(1))
        elif ch == 97:  # a
            args.async_scroll = not args.async_scroll
        elif ch == 109:  # m
            if color_mode in ["random", "normal", "cycle"]:
                color_mode = "multiple"
                setup_curses_colors("random", args.background, args.over_ride)
            else:
                color_mode = "normal"
                setup_curses_colors("green", args.background, args.over_ride)
        elif ch == 77:  # M
            if color_mode in ["multiple", "normal", "cycle"]:
                color_mode = "random"
                setup_curses_colors("random", args.background, args.over_ride)
            else:
                color_mode = "normal"
                setup_curses_colors("green", args.background, args.over_ride)
        elif ch == 99:  # c
            if color_mode in ["random", "multiple", "normal"]:
                color_mode = "cycle"
            else:
                color_mode = "normal"
        elif ch == 108:  # l
            if direction == "right" or direction == "left":
                continue
            if spacer == 1:
                spacer = 2
                x_list = [x for x in range(0, size_x, spacer)]
                line_list.clear()
                screen.clear()
                screen.refresh()
            else:
                spacer = 1
                x_list = [x for x in range(0, size_x, spacer)]
        elif ch == 101:  # e
            args.zero_one = False
            if args.ext or args.ext_only:
                args.ext = False
            else:
                args.ext = True
            char_set = build_character_set2(args)
        elif ch == 69:  # E
            args.zero_one = False
            args.ext_only = not args.ext_only
            char_set = build_character_set2(args)
        elif ch == 122 and not args.zero_one:  # z
            args.zero_one = True
            char_set = build_character_set2(args)
        elif ch == 90 and args.zero_one:  # Z
            args.zero_one = False
            char_set = build_character_set2(args)
        elif ch == 23:  # ctrl-w
            args.wakeup = not args.wakeup
        elif ch == 118:  # v
            args.reverse = not args.reverse
            x_list = [x for x in range(0, size_x, spacer)]
            args.scroll_right = False
            if direction == "down":
                direction = "up"
            elif direction == "up":
                direction = "down"
            else:
                direction = "up"
            line_list.clear()
            screen.clear()
            screen.refresh()
        elif ch == 115:  # s
            args.old_school_scrolling = not args.old_school_scrolling
            if direction == "old scrolling":
                direction = "down"
            else:
                direction = "old scrolling"
            args.scroll_left = False
            args.scroll_right = False
            x_list = [x for x in range(0, size_x, spacer)]
            screen.clear()
            screen.refresh()
            line_list.clear()
            time.sleep(0.2)

        elif ch == 261:  # right arrow
            if not args.scroll_right:
                args.scroll_right = True
                args.scroll_left = False
                args.reverse = False
                args.old_school_scrolling = False
                direction = "right"
                line_list.clear()
                screen.clear()
                screen.refresh()
                time.sleep(0.4)
                y_list = [y for y in range(1, size_y)]
        elif ch == 260:  # left arrow
            if not args.scroll_left:
                args.scroll_left = True
                args.scroll_right = False
                args.reverse = False
                args.old_school_scrolling = False
                direction = "left"
                line_list.clear()
                screen.clear()
                screen.refresh()
                time.sleep(0.4)
                y_list = [y for y in range(1, size_y)]
        elif ch == 259:  # up arrow
            if not args.reverse:
                args.reverse = True
                args.scroll_right = False
                args.old_school_scrolling = False
                direction = "up"
                line_list.clear()
                screen.clear()
                screen.refresh()
                time.sleep(0.4)
                x_list = [x for x in range(0, size_x, spacer)]
        elif ch == 258:  # down arrow
            if direction != "down":
                args.reverse = False
                args.scroll_right = False
                args.old_school_scrolling = False
                direction = "down"
                line_list.clear()
                screen.clear()
                screen.refresh()
                time.sleep(0.3)
                x_list = [x for x in range(0, size_x, spacer)]
        elif ch in [100, 68]:  # d, D
            args.zero_one = False
            args.bold_on = False
            args.bold_all = False
            args.background = "black"
            args.color = "green"
            args.lead_color = "white"
            args.ext = False
            args.ext_only = False
            setup_curses_colors(args.color, args.background, args.over_ride)
            curses_lead_color(args.lead_color, args.background, args.over_ride)
            color_mode = "normal"
            args.async_scroll = False
            args.delay = 4
            args.Katakana_only = False
            args.katakana = False
            if direction == "old scrolling":
                args.old_school_scrolling = False
                x_list = [x for x in range(0, size_x, spacer)]
                screen.clear()
                screen.refresh()
                line_list.clear()
                time.sleep(0.2)
            if direction == "right" or direction == "left":
                args.scroll_right = False
                args.scroll_left = False
                x_list = [x for x in range(0, size_x, spacer)]
                screen.clear()
                screen.refresh()
                line_list.clear()
                time.sleep(0.2)
            direction = "down"
            args.do_not_clear = False
            args.italic = False
            if spacer == 2:
                spacer = 1
                x_list = [x for x in range(0, size_x, spacer)]
            if args.reverse:
                args.reverse = False
                line_list.clear()
                screen.clear()
                screen.refresh()
            char_set = build_character_set2(args)
        elif color_mode == "cycle" and ch in CURSES_CH_CODES_CYCLE_DELAY.keys():
            cycle_delay = 100 * CURSES_CH_CODES_CYCLE_DELAY[ch]
            count = cycle_delay
        elif 48 <= ch <= 57:  # number keys 0 to 9
            args.delay = int(chr(ch))
        elif ch == 87:  # W
            args.do_not_clear = not args.do_not_clear
        elif ch == 119:  # w
            screen.clear()
            screen.refresh()
            line_list.clear()
            time.sleep(2)
            continue
        elif ch == 106:  # j
            args.italic = not args.italic
        elif ch == 102:  # f
            # Freeze the Matrix
            quit_matrix = False
            while True:
                ch = screen.getch()
                if ch == 102:
                    break
                elif ch in [81, 113]:  # q, Q
                    quit_matrix = True
                    break
            if quit_matrix:
                break
        elif ch == 75:  # K
            args.zero_one = False
            args.Katakana_only = not args.Katakana_only
            char_set = build_character_set2(args)
        elif ch == 107:  # k
            args.zero_one = False
            args.Katakana_only = False
            args.katakana = not args.katakana
            char_set = build_character_set2(args)

    screen.erase()
    screen.refresh()


def curses_lead_color(color: str, bg_color: str, over_ride: bool) -> None:
    if over_ride:
        curses.init_pair(10, CURSES_OVER_RIDE_COLORS[color],
                         CURSES_OVER_RIDE_COLORS[bg_color])
    else:
        curses.init_pair(10, CURSES_COLOR[color], CURSES_COLOR[bg_color])


def setup_curses_color_number(
        color_num: int,
        bg_color: str,
        override: bool) -> None:

    if override:
        bg = CURSES_OVER_RIDE_COLORS[bg_color]
    else:
        bg = CURSES_COLOR[bg_color]

    color_list = [color_num for _ in range(7)]
    for x, c in enumerate(color_list):
        curses.init_pair(x + 1, c, bg)


def setup_curses_colors(color: str, bg_color: str, over_ride: bool) -> None:
    """ Init colors pairs in the curses. """
    if over_ride:
        if color == "random":
            color_list = list(CURSES_OVER_RIDE_COLORS.keys())
        else:
            color_list = [color for _ in range(7)]

        for x, c in enumerate(color_list):
            curses.init_pair(x + 1, CURSES_OVER_RIDE_COLORS[c],
                             CURSES_OVER_RIDE_COLORS[bg_color])
    else:
        if color == "random":
            color_list = list(CURSES_COLOR.keys())
        else:
            color_list = [color for _ in range(7)]

        for x, c in enumerate(color_list):
            curses.init_pair(x + 1, CURSES_COLOR[c], CURSES_COLOR[bg_color])


def setup_curses_wake_up_colors(override: bool) -> None:
    if override:
        curses.init_pair(WAKE_UP_PAIR,
                         CURSES_OVER_RIDE_COLORS["green"],
                         CURSES_OVER_RIDE_COLORS["black"])
    else:
        curses.init_pair(WAKE_UP_PAIR,
                         CURSES_COLOR["green"],
                         CURSES_COLOR["black"])


def wake_up_neo(screen, test_mode: bool) -> None:
    z = 0.06 if test_mode else 1  # For test mode - shorter test time
    screen.erase()
    screen.bkgd(" ", curses.color_pair(WAKE_UP_PAIR))
    screen.refresh()
    time.sleep(3 * z)
    display_text(screen, "Wake up, Neo...", 0.08 * z, 7.0 * z)
    display_text(screen, "The Matrix has you...", 0.25 * z, 7.0 * z)
    display_text(screen, "Follow the white rabbit.", 0.1 * z, 7.0 * z)
    display_text(screen, "Knock, knock, Neo.", 0.01 * z, 3.0 * z)
    time.sleep(2 * z)


def display_text(screen, text: str, type_time: float, hold_time: float) -> None:
    for i, letter in enumerate(text, start=1):
        screen.addstr(1, i, letter,
                      curses.color_pair(WAKE_UP_PAIR) + curses.A_BOLD)
        screen.refresh()
        time.sleep(type_time)
    time.sleep(hold_time)
    screen.erase()
    screen.refresh()


def positive_int_zero_to_nine(value: str) -> int:
    """
    Used with argparse.
    Checks to see if value is positive int between 0 and 10.
    """
    msg = f"{value} is an invalid positive int value 0 to 9"
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= 10:
            raise argparse.ArgumentTypeError(msg)
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(msg)


def color_type(value: str) -> str:
    """
    Used with argparse
    Checks to see if the value is a valid color and returns
    the lower case color name.
    """
    lower_value = value.lower()
    if lower_value in CURSES_COLOR.keys():
        return lower_value
    raise argparse.ArgumentTypeError(f"{value} is an invalid color name")


def positive_int(value: str) -> int:
    """
    Used by argparse.
    Checks to see if the value is positive.
    """
    msg = f"{value} is an invalid positive int value"
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(msg)
    else:
        if int_value <= 0:
            raise argparse.ArgumentTypeError(msg)
    return int_value


def int_between_1_and_255(value: str) -> int:
    """
    Used by argparse. Checks to see if the value is between 1 and 255
    """
    msg = f"{value} is an invalid positive int between 1 and 255"
    try:
        int_value = int(value)
        if int_value < 1 or int_value > 255:
            raise argparse.ArgumentTypeError(msg)
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(msg)


def display_commands() -> None:
    print("Commands available during run")
    print("0 - 9  Delay time (0-Fast, 4-Default, 9-Slow)")
    print("q or Q To quit Pymatrix-rain")
    print("b      Bold characters on")
    print("B      Bold all characters")
    print("n      Bold off (Default)")
    print("a      Asynchronous like scrolling (normal scrolling only)")
    print("m      Multiple color mode")
    print("M      Multiple random color mode (normal scrolling only")
    print("c      Cycle colors")
    print("d      Restore all defaults")
    print("l      Toggle double space lines")
    print("e      Extended characters on and off")
    print("E      Extended characters only")
    print("k      Katakana characters like those from the movies if correct font is installed")
    print("K      Katakana characters only")
    print("z      1 and 0 Mode On")
    print("Z      1 and 0 Mode Off")
    print("f      Freeze the matrix (q will still quit")
    print("v      Toggle matrix scrolling up")
    print("W      Toggle do not clear screen (normal scrolling only)")
    print("w      Clear the screen, wait 2 seconds and restart")
    print("j      Toggle italic text")
    print("s      Toggle old school scrolling down only")
    print("up arrow    Matrix scrolls down to up")
    print("down arrow  Matrix scrolls up to down (default)")
    print("right arrow Matrix scrolls from left to right")
    print("left arrow  Matrix scrolls from right to left")
    print("r,t,y,u,i,o,p,[   Set color")
    print("R,T,Y,U,I,O,P,{   Set lead character color")
    print("ctrl + r,t,y,u,i,o,p,[  Set background color")
    print("shift 0 - 9 Cycle color delay (0-Fast, 4-Default, 9-Slow)")


def argument_parsing(
        argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """ Command line argument parsing. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="delay",
                        type=positive_int_zero_to_nine,
                        default=4,
                        help="Set the delay (speed)"
                             " 0: Fast, 4: Default, 9: Slow")
    parser.add_argument("-b", dest="bold_on", action="store_true",
                        help="Bold characters on")
    parser.add_argument("-B", dest="bold_all", action="store_true",
                        help="All bold characters (overrides -b)")
    parser.add_argument("-s", dest="screen_saver", action="store_true",
                        help="Screen saver mode.  Any key will exit.")
    parser.add_argument("-a", dest="async_scroll", action="store_true",
                        help="enable asynchronous like scrolling "
                             "(normal scrolling only)")
    parser.add_argument("-S", dest="start_timer", type=positive_int, default=0,
                        metavar="SECONDS", help="Set start timer in seconds")
    parser.add_argument("-R", dest="run_timer", type=positive_int, default=0,
                        metavar="SECONDS", help="Set run timer in seconds")
    parser.add_argument("-C", dest="color", type=color_type, default="green",
                        help="Set color.  Default is green")
    parser.add_argument("-L", dest="lead_color",
                        type=color_type, default="white",
                        help="Set the lead character color.  Default is white")
    parser.add_argument("-m", dest="multiple_mode", action="store_true",
                        help="Multiple color mode")
    parser.add_argument("-M", dest="random_mode", action="store_true",
                        help="Multiple random color mode "
                             "(normal scrolling only")
    parser.add_argument("-c", dest="cycle", action="store_true",
                        help="cycle through the colors")
    parser.add_argument("-e", dest="ext", action="store_true",
                        help="use extended characters")
    parser.add_argument("-E", dest="ext_only", action="store_true",
                        help="use only extended characters (overrides -e)")
    parser.add_argument("-l", dest="double_space", action="store_true",
                        help="Double space lines")
    parser.add_argument("-z", dest="zero_one", action="store_true",
                        help="Show only zero and ones. Binary")
    parser.add_argument("--background", type=color_type, default="black",
                        help="set background color. Default is black.")
    parser.add_argument("-v", "--reverse", action="store_true",
                        help="Reverse the matrix. "
                             "The matrix scrolls up (vertical)")
    parser.add_argument("--scroll_right", action="store_true",
                        help="Matrix scrolls from left to right")
    parser.add_argument("--scroll_left", action="store_true",
                        help="Matrix scrolls from right to left")
    parser.add_argument("-o", "--old_school_scrolling", action="store_true",
                        help="Old school scrolling. Scroll down only")
    parser.add_argument("-j", "--italic", action="store_true",
                        help="Italic characters")
    parser.add_argument("-k", "--katakana", action="store_true",
                        help="Use half width Katakana (as seen in the movie) "
                             "characters. NOTE: requires the correct"
                             " font to be installed to work")
    parser.add_argument("-K", "--Katakana_only", action="store_true",
                        help="Use only half width Katakana (as seen "
                             "in the movie) characters only. NOTE: requires"
                             " the correct font to be installed to work")
    parser.add_argument("-O", dest="over_ride", action="store_true",
                        help="Override terminal window colors by using color"
                             " numbers between 16 and 255. This requires 256"
                             " color support in the terminal to work.")
    parser.add_argument("-W", "--do_not_clear", action="store_true",
                        help="do not clear the screen (Normal scrolling only)")
    parser.add_argument("--color_number", type=int_between_1_and_255,
                        default=None,
                        metavar="number",
                        help="Enter a number between 1 and 255 to select"
                             " character color. Requires 256 color support in "
                             "the terminal to work. Changing colors or "
                             "background color will remove the color entered.")
    parser.add_argument("--disable_keys", action="store_true",
                        help="Disable keys except for Q to quit. Screensaver "
                             "mode will not be affected")
    parser.add_argument("--list_colors", action="store_true",
                        help="Show available colors and exit. ")
    parser.add_argument("--list_commands", action="store_true",
                        help="List Commands and exit")
    parser.add_argument("--version", action="version",
                        version=f"Version: {version}")

    parser.add_argument("--wakeup", action="store_true",
                        help=argparse.SUPPRESS)
    parser.add_argument("--test_mode", action="store_true",
                        help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = argument_parsing(argv)

    if args.list_colors:
        print(*CURSES_COLOR.keys())
        return
    if args.list_commands:
        display_commands()
        return

    time.sleep(args.start_timer)
    try:
        curses.wrapper(matrix_loop, args)
    except KeyboardInterrupt:
        pass
    except PyMatrixError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
