

Contents:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   preprocessing
   grouping_ms1
   similarity

.. note::

Multiprocessing Module
======================

This module provides functionality to read and process mass spectrometry files, including MSP, MGF, and MZML formats.

Functions
---------

.. autofunction:: read_msp_file
    :module: MSCI.multiprocessing

    Reads an MSP file and returns a DataFrame containing the spectra information.

    **Parameters:**
    - `filename` (str): The path to the MSP file.

    **Returns:**
    - `pandas.DataFrame`: A DataFrame containing the following columns:
        - `Name`: The name of the spectrum.
        - `MW`: Molecular weight of the spectrum.
        - `iRT`: Indexed retention time.

.. autofunction:: process_spectrum
    :module: MSCI.multiprocessing

    Processes a single spectrum from an MZML file.

    **Parameters:**
    - `spectrum` (pyopenms.MSSpectrum): A single spectrum object from an MZML file.

    **Returns:**
    - `dict`: A dictionary containing the processed spectrum data with keys 'MW', 'RT', 'Num Peaks', and 'Peaks'.

.. autofunction:: read_mgf_file
    :module: MSCI.multiprocessing

    Reads an MGF file and returns a list of spectra data.

    **Parameters:**
    - `filename` (str): The path to the MGF file.

    **Returns:**
    - `list`: A list of dictionaries, each containing `mz_values`, `intensities`, `MW`, and `RT` for a spectrum.

.. autofunction:: read_mzml_file
    :module: MSCI.multiprocessing

    Reads an MZML file and returns a list of processed spectrum data.

    **Parameters:**
    - `filename` (str): The path to the MZML file.

    **Returns:**
    - `list`: A list of dictionaries containing processed spectrum data.

.. autofunction:: read_ms_file
    :module: MSCI.multiprocessing

    Determines the file format and calls the appropriate function to read the mass spectrometry file.

    **Parameters:**
    - `filename` (str): The path to the mass spectrometry file.

    **Returns:**
    - `pandas.DataFrame` or `list`: Depending on the file format, returns either a DataFrame or a list of dictionaries.


Grouping MS1 Module
===================

This module provides functions for grouping MS1 peptides based on mass-to-charge ratio (m/z) and indexed retention time (iRT) using k-d tree data structures and tolerance calculations.

Functions
---------

.. autofunction:: make_data_compatible
    :module: MSCI.grouping_ms1

    Converts a DataFrame into a list of tuples compatible with further processing.

    **Parameters:**
    - `index_df` (pandas.DataFrame): DataFrame containing the mass spectrometry data with columns 'MW' (m/z) and 'iRT'.

    **Returns:**
    - `list`: A list of tuples in the format `(index, MW, iRT)`.

.. autofunction:: within_ppm
    :module: MSCI.grouping_ms1

    Checks if two peptide pairs are within a specified ppm (parts per million) tolerance for m/z and absolute tolerance for iRT.

    **Parameters:**
    - `pair` (tuple): A tuple containing two peptide tuples in the format `((index1, MW1, iRT1), (index2, MW2, iRT2))`.
    - `ppm_tolerance1` (float): The ppm tolerance for the m/z values.
    - `ppm_tolerance2` (float): The absolute tolerance for the iRT values.

    **Returns:**
    - `bool`: True if the pair is within the specified tolerances, False otherwise.

.. autofunction:: within_tolerance
    :module: MSCI.grouping_ms1

    Checks if two peptide pairs are within specified absolute tolerances for both m/z and iRT.

    **Parameters:**
    - `pair` (tuple): A tuple containing two peptide tuples in the format `((index1, MW1, iRT1), (index2, MW2, iRT2))`.
    - `tolerance1` (float): The absolute tolerance for the m/z values.
    - `tolerance2` (float): The absolute tolerance for the iRT values.

    **Returns:**
    - `bool`: True if the pair is within the specified tolerances, False otherwise.

.. autofunction:: find_combinations_kdtree
    :module: MSCI.grouping_ms1

    Finds valid peptide combinations within specified tolerances using a k-d tree for efficient querying.

    **Parameters:**
    - `data` (list): A list of tuples containing peptide data in the format `(index, MW, iRT)`.
    - `tolerance1` (float): The tolerance for the m/z values.
    - `tolerance2` (float): The tolerance for the iRT values.
    - `use_ppm` (bool): If True, use ppm tolerance for m/z values; otherwise, use absolute tolerance.

    **Returns:**
    - `list`: A list of valid peptide pairs within the specified tolerances.

.. autofunction:: process_peptide_combinations
    :module: MSCI.grouping_ms1

    Processes peptide combinations from the mass spectrometry data, finding valid pairs within specified tolerances.

    **Parameters:**
    - `mz_irt_df` (pandas.DataFrame): DataFrame containing peptide data with columns 'Name', 'MW', and 'iRT'.
    - `tolerance1` (float): The tolerance for the m/z values.
    - `tolerance2` (float): The tolerance for the iRT values.
    - `use_ppm` (bool): If True, use ppm tolerance for m/z values; otherwise, use absolute tolerance.

    **Returns:**
    - `pandas.DataFrame`: A DataFrame containing the resulting valid peptide pairs with their indices, names, m/z values, and iRT values.


Similarity Module
=================

This module provides functions and classes to calculate similarity between mass spectrometry spectra using various methods such as dot product, spectral angle, and cosine similarity.

Functions and Classes
---------------------

.. autofunction:: ndotproduct
    :module: MSCI.similarity

    Calculates the normalized dot product between two spectra.

    **Parameters:**
    - `x` (pandas.DataFrame): DataFrame containing the first spectrum with columns for m/z and intensities.
    - `y` (pandas.DataFrame): DataFrame containing the second spectrum with columns for m/z and intensities.
    - `m` (float): Exponent for the m/z values in the weight calculation. Default is 0.
    - `n` (float): Exponent for the intensity values in the weight calculation. Default is 0.5.
    - `na_rm` (bool): If True, removes missing values (not used in current implementation). Default is True.

    **Returns:**
    - `float`: The normalized dot product between the two spectra.

.. autofunction:: nspectraangle
    :module: MSCI.similarity

    Calculates the normalized spectral angle between two spectra.

    **Parameters:**
    - `x` (pandas.DataFrame): DataFrame containing the first spectrum with columns for m/z and intensities.
    - `y` (pandas.DataFrame): DataFrame containing the second spectrum with columns for m/z and intensities.
    - `m` (float): Exponent for the m/z values in the weight calculation. Default is 0.
    - `n` (float): Exponent for the intensity values in the weight calculation. Default is 0.5.
    - `na_rm` (bool): If True, removes missing values (not used in current implementation). Default is True.

    **Returns:**
    - `float`: The normalized spectral angle between the two spectra.

.. autoclass:: joinPeaks
    :module: MSCI.similarity
    :members:
    
    A class to join peaks from two spectra based on m/z and intensity values using tolerance and ppm values.

    **Parameters:**
    - `tolerance` (float): Absolute tolerance for matching m/z values. Default is 0.
    - `ppm` (float): Parts per million (ppm) tolerance for matching m/z values. Default is 0.

    **Methods:**

    - **match(x, y)**:
        Matches peaks from two spectra based on the specified tolerance and ppm values.

        **Parameters:**
        - `x` (pandas.DataFrame): DataFrame containing the first spectrum with columns for m/z and intensities.
        - `y` (pandas.DataFrame): DataFrame containing the second spectrum with columns for m/z and intensities.

        **Returns:**
        - `tuple`: Two DataFrames containing the matched peaks from `x` and `y`.

.. autofunction:: process_spectra_pairs
    :module: MSCI.similarity

    Processes pairs of spectra and calculates the similarity score using the spectral angle method.

    **Parameters:**
    - `chunk` (list): List of index pairs to process.
    - `spectra` (list): List of spectra objects.
    - `mz_irt_df` (pandas.DataFrame): DataFrame containing peptide data with columns 'Name', 'MW', and 'iRT'.
    - `tolerance` (float): Absolute tolerance for m/z matching. Default is 0.
    - `ppm` (float): Parts per million (ppm) tolerance for m/z matching. Default is 0.
    - `m` (float): Exponent for the m/z values in the weight calculation. Default is 0.
    - `n` (float): Exponent for the intensity values in the weight calculation. Default is 0.5.

    **Returns:**
    - `pandas.DataFrame`: A DataFrame containing the similarity scores for the processed spectra pairs.

.. autofunction:: process_spectra_pairs_cosine
    :module: MSCI.similarity

    Processes pairs of spectra and calculates the similarity score using the CosineGreedy method.

    **Parameters:**
    - `chunk` (list): List of index pairs to process.
    - `spectra` (list): List of spectra objects.
    - `mz_irt_df` (pandas.DataFrame): DataFrame containing peptide data with columns 'Name', 'MW', and 'iRT'.
    - `tolerance` (float): Tolerance for m/z matching in the CosineGreedy method. Default is 0.

    **Returns:**
    - `pandas.DataFrame`: A DataFrame containing the similarity scores for the processed spectra pairs.



