import argparse

class Parser(object):
    """
    A wrapper class around the Python's argparse.parser.
    """
    @property
    def inline_args(self):
        return self._inline_args

    @property
    def in_file(self):
        return self._in_file

    @property
    def out_file(self):
        return self._out_file

    def print_help(self):
        self._parser.print_help()


    def build_parser(self):
            """Setup and return the argument parser."""
            parser = argparse.ArgumentParser(description='Generate Bibtex entries for IETF RFCs and Internet-Drafts. Titles are output to preserve the original capitalization.')
            parser.add_argument('inline_args', nargs='*', help='list of RFC and/or Internet-Draft IDs, in any order.', default=[])
            parser.add_argument('-f', '--file', default=None, metavar='FILE_NAME', nargs=1, help='read list of RFC and/or Internet-Draft IDs (one per line) from a file')
            parser.add_argument('-o', '--output', default=None, metavar='FILE_NAME', nargs=1, help='output the resulting bibtex to a file')
            self._parser = parser

            return parser

    def parse_args(self):
        """ Parse and process command line args """
        parser = self.build_parser()
        args = parser.parse_args()
        # Bind command line args to global vars
        self._inline_args = args.inline_args

        self._in_file = args.file[0] if args.file is not None else None
        self._out_file = args.output[0] if args.output is not None else None

        return self
