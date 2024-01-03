API
==========



read_msp_file
---------------------
The function parses .msp files, capturing key parameters - the spectrum name, molecular weight (MW), and index of relative retention time (iRT). The acquired data is structured into a pandas DataFrame.

.. code::

   >>>  from MSCI.Preprocessing import read_msp_file
   >>>  mz_irt_df = read_msp_file(filename)


Arguments:
filename: A string representing the path to the MSP file to be read.


read_mzml_file
---------------------
The function parses .mzml files, capturing key parameters - the spectrum name, molecular weight (MW), and retention time (RT). The acquired data is structured into a pandas DataFrame.

.. code::

   >>>  from MSCI.Preprocessing import read_mzml_file
   >>>  mz_irt_df = read_mzml_file(filename)


Arguments:
filename: A string representing the path to the mzml file to be read.

Grouping_mw_rt 
-----



.. code::

   >>> 


joinPeaks
-----



.. code::

   >>> 

process_combin 
-----



.. code::

   >>> 

tryptic_digestion
-----



.. code::

   >>> 


create_mutated_sequence
-----



.. code::

   >>> 


Generate_hla
---------------------



.. code::

   >>>


