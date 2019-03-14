import sys

def print_red(text, end='\n', file=sys.stdout):
    print(f'\u001b[1m\u001b[31m{text}\u001b[0m', end=end)

def print_green(text, end='\n', file=sys.stdout):
    print(f'\u001b[1m\u001b[32m{text}\u001b[0m', end=end)

def print_yellow(text, end='\n', file=sys.stdout):
    print(f'\u001b[33m\u001b[33m{text}\u001b[0m', end=end)

def print_magenta(text, end='\n', file=sys.stdout):
    print(f'\u001b[35m\u001b[31m{text}\u001b[0m', end=end)