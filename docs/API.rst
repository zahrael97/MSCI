.. MSCI Documentation

========

.. toctree::
   :maxdepth: 2
   :caption: **Contents**
   :titlesonly:

   preprocessing
   grouping_ms1
   similarity
   mutation

.. role:: red
.. role:: blue
.. role:: green
.. role:: bold

Multiprocessing Module
======================

:blue:`This module provides functionality to read and process mass spectrometry files, including MSP, MGF, and MZML formats.`

Functions
=========

:brown:`**read_msp_file(filename)**`

    :blue:`Reads an MSP file and returns a DataFrame containing the spectra information.`

    :green:`**Parameters:**`
    - :bold:`filename` (:red:`str`): The path to the MSP file.

    :green:`**Returns:**`
    - :bold:`pandas.DataFrame`: A DataFrame containing the following columns:
        - :bold:`Name`: The name of the spectrum.
        - :bold:`MW`: Molecular weight of the spectrum.
        - :bold:`iRT`: Indexed retention time.

:brown:`**process_spectrum(spectrum)**`

    :blue:`Processes a single spectrum from an MZML file.`

    :green:`**Parameters:**`
    - :bold:`spectrum` (:red:`pyopenms.MSSpectrum`): A single spectrum object from an MZML file.

    :green:`**Returns:**`
    - :bold:`dict`: A dictionary containing the processed spectrum data with keys `MW`, `RT`, `Num Peaks`, and `Peaks`.

:brown:`**read_mgf_file(filename)**`

    :blue:`Reads an MGF file and returns a list of spectra data.`

    :green:`**Parameters:**`
    - :bold:`filename` (:red:`str`): The path to the MGF file.

    :green:`**Returns:**`
    - :bold:`list`: A list of dictionaries, each containing `mz_values`, `intensities`, `MW`, and `RT` for a spectrum.

:brown:`**read_mzml_file(filename)**`

    :blue:`Reads an MZML file and returns a list of processed spectrum data.`

    :green:`**Parameters:**`
    - :bold:`filename` (:red:`str`): The path to the MZML file.

    :green:`**Returns:**`
    - :bold:`list`: A list of dictionaries containing processed spectrum data.

:brown:`**read_ms_file(filename)**`

    :blue:`Determines the file format and calls the appropriate function to read the mass spectrometry file.`

    :green:`**Parameters:**`
    - :bold:`filename` (:red:`str`): The path to the mass spectrometry file.

    :green:`**Returns:**`
    - :bold:`pandas.DataFrame` or :bold:`list`: Depending on the file format, returns either a DataFrame or a list of dictionaries.

Grouping MS1 Module
===================

:blue:`This module provides functions for grouping MS1 peptides based on mass-to-charge ratio (m/z) and indexed retention time (iRT) using k-d tree data structures and tolerance calculations.`

Functions
=========

:brown:`**make_data_compatible(index_df)**`

    :blue:`Converts a DataFrame into a list of tuples compatible with further processing.`

    :green:`**Parameters:**`
    - :bold:`index_df` (:red:`pandas.DataFrame`): DataFrame containing the mass spectrometry data with columns `MW` (m/z) and `iRT`.

    :green:`**Returns:**`
    - :bold:`list`: A list of tuples in the format `(index, MW, iRT)`.

:brown:`**within_ppm(pair, ppm_tolerance1, ppm_tolerance2)**`

    :blue:`Checks if two peptide pairs are within a specified ppm (parts per million) tolerance for m/z and absolute tolerance for iRT.`

    :green:`**Parameters:**`
    - :bold:`pair` (:red:`tuple`): A tuple containing two peptide tuples in the format `((index1, MW1, iRT1), (index2, MW2, iRT2))`.
    - :bold:`ppm_tolerance1` (:red:`float`): The ppm tolerance for the m/z values.
    - :bold:`ppm_tolerance2` (:red:`float`): The absolute tolerance for the iRT values.

    :green:`**Returns:**`
    - :bold:`bool`: True if the pair is within the specified tolerances, False otherwise.

:brown:`**within_tolerance(pair, tolerance1, tolerance2)**`

    :blue:`Checks if two peptide pairs are within specified absolute tolerances for both m/z and iRT.`

    :green:`**Parameters:**`
    - :bold:`pair` (:red:`tuple`): A tuple containing two peptide tuples in the format `((index1, MW1, iRT1), (index2, MW2, iRT2))`.
    - :bold:`tolerance1` (:red:`float`): The absolute tolerance for the m/z values.
    - :bold:`tolerance2` (:red:`float`): The absolute tolerance for the iRT values.

    :green:`**Returns:**`
    - :bold:`bool`: True if the pair is within the specified tolerances, False otherwise.

:brown:`**find_combinations_kdtree(data, tolerance1, tolerance2, use_ppm=True)**`

    :blue:`Finds valid peptide combinations within specified tolerances using a k-d tree for efficient querying.`

    :green:`**Parameters:**`
    - :bold:`data` (:red:`list`): A list of tuples containing peptide data in the format `(index, MW, iRT)`.
    - :bold:`tolerance1` (:red:`float`): The tolerance for the m/z values.
    - :bold:`tolerance2` (:red:`float`): The tolerance for the iRT values.
    - :bold:`use_ppm` (:red:`bool`): If True, use ppm tolerance for m/z values; otherwise, use absolute tolerance.

    :green:`**Returns:**`
    - :bold:`list`: A list of valid peptide pairs within the specified tolerances.

:brown:`**process_peptide_combinations(mz_irt_df, tolerance1, tolerance2, use_ppm=True)**`

    :blue:`Processes peptide combinations from the mass spectrometry data, finding valid pairs within specified tolerances.`

    :green:`**Parameters:**`
    - :bold:`mz_irt_df` (:red:`pandas.DataFrame`): DataFrame containing peptide data with columns `Name`, `MW`, and `iRT`.
    - :bold:`tolerance1` (:red:`float`): The tolerance for the m/z values.
    - :bold:`tolerance2` (:red:`float`): The tolerance for the iRT values.
    - :bold:`use_ppm` (:red:`bool`): If True, use ppm tolerance for m/z values; otherwise, use absolute tolerance.

    :green:`**Returns:**`
    - :bold:`pandas.DataFrame`: A DataFrame containing the resulting valid peptide pairs with their indices, names, m/z values, and iRT values.

Similarity Module
=================

:blue:`This module provides functions and classes to calculate similarity between mass spectrometry spectra using various methods such as dot product, spectral angle, and cosine similarity.`

Functions and Classes
=====================

:brown:`**ndotproduct(x, y, m=0, n=0.5, na_rm=True)**`

    :blue:`Calculates the normalized dot product between two spectra.`

    :green:`**Parameters:**`
    - :bold:`x` (:red:`pandas.DataFrame`): DataFrame containing the first spectrum with columns for m/z and intensities.
    - :bold:`y` (:red:`pandas.DataFrame`): DataFrame containing the second spectrum with columns for m/z and intensities.
    - :bold:`m` (:red:`float`): Exponent for the m/z values in the weight calculation. Default is 0.
    - :bold:`n` (:red:`float`): Exponent for the intensity values in the weight calculation. Default is 0.5.
    - :bold:`na_rm` (:red:`bool`): If True, removes missing values (not used in current implementation). Default is True.

    :green:`**Returns:**`
    - :bold:`float`: The normalized dot product between the two spectra.

:brown:`**nspectraangle(x, y, m=0, n=0.5, na_rm=True)**`

    :blue:`Calculates the normalized spectral angle between two spectra.`

    :green:`**Parameters:**`
    - :bold:`x` (:red:`pandas.DataFrame`): DataFrame containing the first spectrum with columns for m/z and intensities.
    - :bold:`y` (:red:`pandas.DataFrame`): DataFrame containing the second spectrum with columns for m/z and intensities.
    - :bold:`m` (:red:`float`): Exponent for the m/z values in the weight calculation. Default is 0.
    - :bold:`n` (:red:`float`): Exponent for the intensity values in the weight calculation. Default is 0.5.
    - :bold:`na_rm` (:red:`bool`): If True, removes missing values (not used in current implementation). Default is True.

    :green:`**Returns:**`
    - :bold:`float`: The normalized spectral angle between the two spectra.

:brown:`**joinPeaks(tolerance=0, ppm=0)**`

    :blue:`A class to join peaks from two spectra based on m/z and intensity values using tolerance and ppm values.`

    :green:`**Parameters:**`
    - :bold:`tolerance` (:red:`float`): Absolute tolerance for matching m/z values. Default is 0.
    - :bold:`ppm` (:red:`float`): Parts per million (ppm) tolerance for matching m/z values. Default is 0.

    :green:`**Methods:**`

    - **match(x, y)**:
        :blue:`Matches peaks from two spectra based on the specified tolerance and ppm values.`

        :green:`**Parameters:**`
        - :bold:`x` (:red:`pandas.DataFrame`): DataFrame containing the first spectrum with columns for m/z and intensities.
        - :bold:`y` (:red:`pandas.DataFrame`): DataFrame containing the second spectrum with columns for m/z and intensities.

        :green:`**Returns:**`
        - :bold:`tuple`: Two DataFrames containing the matched peaks from `x` and `y`.

:brown:`**process_spectra_pairs(chunk, spectra, mz_irt_df, tolerance=0, ppm=0, m=0, n=0.5)**`

    :blue:`Processes pairs of spectra and calculates the similarity score using the spectral angle method.`

    :green:`**Parameters:**`
    - :bold:`chunk` (:red:`list`): List of index pairs to process.
    - :bold:`spectra` (:red:`list`): List of spectra objects.
    - :bold:`mz_irt_df` (:red:`pandas.DataFrame`): DataFrame containing peptide data with columns `Name`, `MW`, and `iRT`.
    - :bold:`tolerance` (:red:`float`): Absolute tolerance for m/z matching. Default is 0.
    - :bold:`ppm` (:red:`float`): Parts per million (ppm) tolerance for m/z matching. Default is 0.
    - :bold:`m` (:red:`float`): Exponent for the m/z values in the weight calculation. Default is 0.
    - :bold:`n` (:red:`float`): Exponent for the intensity values in the weight calculation. Default is 0.5.

    :green:`**Returns:**`
    - :bold:`pandas.DataFrame`: A DataFrame containing the similarity scores for the processed spectra pairs.

:brown:`**process_spectra_pairs_cosine(chunk, spectra, mz_irt_df, tolerance=0)**`

    :blue:`Processes pairs of spectra and calculates the similarity score using the CosineGreedy method.`

    :green:`**Parameters:**`
    - :bold:`chunk` (:red:`list`): List of index pairs to process.
    - :bold:`spectra` (:red:`list`): List of spectra objects.
    - :bold:`mz_irt_df` (:red:`pandas.DataFrame`): DataFrame containing peptide data with columns `Name`, `MW`, and `iRT`.
    - :bold:`tolerance` (:red:`float`): Tolerance for m/z matching in the CosineGreedy method. Default is 0.

    :green:`**Returns:**`
    - :bold:`pandas.DataFrame`: A DataFrame containing the similarity scores for the processed spectra pairs.

Mutation Module
===============

:blue:`This module provides tools for processing proteins by simulating peptide digestion and introducing mutations based on input data. The primary class, `ProteinMutator`, handles the loading, processing, and mutation of proteins.`

Classes and Functions
=====================

:brown:`**ProteinMutator(proteome_file, mutations_file, output_dir, digestion_method)**`

    :blue:`A class for handling protein mutations and peptide generation based on a provided proteome and mutation data.`

    :green:`**Parameters:**`
    - :bold:`proteome_file` (:red:`str`): Path to the FASTA file containing the proteome sequences.
    - :bold:`mutations_file` (:red:`str`): Path to the TSV file containing mutation data.
    - :bold:`output_dir` (:red:`str`): Directory where output files (peptides and mutated peptides) will be saved.
    - :bold:`digestion_method` (:red:`callable`): A function that takes a protein sequence and returns a list of peptides.

    :green:`**Methods:**`

    - **load_proteome()**:
        :blue:`Loads the proteome sequences from the FASTA file into memory.`

    - **load_mutations()**:
        :blue:`Loads the mutation data from the TSV file into a DataFrame.`

    - **process_protein(target_protein_accession)**:
        :blue:`Processes a single protein by digesting it into peptides and applying mutations based on the mutation data.`

        :green:`**Parameters:**`
        - :bold:`target_protein_accession` (:red:`str`): The accession number of the target protein to be processed.

    - **process_all_proteins()**:
        :blue:`Processes all proteins in the loaded proteome, applying digestion and mutation steps for each.`

:brown:`**tryptic_digest(sequence)**`

    :blue:`Simulates the tryptic digestion of a protein sequence.`

    :green:`**Parameters:**`
    - :bold:`sequence` (:red:`str`): The protein sequence to be digested.

    :green:`**Returns:**`
    - :bold:`list`: A list of peptides resulting from the tryptic digestion.

Example Usage
=============

The following example demonstrates how to use various modules in the MSCI package to process mass spectrometry data, group peptides, and calculate similarity scores:

.. code-block:: python

    from MSCI.Preprocessing.Koina import PeptideProcessor
    from MSCI.Grouping_MS1.Grouping_mw_irt import process_peptide_combinations
    from MSCI.Preprocessing.read_msp_file import read_msp_file
    from MSCI.Similarity.spectral_angle_similarity import process_spectra_pairs
    from MSCI.data.digest import parse_fasta_and_digest, tryptic_digest, peptides_to_csv
    from matchms.importing import load_from_msp
    import random
    import numpy as np
    import pandas as pd
    
    # Parse FASTA file and perform tryptic digestion
    result = parse_fasta_and_digest("/content/sp_human_2023_04.fasta", digest_type="trypsin")
    peptides_to_csv(result, "random_tryptic_peptides.txt")
    
    # Initialize and process peptides using PeptideProcessor
    processor = PeptideProcessor(
        input_file="random_tryptic_peptides.txt",
        collision_energy=30,
        charge=2,
        model_intensity="Prosit_2020_intensity_HCD",
        model_irt="Prosit_2019_irt"
    )
    processor.process('random_tryptic_peptides.msp')
    
    # Load spectra from MSP file
    File = 'random_tryptic_peptides.msp'
    spectra = list(load_from_msp(File))
    mz_tolerance = 1
    irt_tolerance = 5
    
    # Read MSP file and group peptides
    mz_irt_df = read_msp_file(File)
    Groups_df = process_peptide_combinations(mz_irt_df, mz_tolerance, irt_tolerance, use_ppm=False)
    
    # Process similarity pairs and save results
    Groups_df.columns = Groups_df.columns.str.strip()
    index_array = Groups_df[['index1','index2']].values.astype(int)
    result = process_spectra_pairs(index_array, spectra, mz_irt_df, tolerance=0, ppm=10)
    result.to_csv("output.csv", index=False)
    
    # Plot and compare spectra
    import matplotlib.pyplot as plt
    print(mz_irt_df.iloc[19])
    print(mz_irt_df.iloc[36])
    spectra[19].plot_against(spectra[36])
    plt.savefig('spectra_comparison.png')
