import json
import logging
from typing import Optional

from pycountry import countries
from unidecode import unidecode

logger = logging.getLogger("localized-unidecode.utils.decoder")


class Decoder:
    """
    Class for decoding characters to ASCII.
    """

    GENERIC_TRANSLITERATIONS = {
        "RU": "cyrillic",
    }
    SPECIAL_CHARACTERS = "[@_!#$%^&*()<>?/\|}{~:] "

    def __init__(
        self,
        language: str,
        fallback_language: Optional[str] = None,
        character_overrides: Optional[dict[str, str]] = None,
        *,
        decode_symbols: bool = False,
    ):
        """
        _summary_

        :param language: alpha 2 code of the input language
        """
        main_country = countries.get(alpha_2=language)
        if main_country is None:
            raise ValueError("Invalid language code")

        self.main_country = main_country
        self.fallback_country = countries.get(alpha_2=fallback_language) if fallback_language else None

        self.character_overrides = character_overrides or {}
        self.decode_symbols = decode_symbols

        self._load_transliterations()

    def decode(self, text: str) -> str:
        """
        Converts input text into an ASCII representation.

        :param text: input text
        :return: decoded text
        """
        return "".join(self._decode_character(c) for c in text)

    def _decode_character(self, character: str) -> str:
        if character in self.SPECIAL_CHARACTERS:
            return character

        if character in self._character_map:
            return self._character_map[character]

        if self.decode_symbols and character in self._symbol_map:
            return self._symbol_map[character]

        logger.warning(f"Unable to decode character {character}, falling back to generic unidecode.")
        return unidecode(character)

    def _load_transliterations(self):
        self._character_map = {}
        self._symbol_map = {}

        # Load generic transliterations
        if self.main_country.alpha_2 in self.GENERIC_TRANSLITERATIONS:
            self._load_transliteration(self.GENERIC_TRANSLITERATIONS[self.main_country.alpha_2])

        # Load main language transliterations
        self._load_transliteration(self.main_country.alpha_2)

        # Load fallback language transliterations
        if self.fallback_country:
            self._load_transliteration(self.fallback_country.alpha_2)

        self._character_map |= self.character_overrides

    def _load_transliteration(self, language: str):
        try:
            with open(f"utils/mappings/{language.upper()}.json", "r", encoding="utf-8") as f:
                transliteration = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Unable to find transliteration for language {language}")
            return

        self._symbol_map |= transliteration.get("symbols", {})
        self._character_map |= transliteration.get("characters", {})
        self._character_map |= {v.upper(): k.capitalize() for k, v in transliteration.get("characters", {}).items()}

        print({v.upper(): k.upper() for k, v in transliteration.get("symbols", {}).items()})
        print("CHAR MAP", self._character_map)
