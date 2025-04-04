Example of usage 
======

         MSCI is a Python package designed to evaluate the information content of peptide fragmentation spectra. Our objective was to compute an information-content index for all peptides within a given proteome. This would allow us to devise data acquisition and analysis strategies that generate and prioritize the most informative fragment ions for peptide quantification.

#Download MSCI package and necessary installations

.. code:: python

    #!git clone https://github.com/proteomicsunitcrg/MSCI.git
    #! pip install matchms
    # do not restart session if asked (press cancel matchms since probably you already have matchms installed )
    #%cd MSCI
    #import sys
    #sys.path.append('/content/MSCI')
    

.. code:: python

    ! pip install MSCI==0.2.0
    ! pip install biopython
    ! pip install matchms


.. parsed-literal::

    Collecting MSCI==0.2.0
      Downloading MSCI-0.2.0-py2.py3-none-any.whl.metadata (903 bytes)
    Requirement already satisfied: Click>=7.0 in /usr/local/lib/python3.10/dist-packages (from MSCI==0.2.0) (8.1.7)
    Successfully installed MSCI-0.2.0 gitdb-4.0.11 gitpython-3.1.43 pydeck-0.9.1 smmap-5.0.1 streamlit-1.37.1 tenacity-8.5.0 watchdog-4.0.2
    



.. parsed-literal::

    Requirement already satisfied: biopython in /usr/local/lib/python3.10/dist-packages (1.84)
    Requirement already satisfied: numpy in /usr/local/lib/python3.10/dist-packages (from biopython) (1.26.4)
    Requirement already satisfied: matchms in /usr/local/lib/python3.10/dist-packages (0.27.0)
    Requirement already satisfied: deprecated>=1.2.14 in /usr/local/lib/python3.10/dist-packages (from matchms) (1.2.14)
  
    

Import
------

.. code:: python

    from MSCI.Preprocessing.Koina import PeptideProcessor
    from MSCI.Grouping_MS1.Grouping_mw_irt import process_peptide_combinations
    from MSCI.Preprocessing.read_msp_file import read_msp_file
    from MSCI.Similarity.spectral_angle_similarity import process_spectra_pairs
    from MSCI.data.digest import parse_fasta_and_digest, tryptic_digest, peptides_to_csv
    from matchms.importing import load_from_msp
    import random
    import numpy as np
    import pandas as pd
    

Generate predicted dataset
---------------------------

Parse fasta file
----------------

.. code:: python

    result = parse_fasta_and_digest("https://raw.githubusercontent.com/proteomicsunitcrg/MSCI/refs/heads/main/tutorial/sp_human_2023_04.fasta", digest_type="trypsin")
    peptides_to_csv(result, "random_tryptic_peptides.txt")

Download the list of peptides of interest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import random
    
    # List of standard amino acids
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    
    # Function to generate a single tryptic peptide
    def generate_tryptic_peptide(min_length=8, max_length=20):
        length = random.randint(min_length, max_length - 1)
        peptide = ''.join(random.choices(amino_acids, k=length))
        peptide += random.choice('KR')
        return peptide
    
    # Generate a list of 90 random tryptic peptides
    tryptic_peptides = [generate_tryptic_peptide() for _ in range(90)]
    
    # Generate 5 pairs of peptides that are permutations of each other and print them
    permuted_pairs = []
    for _ in range(5):
        peptide = generate_tryptic_peptide()
        # Ensure the peptide has at least 2 characters to swap
        if len(peptide) < 2:
            continue
        # Select two different positions to swap
        pos1, pos2 = random.sample(range(len(peptide) - 1), 2)
        permuted_peptide_list = list(peptide)
        permuted_peptide_list[pos1], permuted_peptide_list[pos2] = permuted_peptide_list[pos2], permuted_peptide_list[pos1]
        permuted_peptide = ''.join(permuted_peptide_list)
        tryptic_peptides.append(peptide)
        tryptic_peptides.append(permuted_peptide)
        permuted_pairs.append((peptide, permuted_peptide))
    
    # Ensure the last peptide meets the length requirement
    last_peptide_length = random.randint(5, 20)
    last_peptide = ''.join(random.choices(amino_acids, k=last_peptide_length))
    tryptic_peptides[-1] = last_peptide
    
    # Shuffle the list to mix the pairs with the other peptides
    random.shuffle(tryptic_peptides)
    # Save the peptides to a file
    with open('random_tryptic_peptides.txt', 'w') as f:
        for peptide in tryptic_peptides:
            f.write(f"{peptide}\n")
    
    
    print("Generated 100 random tryptic peptides with permutation pairs and saved to 'random_tryptic_peptides.txt'.")
    


.. parsed-literal::

    Generated 100 random tryptic peptides with permutation pairs and saved to 'random_tryptic_peptides.txt'.
    

Predict with Koina
~~~~~~~~~~~~~~~~~~

If available your own list of peptides
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    processor = PeptideProcessor(
        input_file="random_tryptic_peptides.txt",
        collision_energy=30,
        charge=2,
        model_intensity="Prosit_2020_intensity_HCD",
        model_irt="Prosit_2019_irt"
    )
    
    processor.process('random_tryptic_peptides.msp')

Load dataset
============

.. code:: python

    # You can use your own spectra
    File= 'random_tryptic_peptides.msp'
    spectra = list(load_from_msp(File))


.. parsed-literal::

    2024-08-22 13:30:02,993:WARNING:matchms:add_precursor_mz:No precursor_mz found in metadata.


Group within MS1 tolerance
==========================

.. code:: python

    mz_tolerance = 1
    irt_tolerance = 5
    
    
    mz_irt_df = read_msp_file(File)
    Groups_df = process_peptide_combinations(mz_irt_df, mz_tolerance, irt_tolerance, use_ppm=False)
    
    Groups_df


.. parsed-literal::

    Results DataFrame Columns: Index(['index1', 'index2', 'peptide 1', 'peptide 2', 'm/z  1', 'm/z 2',
           'iRT 1', 'iRT 2'],
          dtype='object')
    



.. raw:: html

    
      <div id="df-2695c02b-7a10-4ccf-961d-d22d428dca37" class="colab-df-container">
        <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>index1</th>
          <th>index2</th>
          <th>peptide 1</th>
          <th>peptide 2</th>
          <th>m/z  1</th>
          <th>m/z 2</th>
          <th>iRT 1</th>
          <th>iRT 2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2</td>
          <td>15</td>
          <td>FTCQIAHVCPHFNNPK/2</td>
          <td>IDIDKYGKAISACHPPK/2</td>
          <td>928.440166</td>
          <td>928.490379</td>
          <td>50.206707</td>
          <td>49.247311</td>
        </tr>
        <tr>
          <th>1</th>
          <td>8</td>
          <td>19</td>
          <td>RTNYPMFEYHK/2</td>
          <td>TLPRMTKYYGVR/2</td>
          <td>743.350811</td>
          <td>742.905754</td>
          <td>35.316872</td>
          <td>34.458534</td>
        </tr>
        <tr>
          <th>2</th>
          <td>46</td>
          <td>73</td>
          <td>HQEEAMMFHPLMNKNNTFR/2</td>
          <td>QSAICREAEQTKFNMVSKFR/2</td>
          <td>1188.045732</td>
          <td>1187.093736</td>
          <td>61.910671</td>
          <td>62.716576</td>
        </tr>
      </tbody>
    </table>
    </div>
        <div class="colab-df-buttons">
    
      <div class="colab-df-container">
        <button class="colab-df-convert" onclick="convertToInteractive('df-2695c02b-7a10-4ccf-961d-d22d428dca37')"
                title="Convert this dataframe to an interactive table."
                style="display:none;">
    
      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
        <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
      </svg>
        </button>
    
      <style>
        .colab-df-container {
          display:flex;
          gap: 12px;
        }
    
        .colab-df-convert {
          background-color: #E8F0FE;
          border: none;
          border-radius: 50%;
          cursor: pointer;
          display: none;
          fill: #1967D2;
          height: 32px;
          padding: 0 0 0 0;
          width: 32px;
        }
    
        .colab-df-convert:hover {
          background-color: #E2EBFA;
          box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
          fill: #174EA6;
        }
    
        .colab-df-buttons div {
          margin-bottom: 4px;
        }
    
        [theme=dark] .colab-df-convert {
          background-color: #3B4455;
          fill: #D2E3FC;
        }
    
        [theme=dark] .colab-df-convert:hover {
          background-color: #434B5C;
          box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
          filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
          fill: #FFFFFF;
        }
      </style>
    
        <script>
          const buttonEl =
            document.querySelector('#df-2695c02b-7a10-4ccf-961d-d22d428dca37 button.colab-df-convert');
          buttonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
    
          async function convertToInteractive(key) {
            const element = document.querySelector('#df-2695c02b-7a10-4ccf-961d-d22d428dca37');
            const dataTable =
              await google.colab.kernel.invokeFunction('convertToInteractive',
                                                        [key], {});
            if (!dataTable) return;
    
            const docLinkHtml = 'Like what you see? Visit the ' +
              '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
              + ' to learn more about interactive tables.';
            element.innerHTML = '';
            dataTable['output_type'] = 'display_data';
            await google.colab.output.renderOutput(dataTable, element);
            const docLink = document.createElement('div');
            docLink.innerHTML = docLinkHtml;
            element.appendChild(docLink);
          }
        </script>
      </div>
    
    
    <div id="df-8dc8bfe5-3e83-4a39-8c1f-cdc316d9deae">
      <button class="colab-df-quickchart" onclick="quickchart('df-8dc8bfe5-3e83-4a39-8c1f-cdc316d9deae')"
                title="Suggest charts"
                style="display:none;">
    
    <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
         width="24px">
        <g>
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
        </g>
    </svg>
      </button>
    
    <style>
      .colab-df-quickchart {
          --bg-color: #E8F0FE;
          --fill-color: #1967D2;
          --hover-bg-color: #E2EBFA;
          --hover-fill-color: #174EA6;
          --disabled-fill-color: #AAA;
          --disabled-bg-color: #DDD;
      }
    
      [theme=dark] .colab-df-quickchart {
          --bg-color: #3B4455;
          --fill-color: #D2E3FC;
          --hover-bg-color: #434B5C;
          --hover-fill-color: #FFFFFF;
          --disabled-bg-color: #3B4455;
          --disabled-fill-color: #666;
      }
    
      .colab-df-quickchart {
        background-color: var(--bg-color);
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        fill: var(--fill-color);
        height: 32px;
        padding: 0;
        width: 32px;
      }
    
      .colab-df-quickchart:hover {
        background-color: var(--hover-bg-color);
        box-shadow: 0 1px 2px rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
        fill: var(--button-hover-fill-color);
      }
    
      .colab-df-quickchart-complete:disabled,
      .colab-df-quickchart-complete:disabled:hover {
        background-color: var(--disabled-bg-color);
        fill: var(--disabled-fill-color);
        box-shadow: none;
      }
    
      .colab-df-spinner {
        border: 2px solid var(--fill-color);
        border-color: transparent;
        border-bottom-color: var(--fill-color);
        animation:
          spin 1s steps(1) infinite;
      }
    
      @keyframes spin {
        0% {
          border-color: transparent;
          border-bottom-color: var(--fill-color);
          border-left-color: var(--fill-color);
        }
        20% {
          border-color: transparent;
          border-left-color: var(--fill-color);
          border-top-color: var(--fill-color);
        }
        30% {
          border-color: transparent;
          border-left-color: var(--fill-color);
          border-top-color: var(--fill-color);
          border-right-color: var(--fill-color);
        }
        40% {
          border-color: transparent;
          border-right-color: var(--fill-color);
          border-top-color: var(--fill-color);
        }
        60% {
          border-color: transparent;
          border-right-color: var(--fill-color);
        }
        80% {
          border-color: transparent;
          border-right-color: var(--fill-color);
          border-bottom-color: var(--fill-color);
        }
        90% {
          border-color: transparent;
          border-bottom-color: var(--fill-color);
        }
      }
    </style>
    
      <script>
        async function quickchart(key) {
          const quickchartButtonEl =
            document.querySelector('#' + key + ' button');
          quickchartButtonEl.disabled = true;  // To prevent multiple clicks.
          quickchartButtonEl.classList.add('colab-df-spinner');
          try {
            const charts = await google.colab.kernel.invokeFunction(
                'suggestCharts', [key], {});
          } catch (error) {
            console.error('Error during call to suggestCharts:', error);
          }
          quickchartButtonEl.classList.remove('colab-df-spinner');
          quickchartButtonEl.classList.add('colab-df-quickchart-complete');
        }
        (() => {
          let quickchartButtonEl =
            document.querySelector('#df-8dc8bfe5-3e83-4a39-8c1f-cdc316d9deae button');
          quickchartButtonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
        })();
      </script>
    </div>
    
      <div id="id_aecf6954-58ed-42a1-b3b5-6ce64d3ecf24">
        <style>
          .colab-df-generate {
            background-color: #E8F0FE;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            display: none;
            fill: #1967D2;
            height: 32px;
            padding: 0 0 0 0;
            width: 32px;
          }
    
          .colab-df-generate:hover {
            background-color: #E2EBFA;
            box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
            fill: #174EA6;
          }
    
          [theme=dark] .colab-df-generate {
            background-color: #3B4455;
            fill: #D2E3FC;
          }
    
          [theme=dark] .colab-df-generate:hover {
            background-color: #434B5C;
            box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
            filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
            fill: #FFFFFF;
          }
        </style>
        <button class="colab-df-generate" onclick="generateWithVariable('Groups_df')"
                title="Generate code using this dataframe."
                style="display:none;">
    
      <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
           width="24px">
        <path d="M7,19H8.4L18.45,9,17,7.55,7,17.6ZM5,21V16.75L18.45,3.32a2,2,0,0,1,2.83,0l1.4,1.43a1.91,1.91,0,0,1,.58,1.4,1.91,1.91,0,0,1-.58,1.4L9.25,21ZM18.45,9,17,7.55Zm-12,3A5.31,5.31,0,0,0,4.9,8.1,5.31,5.31,0,0,0,1,6.5,5.31,5.31,0,0,0,4.9,4.9,5.31,5.31,0,0,0,6.5,1,5.31,5.31,0,0,0,8.1,4.9,5.31,5.31,0,0,0,12,6.5,5.46,5.46,0,0,0,6.5,12Z"/>
      </svg>
        </button>
        <script>
          (() => {
          const buttonEl =
            document.querySelector('#id_aecf6954-58ed-42a1-b3b5-6ce64d3ecf24 button.colab-df-generate');
          buttonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
    
          buttonEl.onclick = () => {
            google.colab.notebook.generateWithVariable('Groups_df');
          }
          })();
        </script>
      </div>
    
        </div>
      </div>
    



Calculate similarity within fragment tolerance
==============================================

.. code:: python

    Groups_df.columns = Groups_df.columns.str.strip()
    index_array = Groups_df[['index1','index2']].values.astype(int)
    result = process_spectra_pairs(index_array, spectra,  mz_irt_df, tolerance =0, ppm=10)
    result.to_csv("output.csv", index=False)
    result


.. parsed-literal::

    0.002814877157520823
    0.0
    0.0025644450471453695
    



.. raw:: html

    
      <div id="df-4e34b422-566f-4a48-88be-bd899e950cb7" class="colab-df-container">
        <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>index1</th>
          <th>index2</th>
          <th>peptide 1</th>
          <th>peptide 2</th>
          <th>m/z  1</th>
          <th>m/z 2</th>
          <th>iRT 1</th>
          <th>iRT 2</th>
          <th>similarity_score</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2</td>
          <td>15</td>
          <td>FTCQIAHVCPHFNNPK/2</td>
          <td>IDIDKYGKAISACHPPK/2</td>
          <td>928.440166</td>
          <td>928.490379</td>
          <td>50.206707</td>
          <td>49.247311</td>
          <td>0.002815</td>
        </tr>
        <tr>
          <th>1</th>
          <td>8</td>
          <td>19</td>
          <td>RTNYPMFEYHK/2</td>
          <td>TLPRMTKYYGVR/2</td>
          <td>743.350811</td>
          <td>742.905754</td>
          <td>35.316872</td>
          <td>34.458534</td>
          <td>0.000000</td>
        </tr>
        <tr>
          <th>2</th>
          <td>46</td>
          <td>73</td>
          <td>HQEEAMMFHPLMNKNNTFR/2</td>
          <td>QSAICREAEQTKFNMVSKFR/2</td>
          <td>1188.045732</td>
          <td>1187.093736</td>
          <td>61.910671</td>
          <td>62.716576</td>
          <td>0.002564</td>
        </tr>
      </tbody>
    </table>
    </div>
        <div class="colab-df-buttons">
    
      <div class="colab-df-container">
        <button class="colab-df-convert" onclick="convertToInteractive('df-4e34b422-566f-4a48-88be-bd899e950cb7')"
                title="Convert this dataframe to an interactive table."
                style="display:none;">
    
      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
        <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
      </svg>
        </button>
    
      <style>
        .colab-df-container {
          display:flex;
          gap: 12px;
        }
    
        .colab-df-convert {
          background-color: #E8F0FE;
          border: none;
          border-radius: 50%;
          cursor: pointer;
          display: none;
          fill: #1967D2;
          height: 32px;
          padding: 0 0 0 0;
          width: 32px;
        }
    
        .colab-df-convert:hover {
          background-color: #E2EBFA;
          box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
          fill: #174EA6;
        }
    
        .colab-df-buttons div {
          margin-bottom: 4px;
        }
    
        [theme=dark] .colab-df-convert {
          background-color: #3B4455;
          fill: #D2E3FC;
        }
    
        [theme=dark] .colab-df-convert:hover {
          background-color: #434B5C;
          box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
          filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
          fill: #FFFFFF;
        }
      </style>
    
        <script>
          const buttonEl =
            document.querySelector('#df-4e34b422-566f-4a48-88be-bd899e950cb7 button.colab-df-convert');
          buttonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
    
          async function convertToInteractive(key) {
            const element = document.querySelector('#df-4e34b422-566f-4a48-88be-bd899e950cb7');
            const dataTable =
              await google.colab.kernel.invokeFunction('convertToInteractive',
                                                        [key], {});
            if (!dataTable) return;
    
            const docLinkHtml = 'Like what you see? Visit the ' +
              '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
              + ' to learn more about interactive tables.';
            element.innerHTML = '';
            dataTable['output_type'] = 'display_data';
            await google.colab.output.renderOutput(dataTable, element);
            const docLink = document.createElement('div');
            docLink.innerHTML = docLinkHtml;
            element.appendChild(docLink);
          }
        </script>
      </div>
    
    
    <div id="df-860dd60f-58ca-4e64-85be-7b4f647e8213">
      <button class="colab-df-quickchart" onclick="quickchart('df-860dd60f-58ca-4e64-85be-7b4f647e8213')"
                title="Suggest charts"
                style="display:none;">
    
    <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
         width="24px">
        <g>
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
        </g>
    </svg>
      </button>
    
    <style>
      .colab-df-quickchart {
          --bg-color: #E8F0FE;
          --fill-color: #1967D2;
          --hover-bg-color: #E2EBFA;
          --hover-fill-color: #174EA6;
          --disabled-fill-color: #AAA;
          --disabled-bg-color: #DDD;
      }
    
      [theme=dark] .colab-df-quickchart {
          --bg-color: #3B4455;
          --fill-color: #D2E3FC;
          --hover-bg-color: #434B5C;
          --hover-fill-color: #FFFFFF;
          --disabled-bg-color: #3B4455;
          --disabled-fill-color: #666;
      }
    
      .colab-df-quickchart {
        background-color: var(--bg-color);
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        fill: var(--fill-color);
        height: 32px;
        padding: 0;
        width: 32px;
      }
    
      .colab-df-quickchart:hover {
        background-color: var(--hover-bg-color);
        box-shadow: 0 1px 2px rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
        fill: var(--button-hover-fill-color);
      }
    
      .colab-df-quickchart-complete:disabled,
      .colab-df-quickchart-complete:disabled:hover {
        background-color: var(--disabled-bg-color);
        fill: var(--disabled-fill-color);
        box-shadow: none;
      }
    
      .colab-df-spinner {
        border: 2px solid var(--fill-color);
        border-color: transparent;
        border-bottom-color: var(--fill-color);
        animation:
          spin 1s steps(1) infinite;
      }
    
      @keyframes spin {
        0% {
          border-color: transparent;
          border-bottom-color: var(--fill-color);
          border-left-color: var(--fill-color);
        }
        20% {
          border-color: transparent;
          border-left-color: var(--fill-color);
          border-top-color: var(--fill-color);
        }
        30% {
          border-color: transparent;
          border-left-color: var(--fill-color);
          border-top-color: var(--fill-color);
          border-right-color: var(--fill-color);
        }
        40% {
          border-color: transparent;
          border-right-color: var(--fill-color);
          border-top-color: var(--fill-color);
        }
        60% {
          border-color: transparent;
          border-right-color: var(--fill-color);
        }
        80% {
          border-color: transparent;
          border-right-color: var(--fill-color);
          border-bottom-color: var(--fill-color);
        }
        90% {
          border-color: transparent;
          border-bottom-color: var(--fill-color);
        }
      }
    </style>
    
      <script>
        async function quickchart(key) {
          const quickchartButtonEl =
            document.querySelector('#' + key + ' button');
          quickchartButtonEl.disabled = true;  // To prevent multiple clicks.
          quickchartButtonEl.classList.add('colab-df-spinner');
          try {
            const charts = await google.colab.kernel.invokeFunction(
                'suggestCharts', [key], {});
          } catch (error) {
            console.error('Error during call to suggestCharts:', error);
          }
          quickchartButtonEl.classList.remove('colab-df-spinner');
          quickchartButtonEl.classList.add('colab-df-quickchart-complete');
        }
        (() => {
          let quickchartButtonEl =
            document.querySelector('#df-860dd60f-58ca-4e64-85be-7b4f647e8213 button');
          quickchartButtonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
        })();
      </script>
    </div>
    
      <div id="id_1b57c727-f70a-4635-99e8-9c6ae8ac2f79">
        <style>
          .colab-df-generate {
            background-color: #E8F0FE;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            display: none;
            fill: #1967D2;
            height: 32px;
            padding: 0 0 0 0;
            width: 32px;
          }
    
          .colab-df-generate:hover {
            background-color: #E2EBFA;
            box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
            fill: #174EA6;
          }
    
          [theme=dark] .colab-df-generate {
            background-color: #3B4455;
            fill: #D2E3FC;
          }
    
          [theme=dark] .colab-df-generate:hover {
            background-color: #434B5C;
            box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
            filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
            fill: #FFFFFF;
          }
        </style>
        <button class="colab-df-generate" onclick="generateWithVariable('result')"
                title="Generate code using this dataframe."
                style="display:none;">
    
      <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
           width="24px">
        <path d="M7,19H8.4L18.45,9,17,7.55,7,17.6ZM5,21V16.75L18.45,3.32a2,2,0,0,1,2.83,0l1.4,1.43a1.91,1.91,0,0,1,.58,1.4,1.91,1.91,0,0,1-.58,1.4L9.25,21ZM18.45,9,17,7.55Zm-12,3A5.31,5.31,0,0,0,4.9,8.1,5.31,5.31,0,0,0,1,6.5,5.31,5.31,0,0,0,4.9,4.9,5.31,5.31,0,0,0,6.5,1,5.31,5.31,0,0,0,8.1,4.9,5.31,5.31,0,0,0,12,6.5,5.46,5.46,0,0,0,6.5,12Z"/>
      </svg>
        </button>
        <script>
          (() => {
          const buttonEl =
            document.querySelector('#id_1b57c727-f70a-4635-99e8-9c6ae8ac2f79 button.colab-df-generate');
          buttonEl.style.display =
            google.colab.kernel.accessAllowed ? 'block' : 'none';
    
          buttonEl.onclick = () => {
            google.colab.notebook.generateWithVariable('result');
          }
          })();
        </script>
      </div>
    
        </div>
      </div>
    



Plot results
---------

Plot spectra of interest using matchms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import matplotlib.pyplot as plt
    print(mz_irt_df.iloc[19])
    print(mz_irt_df.iloc[36])
    spectra[19].plot_against(spectra[36])
    plt.savefig('spectra_comparison.png')


.. parsed-literal::

    Name    MRIGTPEPWSTQSDKR/2
    MW              944.970342
    iRT              41.258202
    Name: 19, dtype: object
    Name    QAIMSISYHSCYNMFR/2
    MW              975.936599
    iRT              93.540787
    Name: 36, dtype: object
    



