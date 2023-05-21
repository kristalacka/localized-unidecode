import unittest
from unittest.mock import patch

from src.localized_unidecode.decoder import Decoder


class DecoderTests(unittest.TestCase):
    def setUp(self):
        self.decoder = Decoder(language="gb")

    def test_decode_special_characters(self):
        decoded = self.decoder.decode("[@_!#$%^&*()<>?/\|}{~:] ")
        self.assertEqual(decoded, "[@_!#$%^&*()<>?/\|}{~:] ")

    def test_decode_ascii_characters(self):
        decoded = self.decoder.decode("Hello World!")
        self.assertEqual(decoded, "Hello World!")

    @patch("src.localized_unidecode.decoder.logger")
    def test_decode_unidecode_fallback(self, mock_logger):
        decoded = self.decoder.decode("ö")
        self.assertEqual(decoded, "o")
        mock_logger.debug.assert_called_with("Unable to decode character ö, falling back to unidecode.")

    def test_decode_transliteration(self):
        decoder = Decoder(language="ru")
        decoded = decoder.decode("Привет")
        self.assertEqual(decoded, "Privet")

    @patch("src.localized_unidecode.decoder.logger")
    def test_load_transliteration_warning(self, mock_logger):
        Decoder(language="fr")
        mock_logger.warning.assert_called_with("Unable to find transliteration for language FR")

    def test_character_overrides(self):
        character_overrides = {
            "ä": "ae",
            "ü": "ue",
        }
        decoder = Decoder(language="de", character_overrides=character_overrides)
        decoded = decoder.decode("äü")
        self.assertEqual(decoded, "aeue")

    def test_decode_symbols_disabled(self):
        decoder = Decoder(language="ru", decode_symbols=False)
        decoded = decoder.decode("«Hello»")
        self.assertEqual(decoded, "<<Hello>>")

    def test_decode_symbols_enabled(self):
        decoder = Decoder(language="ru", decode_symbols=True)
        decoded = decoder.decode("«Hello»")
        self.assertEqual(decoded, '"Hello"')

    def test_fallback_language(self):
        decoder = Decoder(language="ru", fallback_language="lt")
        decoded = decoder.decode("Привет žmonės")
        self.assertEqual(decoded, "Privet zhmones")

    def test_invalid_language_code(self):
        with self.assertRaises(ValueError):
            Decoder(language="xyz")


if __name__ == "__main__":
    unittest.main()
