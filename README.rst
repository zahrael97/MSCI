
.. raw:: html

   <p align="center">
      <img src="docs/MSCI_logo.png" alt="logo" width="300" height="300">
   </p>


.. image:: https://img.shields.io/pypi/v/msci.svg
        :target: https://pypi.python.org/pypi/msci


* Free software: MIT license
* Official Documentation available at: https://msci.readthedocs.io.


Peptide identification by mass spectrometry relies on the interpretation of fragmentation spectra based on the m/z pattern, relative intensities, and retention time (RT). Given a proteome, we wondered how many peptides generate very similar fragmentation spectra with current MS methods. MSCI is a Python package built to assess the information content of peptide fragmentation spectra, we aimed calculating an information-content index for all peptides in a given proteome would enable us to design data acquisition and data analysis strategies that generate and prioritize the most informative fragment ions to be queried for peptide quantification.

.. image:: docs/INTRODUCTION.png
  :alt: matchms workflow illustration
