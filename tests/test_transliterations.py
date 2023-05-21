import unittest

from src.localized_unidecode.decoder import Decoder


class TransliterationTests(unittest.TestCase):
    def test_lithuanian_transliteration(self):
        decoder = Decoder(language="lt")
        decoded = decoder.decode("Ąčęėįšųūž")
        self.assertEqual(decoded, "Acheeeeshuuzh")

    def test_bulgarian_transliteration(self):
        decoder = Decoder(language="bg")
        decoded = decoder.decode("България")
        self.assertEqual(decoded, "Balgariya")

    def test_belarusian_transliteration(self):
        decoder = Decoder(language="be")
        decoded = decoder.decode("Беларусь")
        self.assertEqual(decoded, "Belarusʹ")

    def test_japanese_transliteration(self):
        decoder = Decoder(language="jp")
        decoded = decoder.decode("こんにちは")
        self.assertEqual(decoded, "konnichiha")

    def test_russian_transliteration(self):
        decoder = Decoder(language="ru")
        decoded = decoder.decode("Привет")
        self.assertEqual(decoded, "Privet")


if __name__ == "__main__":
    unittest.main()
