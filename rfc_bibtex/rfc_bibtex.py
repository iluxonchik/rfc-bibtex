#!/usr/bin/env python3
import sys, re
import pathlib
import os, os.path
from urllib import request
import urllib.error
import random

from .exceptions import BadIDNameException, URLFetchException, BadRFCNumberException
from .utils import print_red, print_yellow
from .parser import Parser
from .errors import Errors


class RFCBibtex(object):

    URL_FMT_RFC_OR_DRAFT_WITHOUT_ID       = 'https://datatracker.ietf.org/doc/{id_name}/bibtex/'
    URL_FMT_DRAFT                         = 'https://datatracker.ietf.org/doc/{id_name}/{version}/bibtex/'
    URL_ERROR_MSG = 'Failed to read RFC or Internt-Draft resource'
    ID_TYPE_RFC   = 'rfc'
    ID_TYPE_INTERNET_DRAFT = 'draft'

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
    AUX_CITATION_RE = re.compile(r"\\citation\{((rfc.+?)|(draft-.+?))\}",re.I)
    TEX_CITATION_RE = re.compile(r"\\cite\{((rfc.+?)|(draft-.+?))\}",re.I)
    TEX_EXTENSION = '.tex'
    AUX_EXTENSION = '.aux'

    def __init__(self, id_names=None, in_file_names=None, out_file_name=None):
        if id_names is None:
            id_names = []

        self._id_names      = id_names
        self._out_file_name = out_file_name

        self._id_name_err_list = []
        self._remote_fetch_err_list = [] # (type, name, url)
        self._urllib_err_list = [] # urllib errors when trying to access the urls

        # list of provided draft ids that do not explicity declare a version
        self._id_drafts_without_version_list = []

        # TODO: this approach adds up a massive tech debt, but its reduction will be done during
        #       the refactoring task
        self._errors = Errors()

        self._draft_version_re = re.compile(r"(?P<id>.+)-(?P<version>\d+)$", re.I)
        self._bibtex_id_re = re.compile(r"@\w+{(?P<bibtex_id>.+?),")
        self._updated_id_re = re.compile(r'%% You should probably cite (?P<new_id>(rfc|draft)[-\d\w]+)')

        if in_file_names:
            for in_file_name in in_file_names:
                self._id_names += self._read_ids_from_file(in_file_name)

        self._id_names = self._remove_duplicate_ids_preserving_order(self._id_names)
    
    def _remove_duplicate_ids_preserving_order(self, id_names):
        id_names_without_duplicates = set()
        # local var resoluiton is faster
        add_meth = id_names_without_duplicates.add
        return [x for x in id_names if not (x in id_names_without_duplicates or add_meth(x))]

    @property
    def bibtex_entries(self):
        # remove Nones (errors returned by urllib), so that they're not printed
        return filter(None.__ne__, [self.get_bibtex_from_id(id_name) for id_name in self._id_names])

    def _read_ids_from_plain_file(self, filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f ]

    def _read_ids_from_aux_file(self, filename):
        with open(filename, 'r') as f:
            rfcs = list([m.group(1) for line in f for m in [self.AUX_CITATION_RE.search(line)] if m])
        return rfcs

    def _read_ids_from_tex_file(self, filename):
        with open(filename, 'r') as f:
            rfcs = list([m.group(1) for line in f for m in [self.TEX_CITATION_RE.search(line)] if m])
        return rfcs

    def _read_ids_from_file(self, filename):
        """
        Read identifiers from a text file. 
        If the text file is a LaTeX .aux file, parse the \citation{} command.
        If the text file is a LaTeX .tex file, parse the corresponding .aux file
        """
        filename = pathlib.Path(filename)

        if filename.suffix == self.AUX_EXTENSION:
            return self._read_ids_from_aux_file(filename)
        elif filename.suffix == self.TEX_EXTENSION:
            return self._read_ids_from_tex_file(filename)
        else:
            # file containing one ID per line 
            return self._read_ids_from_plain_file(filename)

    def _generate_bibtex(self, outfile=sys.stdout):
        for entry in self.bibtex_entries:
            output = '{}\n'.format(entry)
            print(output, file=outfile)

    def _print_errors(self):
        if self._id_name_err_list:
            print_red('The following identifier names are invalid:', file=sys.stderr)
            for id_name in self._id_name_err_list:
                print_red('\t* {}'.format(id_name), file=sys.stderr)

        if self._remote_fetch_err_list:
            print_red('Errors in fetching from the following URLs:\n', file=sys.stderr)
            for err_tuple in self._remote_fetch_err_list:
                type_name = err_tuple[0] if err_tuple[0] == self.ID_TYPE_RFC else 'Internet Draft'
                print('\t* Type:{} | ID:{} | URL:{}'.format(type_name, err_tuple[1], err_tuple[2]), file=sys.stderr)

    def _print_no_explicit_version_warnings(self):
        if self._id_drafts_without_version_list:
            print_yellow('WARNING', file=sys.stderr)
            print_yellow('If the draft version is not explicitly defined in the draft ID, the latest one will be obtained,\n'
                  'which may be an RFC ID, in case the draft has been assigned one. If the latter happens, you will receive a\n'
                  'separate warning of the drafts that are now in the RFC stage. It is highly recommended to define the draft ID\n'
                  'explicitly, since there may be major document differences between two draft versions.\n', file=sys.stderr)
            print_yellow('No explicit version has been defined for following draft ids:', file=sys.stderr)
            for draft_id in self._id_drafts_without_version_list:
                print_yellow('\t* {}'.format(draft_id.lower()), file=sys.stderr)

    def _print_urllib_errors(self):
        if self._urllib_err_list:
            print_red('Errors when fetching the following URLs: ', file=sys.stderr)
            for url in self._urllib_err_list:
                print_red('\t* {}'.format(url), file=sys.stderr)
    
    def _print_updated_id_errors(self):
        # TODO: find a more elegant way of testing if an iterator has elements
        rfc_errors = list(self._errors.draft_updated_to_rfc)
        draft_errors = list(self._errors.draft_updated_to_draft)

        if draft_errors:
            print_yellow('The following drafts have been updated to a new draft version:', file=sys.stderr)
            for updated_entity in draft_errors:
                print_yellow('\t* {} --> {}'.format(updated_entity.old_id.lower(), updated_entity.new_id), file=sys.stderr)

        if rfc_errors:
            print_red('The following drafts have been updated to an RFC:', file=sys.stderr)
            for updated_entity in rfc_errors:
                print_red('\t* {} --> {}'.format(updated_entity.old_id.lower(), updated_entity.new_id), file=sys.stderr)

    def generate_bibtex(self):
        if self._out_file_name is not None:
            with open(self._out_file_name, 'w') as out_file:
                self._generate_bibtex(out_file)
        else:
            self._generate_bibtex(sys.stdout)

        # TODO: refactor error collection and printing
        self._print_no_explicit_version_warnings()
        self._print_updated_id_errors()
        self._print_errors()
        self._print_urllib_errors()

    def _make_title_uppercase(self, response):
        r = re.compile(r'(title = )({.*})')
        res =  r.sub(r'\1{\2}', response)
        return res

    def _replace_bibtex_name_if_needed(self, response, id_name):
        bibtex_id = self._get_id_from_bibtex(response)
        if (self._id_is_rfc(id_name) or self._id_is_draft(id_name)):
            new_response = re.sub(bibtex_id, id_name, response, count=1)
            return new_response
        else:
            # id is neither RFC, nor draft, this should nenver happen
            raise Exception("Unexpected entry id: {id_name}. Expecting either an RFC or a draft".format(id_name))
    
    def _collect_updated_ids(self, old_id, response):
        match = self._updated_id_re.search(response)
        if match:
            new_id = match.group('new_id')
            self._errors.add_updated_entity(old_id, new_id)
    
    def get_bibtex_from_id(self, id_name):
        try:
            url, id_type, id_name = self._get_url_from_id_name(id_name)
            response = self._get_response_from_url(url)
            self._collect_updated_ids(id_name, response)
            # override ids for drafts
            response = self._replace_bibtex_name_if_needed(response, id_name)
        except urllib.error.HTTPError:
            self._urllib_err_list.append(url)
            return None
        except BadIDNameException:
            return None

        if response.startswith(self.URL_ERROR_MSG):
            self._remote_fetch_err_list += [(id_type, id_name, url)]
            return None # None type objects will be ignored by the output
        response = self._make_title_uppercase(response)
        response = response.strip()
        return response

    def _get_url_from_rfc_id(self, rfc_id):
        return self.URL_FMT_RFC_OR_DRAFT_WITHOUT_ID.format(id_name=rfc_id)

    def _get_url_from_draft_id(self, draft_id):
        match = self._draft_version_re.search(draft_id)
        
        if match:
            # draft version has been found
            draft_id_without_version = match.group('id')
            draft_version = match.group('version')
            return self.URL_FMT_DRAFT.format(id_name=draft_id_without_version, version=draft_version)
        else:
            self._id_drafts_without_version_list.append(draft_id)
            return self.URL_FMT_RFC_OR_DRAFT_WITHOUT_ID.format(id_name=draft_id)

    @staticmethod
    def _id_is_draft(id_name):
        return bool(re.match(RFCBibtex.ID_TYPE_INTERNET_DRAFT, id_name, re.I))
    
    @staticmethod
    def _id_is_rfc(id_name):
        return bool(re.match(RFCBibtex.ID_TYPE_RFC, id_name, re.I))
    
    def _get_id_from_bibtex(self, bibtex):
        match = self._bibtex_id_re.search(bibtex)
        if match:
            return match.group('bibtex_id')
        raise BadIDNameException('Could not parse id of the bibtex: {}'.format(bibtex))

    def _get_url_from_id_name(self, id_name):
        id_type = None # needed for error reporting

        if self._id_is_rfc(id_name):
            return self._get_url_from_rfc_id(id_name), self.ID_TYPE_RFC, id_name
        elif self._id_is_draft(id_name):
            return self._get_url_from_draft_id(id_name), self.ID_TYPE_RFC, id_name
        else:
            # we have an error in an id, but let's not fail the program
            # letting the valid names complete. We'll simply notify the user
            # of the error at the end.
            self._id_name_err_list += [id_name]
            raise BadIDNameException()

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

    obj = RFCBibtex(parser.inline_args, parser.in_files, parser.out_file)
    obj.generate_bibtex()

if __name__ == '__main__':
    run()
