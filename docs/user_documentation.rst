Example Usage
===================
This is an example of how to use the decoder::

    from localized_unidecode import Decoder

    decoder = Decoder('BG')

    decoded_string = decoder.decode('Това е тест за демонстрация на проекта')
    print(decoded_string)

The above code outputs the following::

    Tova e test za demonstracia na proekta

If you need to customize the default transliteration table, you can pass a dictionary containing the custom mapping to the decoder::

    from localized_unidecode import Decoder

    decoder = Decoder('BG', character_overrides={'х': 'h'})

    decoded_string = decoder.decode('доходи')
    print(decoded_string)

The above code outputs the following::
    
    dohodi

If you also want to decode common symbols, you can pass the `decode_symbols` keyword argument::

    from localized_unidecode import Decoder

    decoder = Decoder('RU', decode_symbols=True)

    decoded_string = decoder.decode('«тест»')
    print(decoded_string)

The above code outputs the following::

    "test"

You can also pass a fallback language in case the character is not found in the main language's transliteration table::

    from localized_unidecode import Decoder

    decoder = Decoder('BG', fallback_language='LT')

    decoded_string = decoder.decode('lietuviškas тест')
    print(decoded_string)

The above code outputs the following::

    lietuvishkas test