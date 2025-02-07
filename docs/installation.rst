Installation Guide
==================

This guide will help you install the MSCI package and its dependencies.

Installing MSCI via pip
-----------------------
You can install MSCI directly using pip, which will also handle the necessary dependencies.

.. code-block:: bash

    pip install MSCI==0.2.0

If you're working in a Jupyter notebook or a Colab environment, you may need to adjust the Python path to include the MSCI module:

.. code-block:: python

    import sys
    sys.path.append('/path/to/MSCI')


**Note**: If you already have `matchms` installed and your environment prompts you to restart the session, select 'Cancel' to avoid any disruptions.

Clone the Repository
--------------------
If you prefer to work with the latest functions directly from the repository, you can clone it using the following command:

.. code-block:: bash

    git clone https://github.com/proteomicsunitcrg/MSCI.git
After cloning the repository, navigate to the MSCI directory:

.. code-block:: bash

    cd MSCI

This step ensures that you are in the correct directory before running any scripts or modules from the MSCI package.

Conclusion
----------
Once installed, you can start using the MSCI package to process mass spectrometry data, perform peptide grouping, and calculate similarity scores.
