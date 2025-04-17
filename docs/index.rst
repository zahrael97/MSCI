.. MSCI documentation master file, created by
   sphinx-quickstart.

============================================
MSCI: Mass Spectrometry Content Information Python Library
============================================

MSCI is a Python package designed for the assessment of peptide fragmentation spectra information content. It helps researchers identify indistinguishable peptides in a given proteome by analyzing spectral similarity scores. 

.. image:: INTRODUCTION.png
   :alt: MSCI workflow illustration

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   tutorial
   API
   GUI
   contributing

API
===

The MSCI package offers functionalities for:

- **Data Import:** Load proteomes and spectral libraries.
- **Spectra Prediction & Processing:** Predict peptide spectra and filter fragments.
- **Spectra Grouping:** Group peptides based on m/z and iRT values.
- **Similarity Measurement:** Compute spectral similarity using different scoring functions.
- **Output & Visualization:** Export similarity results and generate fragmentation plots.

For full API documentation, see :doc:`API`.

Usage
=====

Example workflow:

For a full tutorial, visit our Colab notebook:
https://colab.research.google.com/drive/1ny97RNgvnpD7ZrHW8TTRXWCAQvIcavkk


For Code and datasets visit https://github.com/proteomicsunitcrg/MSCI

Graphical User Interface (GUI)
==============================

MSCI includes a web-based GUI for non-programmers, accessible at:
https://msci--proteomicsunit.streamlit.app/


License
=======

MSCI is released under the MIT License.
