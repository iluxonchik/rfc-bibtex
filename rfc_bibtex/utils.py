import sys

RED   = "\033[1;31m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"

def print_err_red(text):
    sys.stderr.write(BOLD + RED)
    sys.stderr.write(text)
    sys.stderr.write(RESET)
