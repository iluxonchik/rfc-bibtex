import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='rfcbibtex',
    packages = ['rfc_bibtex'],
    version='0.3.2',
    author='Illya Gerasymchuk',
    author_email='illya@iluxonchik.me',
    description='Generate Bibtex entries for IETF RFCs and Internet Drafts.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/iluxonchik/rfc-bibtex/',
    download_url = 'https://github.com/iluxonchik/rfc-bibtex/archive/0.3.2.tar.gz',
    license = 'MIT',
    classifiers=(
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    keywords = ['rfc', 'internet draft', 'latex', 'bibtex', 'ietf'],
    scripts=['bin/rfcbibtex'], 
)

