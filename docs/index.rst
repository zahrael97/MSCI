.. MSCI documentation master file, created by
   sphinx-quickstart on Sun Dec 24 14:38:13 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MSCI : Mass Spectrometry Content Information python Library
Contents
--------

Installation
============

.. toctree::
   :maxdepth: 1

   installation

API 
=============

.. toctree::
   :maxdepth: 2

   API






Peptide identification by mass spectrometry relies on the interpretation of fragmentation spectra based on the m/z pattern, relative intensities, and retention time (RT). Given a proteome, we wondered how many peptides generate very similar fragmentation spectra with current MS methods. *MSCI*  is a Python package built to assess the information content of peptide fragmentation spectra, we aimed to calculate an information-content index for all peptides in a given proteome that would enable us to design data acquisition and data analysis strategies that generate and prioritize the most informative fragment ions to be queried for peptide quantification.

.. image:: INTRODUCTION.png
  :alt: matchms workflow illustration


Installation
==================
prerequisites:

- Python 3.8 -3.11
- Anaconda
- Matchms

