from distutils.core import setup
setup(
  name = 'rfc-bibtex',
  packages = ['rfc_bibtex'],
  version = '0.2.1',
  description = 'Generate Bibtex entries for IETF RFCs and Internet-Drafts.',
  author = 'Illya Gerasymchuk',
  author_email = 'giluxonchik@gmail.com',
  url = 'https://github.com/iluxonchik/rfc-bibtex/',
  download_url = 'https://github.com/iluxonchik/rfc-bibtex/archive/0.2.1.tar.gz',
  keywords = ['rfc', 'internet draft', 'latex', 'bibtex', 'ietf'],
  scripts=['bin/rfc-bibtex', 'bin/rfc_bibtex', 'bin/rfcbibtex'],
  classifiers = [],
)
