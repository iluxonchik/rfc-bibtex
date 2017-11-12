#!/usr/bin/env python3
import sys, re
from urllib import request
import argparse

from exceptions import BadIDNameException, URLFetchException
from utils import print_err_red

# https://sysnetgrp.no-ip.org/rfc/rfcbibtex.php?type=RFC&number=5246
# https://sysnetgrp.no-ip.org/rfc/rfcbibtex.php?type=I-D&number=draft-ietf-tls-tls13-21

class Parser(object):

    @property
    def inline_args(self):
        return self._inline_args

    @property
    def in_file(self):
        return self._in_file

    @property
    def out_file(self):
        return self._out_file

    def build_parser(self):
            """Setup and return the argument parser."""
            parser = argparse.ArgumentParser(description='Generate Bibtex entries for IETF RFCs and Internet-Drafts. Titles are output to preserve the original capitalization.')
            parser.add_argument('inline_args', nargs='*', help='list of RFC and/or Internet-Draft IDs, in any order.', default=[])
            parser.add_argument('-f', '--file', default=None, metavar='FILE_NAME', nargs=1, help='read list of RFC and/or Internet-Draft IDs (one per line) from a file')
            parser.add_argument('-o', '--output', default=None, metavar='FILE_NAME', nargs=1, help='output the resulting bibtex to a file')

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

class RFCBibtex(object):

    URL_FMT = 'https://sysnetgrp.no-ip.org/rfc/rfcbibtex.php?type={}&number={}'
    URL_ERROR_MSG = 'Failed to read RFC or Internt-Draft resource'
    ID_TYPE_RFC = 'RFC'
    ID_TYPE_INTERNET_DRAFT = 'I-D'

    def __init__(self, id_names=[], in_file_name=None, out_file_name=None):
        self._id_names = id_names
        self._out_file_name = out_file_name

        self._id_name_err_list = []
        self._remote_fetch_err_list = [] # (type, name, url)

        if in_file_name is not None:
            self._id_names += self._read_ids_from_file(in_file_name)

    def _read_ids_from_file(self, file_name):
        with open(file_name, 'r') as in_file:
            return [line.strip() for line in in_file ]

    def _generate_bibtex_to_file(self):
        with open(self._out_file_name, 'w') as out_file:
            for id_name in self._id_names:
                try:
                    entry = self.get_bibtex_from_id(id_name)
                    out_file.write(entry)
                    out_file.write('\n')
                except (URLFetchException, BadIDNameException):
                    # error already logged
                    pass

    def _generate_bibtex_to_stdout(self):
        for id_name in self._id_names:
            try:
                entry = self.get_bibtex_from_id(id_name)
                print(entry)
            except (URLFetchException, BadIDNameException):
                # error already logged
                pass

    def _print_errors(self):
        if self._id_name_err_list:
            print_err_red('ERROR in the following ID names (ignored):\n')
            for id_name in self._id_name_err_list:
                print('\t* {}'.format(id_name), file=sys.stderr)

        if self._remote_fetch_err_list:
            print_err_red('ERRORS in fetching from the URLs (ignored):\n')
            for err_tuple in self._remote_fetch_err_list:
                type_name = err_tuple[0] if err_tuple[0] == self.ID_TYPE_RFC else 'Internet-Drafts'
                print('\t* Type:{} | ID:{} | URL:{}'.format(type_name, err_tuple[1], err_tuple[2]), file=sys.stderr)

    def generate_bibtex(self):
        if self._out_file_name is not None:
            self._generate_bibtex_to_file()
        else:
            self._generate_bibtex_to_stdout()

        self._print_errors()

    def _make_title_uppercase(self, response):
        r = re.compile(r'(title = )({.*})')
        res =  r.sub(r'\1{\2}', response)
        return res

    def get_bibtex_from_id(self, id_name):
        url, id_type, id_name = self._get_url_from_id_name(id_name)
        response = self._get_response_from_url(url)
        if response.startswith(self.URL_ERROR_MSG):
            self._remote_fetch_err_list += [(id_type, id_name, url)]
            raise URLFetchException()
        response = self._make_title_uppercase(response)
        return response


    def _get_url_from_id_name(self, id_name):
        id_name = id_name.lower()
        id_type = None # needed for error reporting

        if id_name.startswith('rfc'):
            # we have an RFC
            id_name = id_name[3:]
            id_type = self.ID_TYPE_RFC
        elif id_name.startswith('draft'):
            # we have an Internet Draft
            id_type = self.ID_TYPE_INTERNET_DRAFT
        else:
            # we have an error in an id, but let's not fail the program
            # letting the valid names complete. We'll simply notify the user
            # of the error at the end.
            self._id_name_err_list += [id_name]
            raise BadIDNameException()

        url = self.URL_FMT.format(id_type, id_name)
        return url, id_type, id_name

    def _get_response_from_url(self, url):
        req = request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            }
        )
        with request.urlopen(url) as response:
            return response.read().decode()

if __name__ == '__main__':
    parser = Parser()
    parser.parse_args()

    obj = RFCBibtex(parser.inline_args, parser.in_file, parser.out_file)
    obj.generate_bibtex()
