.. MSCI documentation master file, created by
   sphinx-quickstart on Sun Dec 24 14:38:13 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================================
MSCI: Mass Spectrometry Content Information Python Library
==================================================

MSCI (Mass Spectrometry Content Information) is a Python package designed for the evaluation of peptide fragmentation spectra information content. The library provides a comprehensive toolset to analyze spectral similarities and aid in the selection of the most informative fragment ions, facilitating improved peptide identification in mass spectrometry-based proteomics.

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   usage
   API
   examples
   contributing
   references

Installation
============

Prerequisites
-------------

- Python 3.8 - 3.11
- Anaconda
- matchms
- Pyteomics
- OpenMS

Installation via pip
--------------------

You can install MSCI directly from PyPI using pip:

.. code-block:: bash

   pip install msci

Alternatively, you can install MSCI from source:

.. code-block:: bash

   git clone https://github.com/zahrael97/MSCI.git
   cd MSCI
   pip install .

For an interactive tutorial, you can explore the MSCI Google Colab notebook:

`Google Colab Tutorial <https://colab.research.google.com/drive/1ny97RNgvnpD7ZrHW8TTRXWCAQvIcavkk>`_

Usage
=====

MSCI enables researchers to analyze peptide fragmentation spectra and assess similarities between peptide sequences. The package includes functionalities for:

- **Proteome Import**: Supports FASTA and peptide list formats for in-silico digestion and spectral library import.
- **Spectra Prediction & Processing**: Uses Koina for spectra prediction and supports filtering and preprocessing of spectra.
- **Spectra Grouping**: Clusters peptide sequences based on user-defined MS1 m/z and indexed retention time (iRT) tolerances.
- **Similarity Measurement**: Implements spectral comparison methods such as normalized dot product, spectral angle, and greedy cosine similarity.
- **Output & Visualization**: Exports results as CSV, TSV, or Excel files and generates mirror plots for spectral comparison.

Quick Start
-----------

To analyze a set of peptide spectra, follow these steps:

.. code-block:: python

   from msci import MSCI
   msci = MSCI()
   peptides = msci.import_proteome("proteome.fasta")
   spectra = msci.predict_spectra(peptides)
   similarity_scores = msci.compute_similarity(spectra)
   msci.export_results("output.csv")


Contributing
============

Contributions are welcome! Please see our `GitHub repository <https://github.com/zahrael97/MSCI>`_ for guidelines on how to contribute.

References
==========


For more information, visit the `MSCI documentation <https://msci.readthedocs.io/en/latest/>`_.
