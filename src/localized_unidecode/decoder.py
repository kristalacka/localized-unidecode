import json
import logging
import os
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
        Constructor for symbol decoder.

        :param language: Alpha2 code of the input language
        :param fallback_language: Alpha2 code of a fallback language, defaults to None
        :param character_overrides: Custom overrides to replace default decoding behavior, defaults to None
        :param decode_symbols: Whether to decode symbols, e.g. `« »` to `" "`, defaults to False
        :raises ValueError: if the provided main language code is invalid
        """
        main_country = countries.get(alpha_2=language)
        if main_country is None:
            raise ValueError("Invalid language code")

        self.main_country = main_country
        self.fallback_country = countries.get(alpha_2=fallback_language) if fallback_language else None

        self.character_overrides = character_overrides or {}
        self.decode_symbols = decode_symbols

        self._character_map = {}
        self._symbol_map = {}
        self._load_transliterations()

    def decode(self, text: str) -> str:
        """
        Converts input text into an ASCII representation.

        :param text: input text
        :return: decoded text
        """
        return "".join(self._decode_character(c) for c in text)

    def _decode_character(self, character: str) -> str:
        """
        Decodes a single character. Output representation can be multiple characters.

        :param character: Input character
        :return: Decoded character
        """
        if character in self.SPECIAL_CHARACTERS:
            return character

        if character in self._character_map:
            return self._character_map[character]

        if self.decode_symbols and character in self._symbol_map:
            return self._symbol_map[character]

        if character.isascii():
            return character

        logger.debug(f"Unable to decode character {character}, falling back to unidecode.")
        return unidecode(character)

    def _load_transliterations(self):
        """
        Loads all relevant transliterations for the decoder.
        """
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
        """
        Loads a specific character mapping.

        :param language: mapping to load.
        """
        try:
            with open(
                os.path.join(os.path.dirname(__file__), f"utils/mappings/{language.upper()}.json"),
                "r",
                encoding="utf-8",
            ) as f:
                transliteration = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Unable to find transliteration for language {language}")
            return

        self._symbol_map = {**transliteration.get("symbols", {}), **self._symbol_map}
        self._character_map = {**transliteration.get("characters", {}), **self._character_map}
        self._character_map = {
            **{k.upper(): v.capitalize() for k, v in transliteration.get("characters", {}).items()},
            **self._character_map,
        }
