# Localized unidecode

This project provides character transliteration functionality based on the rules of specific languages. The component takes a country and a text as input and outputs the text with characters transliterated into ASCII representations according to the rules of the specified language.  
Documentation can be found here: https://localized-unidecode.readthedocs.io/en/latest/

## Supported languages

Currently the system has language-specific rules for these languages:

- Lithuanian
- Bulgarian
- Belarusian
- Russian
- Japanese (Hepburn romanization, needs checking)

For other languages, generic transliteration will be done as a fallback. Contributions are welcome for additional language support.

## Installation

The package can be installed using pip:  
`pip install -i https://test.pypi.org/simple/ localized-unidecode`

## Example usage

```python
from localized_unidecode import Decoder

decoder = Decoder('BG')

decoded_string = decoder.decode('Това е тест за демонстрация на проекта')
print(decoded_string)
```

Output: `Tova e test za demonstratsiia na proekta`

If you need to customize the default transliteration table, you can pass a dictionary containing the custom mapping to the decoder

```python
    from localized_unidecode import Decoder

    decoder = Decoder('BG', character_overrides={'х': 'h'})

    decoded_string = decoder.decode('доходи')
    print(decoded_string)
```

Output: `dohodi`

If you also want to decode common symbols, you can pass the `decode_symbols` keyword argument

```python
    from localized_unidecode import Decoder

    decoder = Decoder('RU', decode_symbols=True)

    decoded_string = decoder.decode('«тест»')
    print(decoded_string)
```

Output:`"test"`

You can also pass a fallback language in case the character is not found in the main language's transliteration table::

```python
    from localized_unidecode import Decoder

    decoder = Decoder('BG', fallback_language='LT')

    decoded_string = decoder.decode('lietuviškas тест')
    print(decoded_string)
```

Output:`lietuvishkas test`

## License

This software is licensed under the MIT License. See the LICENSE file for details.
