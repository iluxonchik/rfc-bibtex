import pytest

from rfc_bibtex.rfc_bibtex import RFCBibtex

def test_re():
    assert RFCBibtex.latex_citation_re.search(r"\citation{RFC32}")
    assert RFCBibtex.latex_citation_re.search(r"\citation{draft-tls-nothing}")
    assert not RFCBibtex.latex_citation_re.search(r"\citation{nothing}")

def test_rfc_keyfunction():
    assert RFCBibtex._rfc_key_function("RFC32")=="RFC00032"
    assert RFCBibtex._rfc_key_function("RFC32a")=="RFC32a"
    assert RFCBibtex._rfc_key_function("draft-nothing")=="draft-nothing"
