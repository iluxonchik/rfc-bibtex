#
# a Makefile so we can say 'make check'

check:
	python -m unittest tests/rfc_bibtex_test.py
