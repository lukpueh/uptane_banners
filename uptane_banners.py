#!/usr/bin/env python
"""
<Program Name>
  uptane_banners.py

<Author>
  Lukas Puehringer <lukas.puehringer@nyu.edu>

<Started>
  Jan 10, 2017

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Provides functions to read text files (e.g. ascii art) and print them
  horizontally centered to a bash terminal.

"""
import os
import time
from subprocess import Popen, call, PIPE

# Bash font color escape sequences
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

# Bash background color escape sequences
BLACK_BG = "\033[40m"
BLUE_BG = "\033[44m"
WHITE_BG = "\033[107m"
GRAY_BG = "\033[100m"

RESET_COLOR = '\033[0m'

def get_screen_size():
  """Calls bash command `stty size` and returns standard output, i.e.
  width and height of current terminal (blocking call). """
  process = Popen('stty size', shell=True, stdout=PIPE)
  process.wait()
  rows, cols = process.stdout.read().split()
  return int(rows), int(cols)


def clear_screen():
  """Calls bash command `clear`, clears the current temrinal (blocking call). """
  call('clear')


def load_banner(file_path):
  """Loads text from file, appends each line to an array and returns array. """
  banner = open(file_path, 'r').read()
  banner_array = []
  for line in banner.split("\n"):
    banner_array.append(line)
  return banner_array


def print_banner(banner_array, show_for=False, color=False, color_bg=False,
    text=False):
  """
  <Purpose>
    Clears current terminal window and prints passed banner array.
    The passed banner is aligned horizontally.

  <Arguments>
    banner_array:
      Array of string (lines to print)

    show_for: (optional)
      If passed, sleep for given time (in seconds) and then clears the screen.

    color: (optional)
      If passed, fills the banner font. Use one of the constants above.


    color_bg: (optional)
      If passed, fills the banner background. Use one of the constants above.

    text: (optional)
      Text to be displayed below the banner (NOT YET IMPLEMENTED)

  <Exceptions>
    Exception if banner width (longest element of banner_array)

  <Side Effects>
    Clears terminal and prints passed banner to terminal

  <Returns>
    None
  """

  rows, cols = get_screen_size()

  # Get left padding
  banner_width = len(max(banner_array, key=len))

  if banner_width > cols:
    raise Exception("Banner width exceeds terminal width.")
  elif banner_width == cols:
    left_fill = 0
  else:
    left_fill = int((cols - banner_width) / 2)

  clear_screen()

  # Print banner, horizontally left and right padded
  for line in banner_array:
    right_fill = cols - left_fill - len(line)
    # Right and left fill with spaces (for alignment and background color)
    output = (left_fill * " ") + line + (right_fill * " ")

    if color:
      output = color + output

    if color_bg:
      output = color_bg + output

    if color or color_bg:
      output += RESET_COLOR

    print(output)

  if show_for:
    time.sleep(show_for)
    clear_screen()


BANNER_UPDATED = load_banner("ascii/updated.txt")
BANNER_DEFENDED = load_banner("ascii/defended.txt")
BANNER_FROZEN = load_banner("ascii/frozen.txt")
BANNER_HACKED = load_banner("ascii/hacked.txt")
BANNER_COMPROMISED = load_banner("ascii/compromised.txt")
BANNER_REPLAY = load_banner("ascii/replay.txt")

def main():
  print_banner(BANNER_UPDATED, color=GREEN, color_bg=GRAY_BG, show_for=3)
  print_banner(BANNER_DEFENDED, color=YELLOW, color_bg=BLUE_BG, show_for=3)
  print_banner(BANNER_FROZEN, color=YELLOW, color_bg=BLUE_BG, show_for=3)
  print_banner(BANNER_COMPROMISED, color=RED, color_bg=BLACK_BG, show_for=3)
  print_banner(BANNER_HACKED, color=RED, color_bg=BLACK_BG, show_for=3)
  print_banner(BANNER_REPLAY, color=RED, color_bg=BLACK_BG, show_for=3)

if __name__ == "__main__":
  main()