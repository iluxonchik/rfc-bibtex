import sys

RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

def print_err_red(text):
    sys.stderr.write(BOLD + RED)
    sys.stderr.write(text)
    sys.stderr.write(RESET)
