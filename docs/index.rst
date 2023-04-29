.. localized-unidecode documentation master file, created by
   sphinx-quickstart on Sat Apr 29 20:27:01 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to localized-unidecode's documentation!
===============================================
This project provides character transliteration functionality based on the rules of specific languages. The component takes a country and a text as input and outputs the text with characters transliterated into ASCII representations according to the rules of the specified language.

Currently the system has language-specific rules for these languages:

- Lithuanian
- Bulgarian
- Belarusian
- Russian
- Japanese (Hepburn romanization, needs checking)

For other languages, generic transliteration will be done as a fallback. Contributions are welcome for additional language support.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation

   modules

   user_documentation

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
