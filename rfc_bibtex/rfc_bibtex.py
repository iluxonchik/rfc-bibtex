#!/usr/bin/env python3
import sys, re
import pathlib
import os, os.path
from urllib import request
import random

from .exceptions import BadIDNameException, URLFetchException, BadRFCNumberException
from .utils import print_err_red
from .parser import Parser

class RFCBibtex(object):

    # Old server; a backup
    #URL_FMT      = 'https://sysnetgrp.no-ip.org/rfc/rfcbibtex.php?type={id_type}&number={id_name}'
    URL_FMT       = 'https://datatracker.ietf.org/doc/{id_name}/bibtex/'
    URL_ERROR_MSG = 'Failed to read RFC or Internt-Draft resource'
    ID_TYPE_RFC   = 'RFC'
    ID_TYPE_INTERNET_DRAFT = 'I-D'

    # This client uses multiple user agents to fake out attempts to prevent webscraping. 
    USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36']

    # If scanning a .aux file, look for RFC or Internet draft citations with this regular expression
    LATEX_CITATION_RE = re.compile(r"^\\citation\{((rfc.*)|(draft-.*))\}",re.I)
    TEX_EXTENSION = '.tex'
    AUX_EXTENSION = '.aux'

    def __init__(self, id_names=[], in_file_name=None, out_file_name=None):
        self._id_names      = id_names
        self._out_file_name = out_file_name

        self._id_name_err_list = []
        self._remote_fetch_err_list = [] # (type, name, url)

        if in_file_name is not None:
            self._id_names += self._read_ids_from_file(in_file_name)

    def _rfc_key_function(name):
        """Turn RFC32 into RFC00032 for sorting"""
        try:
            if name.upper().startswith('RFC'):
                return "RFC{:05d}".format( int(name[3:]))
        except (ValueError,TypeError) as e:
            raise BadRFCNumberException(name)
        return name

    def _read_ids_from_file(self, file_name):
        """
        Read identifiers from a text file. 
        If the text file is a LaTeX .aux file, parse the \citation{} command.
        If the text file is a LaTeX .tex file, parse the corresponding .aux file
        """
        file_name = pathlib.Path(file_name)
        if file_name.stem == TEX_EXTENSION:
            file_name_aux = file_name.parent / (file_name.stem + AUX_EXTENSION)
            if not file_name_aux.exists():
                raise RuntimeError("Run LaTeX on {} to create {}".format(file_name,file_name_aux)) 
            file_name = file_name_aux
        with file_name.open() as in_file:
            if file_name.suffix == AUX_EXTENSION:
                rfcs = set([m.group(1) for line in in_file for m in [self.LATEX_CITATION_RE.search(line)] if m])
                return sorted(rfcs, key=self._rfc_key_function)
            return [line.strip() for line in in_file ]

    def _generate_bibtex(self,out_file):
        for id_name in self._id_names:
            try:
                entry = self.get_bibtex_from_id(id_name)
                out_file.write(entry)
                out_file.write('\n\n')
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
            with open(self._out_file_name, 'w') as out_file:
                self._generate_bibtex(out_file)
        else:
            self._generate_bibtex(sys.stdout)

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
        response = response.strip()
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

        url = self.URL_FMT.format(id_type=id_type, id_name=id_name)
        return url, id_type, id_name

    def _get_response_from_url(self, url):
        uagent = random.choice(self.USER_AGENTS)
        req = request.Request(
            url,
            data=None,
            headers={
                'User-Agent': uagent
            }
        )
        with request.urlopen(url) as response:
            return response.read().decode()

def run():
    parser = Parser()
    parser = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()

    obj = RFCBibtex(parser.inline_args, parser.in_file, parser.out_file)
    obj.generate_bibtex()

if __name__ == '__main__':
    run()
