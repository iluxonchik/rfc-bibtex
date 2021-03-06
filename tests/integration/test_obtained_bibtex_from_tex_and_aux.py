"""
Integration tests related to reading raw list of RFCs providied in a text file (one per line)
and directly as command-line args.
"""
import vcr
from .base import BaseRFCBibTexIntegrationTestCase
from rfc_bibtex.rfc_bibtex import RFCBibtex

"""
NOTE: the tests are written with the migrations that will be done in consideration.
      For example, the URLs from which the RFC will be obtained will be changed,
      with this, there is also a change in the returned content. For this reason,
      tests were adapted to work in both of them. This is why some assertions might
      seem like incomplete. Later, the tests should and will be refactored.
"""
class ObtainedBibtexFromTexAndAuxFilesTestCase(BaseRFCBibTexIntegrationTestCase):
    TLS_RFCS_FILE_AUX = BaseRFCBibTexIntegrationTestCase.TEST_RESOURCES_PATH + "tls_rfcs.aux"
    TLS_RFCS_FILE_INVALID_IDS_AUX = BaseRFCBibTexIntegrationTestCase.TEST_RESOURCES_PATH + "tls_rfcs_invalid_ids.aux"
    TLS_RFCS_FILE_NON_EXISTING_IDS_AUX = BaseRFCBibTexIntegrationTestCase.TEST_RESOURCES_PATH + "tls_rfcs_non_existing_ids.aux"
    TLS_RFCS_FILE_TEX = BaseRFCBibTexIntegrationTestCase.TEST_RESOURCES_PATH + "tls_rfcs.tex"
    TLS_RFCS_FILE_INVALID_IDS_TEX = BaseRFCBibTexIntegrationTestCase.TEST_RESOURCES_PATH + "tls_rfcs_invalid_ids.tex"
    TLS_RFCS_FILE_NON_EXISTING_IDS_TEX = BaseRFCBibTexIntegrationTestCase.TEST_RESOURCES_PATH + "tls_rfcs_non_existing_ids.tex"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @vcr.use_cassette(path='tests/integration/resources/fixtures/vcr_cassettes/synopsis.yaml', record_mode='new_episodes')
    def test_reading_rfcs_from_aux_file_returns_expected_latex(self):
        rfc_bibtex = RFCBibtex(in_file_names=[self.TLS_RFCS_FILE_AUX])
        entries = list(rfc_bibtex.bibtex_entries)
        self.assertEqual(len(entries), 3)
        self.assertIn("RFC5246", entries[0])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.2", entries[0])
        self.assertIn("2008", entries[0])
        self.assertIn("RFC Editor", entries[0])

        self.assertIn("{draft-ietf-tls-tls13-21}", entries[1])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[1])

        self.assertIn("RFC8446", entries[2])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[2])
        self.assertIn("2018", entries[2])
        self.assertIn("RFC Editor", entries[2])

    @vcr.use_cassette(path='tests/integration/resources/fixtures/vcr_cassettes/synopsis.yaml', record_mode='new_episodes')
    def test_reading_rfcs_from_tex_file_returns_expected_latex(self):
        rfc_bibtex = RFCBibtex(in_file_names=[self.TLS_RFCS_FILE_TEX])
        entries = list(rfc_bibtex.bibtex_entries)
        self.assertEqual(len(entries), 3)
        self.assertIn("RFC5246", entries[0])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.2", entries[0])
        self.assertIn("2008", entries[0])
        self.assertIn("RFC Editor", entries[0])

        self.assertIn("{draft-ietf-tls-tls13-21}", entries[1])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[1])

        self.assertIn("RFC8446", entries[2])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[1])
        self.assertIn("2018", entries[2])
        self.assertIn("RFC Editor", entries[2])

    @vcr.use_cassette(path='tests/integration/resources/fixtures/vcr_cassettes/synopsis.yaml', record_mode='new_episodes')
    def test_reading_rfcs_aux_file_with_invalid_ids_returns_expected_latex(self):
        """
        Test that invalid RFC/draft IDs don't break the program.
        """
        rfc_bibtex = RFCBibtex(in_file_names=[self.TLS_RFCS_FILE_INVALID_IDS_AUX])
        entries = list(rfc_bibtex.bibtex_entries)
        self.assertEqual(len(entries), 3)
        self.assertIn("RFC5246", entries[0])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.2", entries[0])
        self.assertIn("2008", entries[0])
        self.assertIn("RFC Editor", entries[0])

        self.assertIn("{draft-ietf-tls-tls13-21}", entries[1])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[1])

        self.assertIn("RFC8446", entries[2])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[2])
        self.assertIn("2018", entries[2])
        self.assertIn("RFC Editor", entries[2])

    @vcr.use_cassette(path='tests/integration/resources/fixtures/vcr_cassettes/synopsis.yaml', record_mode='new_episodes')
    def test_reading_rfcs_from_aux_file_with_non_existing_rfcs_returns_expected_latex(self):
        """
        Test that non-exsting RFC/draft IDs don't break the program.
        """
        rfc_bibtex = RFCBibtex(in_file_names=[self.TLS_RFCS_FILE_NON_EXISTING_IDS_AUX])
        entries = list(rfc_bibtex.bibtex_entries)
        self.assertEqual(len(entries), 3)
        self.assertIn("RFC5246", entries[0])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.2", entries[0])
        self.assertIn("2008", entries[0])
        self.assertIn("RFC Editor", entries[0])

        self.assertIn("{draft-ietf-tls-tls13-21}", entries[1])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[1])

        self.assertIn("RFC8446", entries[2])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[2])
        self.assertIn("2018", entries[2])
        self.assertIn("RFC Editor", entries[2])

    @vcr.use_cassette(path='tests/integration/resources/fixtures/vcr_cassettes/synopsis.yaml', record_mode='new_episodes')
    def test_reading_rfcs_tex_file_with_invalid_ids_returns_expected_latex(self):
        """
        Test that invalid RFC/draft IDs don't break the program.
        """
        rfc_bibtex = RFCBibtex(in_file_names=[self.TLS_RFCS_FILE_INVALID_IDS_TEX])
        entries = list(rfc_bibtex.bibtex_entries)
        self.assertEqual(len(entries), 3)
        self.assertIn("RFC5246", entries[0])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.2", entries[0])
        self.assertIn("2008", entries[0])
        self.assertIn("RFC Editor", entries[0])

        self.assertIn("{draft-ietf-tls-tls13-21}", entries[1])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[1])

        self.assertIn("RFC8446", entries[2])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[2])
        self.assertIn("2018", entries[2])
        self.assertIn("RFC Editor", entries[2])


    @vcr.use_cassette(path='tests/integration/resources/fixtures/vcr_cassettes/synopsis.yaml', record_mode='new_episodes')
    def test_reading_rfcs_from_tex_file_with_non_existing_rfcs_returns_expected_latex(self):
        """
        Test that non-exsting RFC/draft IDs don't break the program.
        """
        rfc_bibtex = RFCBibtex(in_file_names=[self.TLS_RFCS_FILE_NON_EXISTING_IDS_TEX])
        entries = list(rfc_bibtex.bibtex_entries)
        self.assertEqual(len(entries), 3)
        self.assertIn("RFC5246", entries[0])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.2", entries[0])
        self.assertIn("2008", entries[0])
        self.assertIn("RFC Editor", entries[0])

        self.assertIn("{draft-ietf-tls-tls13-21}", entries[1])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[1])

        self.assertIn("RFC8446", entries[2])
        self.assertIn("The Transport Layer Security (TLS) Protocol Version 1.3", entries[2])
        self.assertIn("2018", entries[2])
        self.assertIn("RFC Editor", entries[2])