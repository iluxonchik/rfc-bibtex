import unittest

from rfc_bibtex.rfc_bibtex import RFCBibtex
from rfc_bibtex.exceptions import BadRFCNumberException

class RegexParsingTestCase(unittest.TestCase):
    def test_re(self):
        self.assertTrue(RFCBibtex.AUX_CITATION_RE.search(r"\citation{RFC32}"))
        self.assertTrue(RFCBibtex.AUX_CITATION_RE.search(r"\citation{draft-tls-nothing}"))
        self.assertFalse(RFCBibtex.AUX_CITATION_RE.search(r"\citation{nothing}"))
