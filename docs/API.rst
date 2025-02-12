MSCI Documentation
=================

.. contents:: Table of Contents
   :depth: 2
   :local:



Functions
---------

generate_variable_length_peptides(protein_sequence, min_length=8, max_length=11)
-------------------------------------------------------------------------------

Generates all possible peptides of varying lengths from a given protein sequence.

**Parameters:**
    - **protein_sequence** (*str*) -- The protein sequence from which peptides are generated.
    - **min_length** (*int, optional*) -- The minimum length of peptides to generate (default: 8).
    - **max_length** (*int, optional*) -- The maximum length of peptides to generate (default: 11).

**Returns:**
    - **list** -- A list of generated peptides of varying lengths.

**Example:**
    .. code-block:: python

        peptides = generate_variable_length_peptides("ABCDEFG", min_length=3, max_length=5)
        print(peptides)
        # Output: ['ABC', 'BCD', 'CDE', 'DEF', 'EFG', 'ABCD', 'BCDE', 'CDEF', 'DEFG', 'ABCDE', 'BCDEF', 'CDEFG']


extract_peptides_from_fasta(fasta_path, min_length=8, max_length=11)
--------------------------------------------------------------------

Reads a FASTA file and extracts peptides from each protein sequence.

**Parameters:**
    - **fasta_path** (*str*) -- The path to the FASTA file.
    - **min_length** (*int, optional*) -- The minimum length of peptides to extract (default: 8).
    - **max_length** (*int, optional*) -- The maximum length of peptides to extract (default: 11).

**Returns:**
    - **list** -- A list of peptides extracted from the protein sequences in the FASTA file.

**Example:**
    .. code-block:: python

        peptides = extract_peptides_from_fasta("example.fasta", min_length=3, max_length=5)
        print(peptides)
        # Output: ['ABC', 'BCD', 'CDE', 'DEF', 'EFG', ...]

keep_top_n_peaks(spectrum, n)
------------------------------

Filters a spectrum to retain only the top `n` most intense peaks.

**Parameters:**
    - **spectrum** (*object*) -- A spectrum object containing mass-to-charge ratio (m/z) peaks.
    - **n** (*int*) -- The number of top peaks to retain.

**Returns:**
    - **object** -- A spectrum object with only the top `n` peaks.

**Example:**
    .. code-block:: python

        filtered_spectrum = keep_top_n_peaks(spectrum, n=5)
        print(filtered_spectrum)

filter_spectra_by_top_peaks(input_file_path, output_file_path, n_peaks)
------------------------------------------------------------------------

Reads a pickled list of spectra, processes each spectrum to keep only the top `n` peaks, and saves the results.

**Parameters:**
    - **input_file_path** (*str*) -- Path to the input pickle file containing spectra.
    - **output_file_path** (*str*) -- Path to save the processed spectra as a pickle file.
    - **n_peaks** (*int*) -- The number of top peaks to retain in each spectrum.

**Returns:**
    - **list** -- A list of processed spectra with only the top `n` peaks.


reading MS spectra
---------------------

This module provides functionality to read and process mass spectrometry files, including MSP, MGF, and MZML formats.


read_msp_file
-------------
Reads an MSP file and returns a DataFrame containing the spectra information.

:param filename: The path to the MSP file
:type filename: str
:returns: A DataFrame with spectra information
:rtype: pandas.DataFrame

The returned DataFrame contains the following columns:

- **Name** -- The name of the spectrum
- **MW** -- Mass/charge of the spectrum
- **iRT** -- Indexed retention time

`Download Example Data <https://github.com/proteomicsunitcrg/MSCI/tree/main/Example_data>`

---

read_mgf_file
-------------
Reads an MGF file and returns a list of spectra data.

:param filename: The path to the MGF file
:type filename: str
:returns: A list of dictionaries containing spectra data
:rtype: list[dict]

Each dictionary contains:

- **mz_values**
- **intensities**
- **MW**
- **RT**

`Download Example Data <https://github.com/proteomicsunitcrg/MSCI/tree/main/Example_data>`

---

read_mzml_file
--------------
Reads an MZML file and returns a list of processed spectrum data.

:param filename: The path to the MZML file
:type filename: str
:returns: A list of processed spectrum data
:rtype: list[dict]

`Download Example Data <https://github.com/proteomicsunitcrg/MSCI/tree/main/Example_data>`

---

read_ms_file
------------
Determines the file format and calls the appropriate function to read the mass spectrometry file.

:param filename: The path to the mass spectrometry file
:type filename: str
:returns: A DataFrame or a list depending on the file format
:rtype: pandas.DataFrame | list

`Example Data <https://github.com/proteomicsunitcrg/MSCI/tree/main/Example_data>`_


Grouping MS1 Module
--------------------

This module provides functions for grouping MS1 peptides based on mass-to-charge ratio (m/z) and indexed retention time (iRT) using k-d tree data structures and tolerance calculations.

Functions
~~~~~~~~

make_data_compatible(index_df)
--------------------

Converts a DataFrame into a list of tuples compatible with further processing.

:Parameters:
    - **index_df** (*pandas.DataFrame*) -- DataFrame containing mass spectrometry data with columns ``MW`` and ``iRT``

:Returns:
    **list** of tuples in format ``(index, MW, iRT)``

within_ppm(pair, ppm_tolerance1, ppm_tolerance2)
--------------------

Checks if two peptide pairs are within specified tolerances.

:Parameters:
    - **pair** (*tuple*) -- Two peptide tuples ``((index1, MW1, iRT1), (index2, MW2, iRT2))``
    - **ppm_tolerance1** (*float*) -- PPM tolerance for m/z values
    - **ppm_tolerance2** (*float*) -- Absolute tolerance for iRT values

:Returns:
    **bool** -- True if within tolerances, False otherwise

within_tolerance(pair, tolerance1, tolerance2)
--------------------

Checks if peptide pairs are within absolute tolerances.

:Parameters:
    - **pair** (*tuple*) -- Two peptide tuples ``((index1, MW1, iRT1), (index2, MW2, iRT2))``
    - **tolerance1** (*float*) -- Absolute tolerance for m/z values
    - **tolerance2** (*float*) -- Absolute tolerance for iRT values

:Returns:
    **bool** -- True if within tolerances, False otherwise

find_combinations_kdtree(data, tolerance1, tolerance2, use_ppm=True)
--------------------

Uses k-d tree for efficient querying of valid peptide combinations.

:Parameters:
    - **data** (*list*) -- Peptide data tuples ``(index, MW, iRT)``
    - **tolerance1** (*float*) -- Tolerance for m/z values
    - **tolerance2** (*float*) -- Tolerance for iRT values
    - **use_ppm** (*bool*) -- Use PPM tolerance if True, absolute if False

:Returns:
    **list** of valid peptide pairs

Similarity Module
---------------

This module calculates similarity between mass spectrometry spectra using various methods.

Functions and Classes
~~~~~~~~~~~~~~~~~~~

ndotproduct(x, y, m=0, n=0.5, na_rm=True)
--------------------

Calculates normalized dot product between spectra.

:Parameters:
    - **x** (*pandas.DataFrame*) -- First spectrum (m/z and intensities)
    - **y** (*pandas.DataFrame*) -- Second spectrum (m/z and intensities)
    - **m** (*float*) -- M/z values exponent (default: 0)
    - **n** (*float*) -- Intensity values exponent (default: 0.5)
    - **na_rm** (*bool*) -- Remove missing values (default: True)

:Returns:
    **float** -- Normalized dot product

nspectraangle(x, y, m=0, n=0.5, na_rm=True)
--------------------

Calculates normalized spectral angle between spectra.

:Parameters:
    - **x** (*pandas.DataFrame*) -- First spectrum (m/z and intensities)
    - **y** (*pandas.DataFrame*) -- Second spectrum (m/z and intensities)
    - **m** (*float*) -- M/z values exponent (default: 0)
    - **n** (*float*) -- Intensity values exponent (default: 0.5)
    - **na_rm** (*bool*) -- Remove missing values (default: True)

:Returns:
    **float** -- Normalized spectral angle

joinPeaks(tolerance=0, ppm=0)
--------------------

Class that joins peaks from two spectra based on m/z and intensity values.

:Parameters:
    - **tolerance** (*float*) -- Absolute tolerance for m/z matching
    - **ppm** (*float*) -- PPM tolerance for m/z matching

Methods:
    - **match(x, y)** -- Matches peaks from two spectra
        - Parameters: Two DataFrames with m/z and intensities
        - Returns: Tuple of matched peaks DataFrames

Mutation Module
-------------

Tools for processing proteins by simulating peptide digestion and introducing mutations.


ProteinMutator
--------------------

.. class:: ProteinMutator(proteome_file, mutations_file, output_dir, digestion_method)

    Handles protein mutations and peptide generation.

    :Parameters:
        - **proteome_file** (*str*) -- Path to FASTA proteome file
        - **mutations_file** (*str*) -- Path to TSV mutations file
        - **output_dir** (*str*) -- Output directory path
        - **digestion_method** (*callable*) -- Function returning peptide list

    Methods:
        - **load_proteome()** -- Loads proteome sequences
        - **load_mutations()** -- Loads mutation data
        - **process_protein(target_protein_accession)** -- Processes single protein
        - **process_all_proteins()** -- Processes all proteins

tryptic_digest(sequence)
--------------------

Simulates tryptic digestion of protein sequence.

:Parameters:
    - **sequence** (*str*) -- Protein sequence

:Returns:
    **list** -- Resulting peptides
