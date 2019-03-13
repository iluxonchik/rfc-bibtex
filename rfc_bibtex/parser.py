import argparse

class Parser(object):
    """
    A wrapper class around the Python's argparse.parser.
    """
    @property
    def inline_args(self):
        return self._inline_args

    @property
    def in_files(self):
        return self._in_file

    @property
    def out_file(self):
        return self._out_file

    def print_help(self):
        self._parser.print_help()


    def build_parser(self):
            """Setup and return the argument parser."""
            parser = argparse.ArgumentParser(description='Generate BibTex entries for IETF RFCs and Internet Drafts. The list of IDs can be read from a file '
                                                         '(including .tex and .aux) or directly from command-line arguments.')
            parser.add_argument('inline_args', nargs='*', help='list of RFC and/or Internet Draft IDs, in any order.', default=[])
            parser.add_argument('-f', '--files', default=[], metavar='FILE_NAMES', nargs='+', help='read list of RFC and/or Internet Draft IDs from a file. ' 
                                'Supported file formats are the following: .tex, .aux and .txt (one ID per line). '
                                'If a file with any other extension is provided, the tool attempts to read it as a .txt file, '
                                'containing one ID per line.')
            parser.add_argument('-o', '--output', default=None, metavar='FILE_NAME', nargs=1, help='output the resulting BibTex to a file')
            self._parser = parser

            return parser

    def parse_args(self):
        """ Parse and process command line args """
        parser = self.build_parser()
        args = parser.parse_args()
        # Bind command line args to global vars
        self._inline_args = args.inline_args

        self._in_file = args.files
        self._out_file = args.output[0] if args.output is not None else None

        return self
