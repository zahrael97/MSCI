import requests
import pandas as pd
import re
from itertools import combinations
import streamlit as st
import time
# Existing masses and modifications
PARTICLE_MASSES = {"PROTON": 1.007276467, "ELECTRON": 0.00054858}

ATOM_MASSES = {
    "H": 1.007825035,
    "C": 12.0,
    "O": 15.9949146,
    "N": 14.003074,
}

MASSES = {**PARTICLE_MASSES, **ATOM_MASSES}
MASSES["N_TERMINUS"] = MASSES["H"]
MASSES["C_TERMINUS"] = MASSES["O"] + MASSES["H"]

AA_MASSES = {
    "A": 71.037114,
    "R": 156.101111,
    "N": 114.042927,
    "D": 115.026943,
    "C": 103.009185,
    "E": 129.042593,
    "Q": 128.058578,
    "G": 57.021464,
    "H": 137.058912,
    "I": 113.084064,
    "L": 113.084064,
    "K": 128.094963,
    "M": 131.040485,
    "F": 147.068414,
    "P": 97.052764,
    "S": 87.032028,
    "T": 101.047679,
    "U": 150.95363,
    "W": 186.079313,
    "Y": 163.063329,
    "V": 99.068414,
    "[]-": MASSES["N_TERMINUS"],
    "-[]": MASSES["C_TERMINUS"],
}

MOD_MASSES = {
    "[UNIMOD:737]": 229.162932,  # TMT_6
    "[UNIMOD:2016]": 304.207146,  # TMT_PRO
    "[UNIMOD:214]": 144.102063,  # iTRAQ4
    "[UNIMOD:730]": 304.205360,  # iTRAQ8
    "[UNIMOD:259]": 8.014199,  # SILAC Lysine
    "[UNIMOD:267]": 10.008269,  # SILAC Arginine
    "[]": 0.0,
    "[UNIMOD:1]": 42.010565,  # Acetylation
    "[UNIMOD:1896]": 158.003765,  # DSSO-crosslinker
    "[UNIMOD:1881]": 54.010565,  # Alkene short fragment of DSSO-crosslinker
    "[UNIMOD:1882]": 85.982635,  # Thiol long fragment of DSSO-crosslinker
    "[UNIMOD:1884]": 196.084792,  # BuUrBu (DSBU)-crosslinker
    "[UNIMOD:1885]": 111.032028,  # BuUr long fragment of BuUrBu (DSBU)-crosslinker
    "[UNIMOD:1886]": 85.052764,  # Bu short fragment of BuUrBu (DSBU)-crosslinker
    "[UNIMOD:1898]": 138.068080,  # DSS and BS3 non-cleavable crosslinker
    "[UNIMOD:122]": 27.994915,  # Formylation
    "[UNIMOD:1289]": 70.041865,  # Butyrylation
    "[UNIMOD:1363]": 68.026215,  # Crotonylation
    "[UNIMOD:1848]": 114.031694,  # Glutarylation
    "[UNIMOD:1914]": -32.008456,  # Oxidation and then loss of oxidized M side chain
    "[UNIMOD:2]": -0.984016,  # Amidation
    "[UNIMOD:21]": 79.966331,  # Phosphorylation
    "[UNIMOD:213]": 541.06111,  # ADP-ribosylation
    "[UNIMOD:23]": -18.010565,  # Water Loss
    "[UNIMOD:24]": 71.037114,  # Propionamidation
    "[UNIMOD:354]": 44.985078,  # Nitrosylation
    "[UNIMOD:28]": -17.026549,  # Glu to PyroGlu
    "[UNIMOD:280]": 28.0313,  # Ethylation
    "[UNIMOD:299]": 43.989829,  # Carboxylation
    "[UNIMOD:3]": 226.077598,  # Biotinylation
    "[UNIMOD:34]": 14.01565,  # Methylation
    "[UNIMOD:345]": 47.984744,  # Trioxidation
    "[UNIMOD:35]": 15.994915,  # Hydroxylation
    "[UNIMOD:351]": 3.994915,  # Oxidation to Kynurenine
    "[UNIMOD:36]": 28.0313,  # Dimethylation
    "[UNIMOD:360]": -30.010565,  # Pyrrolidinone
    "[UNIMOD:368]": -33.987721,  # Dehydroalanine
    "[UNIMOD:37]": 42.04695,  # Trimethylation
    "[UNIMOD:385]": -17.026549,  # Ammonia loss
    "[UNIMOD:392]": 29.974179,  # Quinone
    "[UNIMOD:4]": 57.021464,  # Carbamidomethyl
    "[UNIMOD:40]": 79.956815,  # Sulfonation
    "[UNIMOD:401]": -2.01565,  # Didehydro
    "[UNIMOD:425]": 31.989829,  # Dioxidation
    "[UNIMOD:43]": 203.079373,  # HexNAc
    "[UNIMOD:44]": 204.187801,  # Farnesylation
    "[UNIMOD:447]": -15.994915,  # Reduction
    "[UNIMOD:46]": 229.014009,  # Pyridoxal phosphate
    "[UNIMOD:47]": 238.229666,  # Palmitoylation
    "[UNIMOD:5]": 43.005814,  # Carbamyl
    "[UNIMOD:58]": 56.026215,  # Propionylation
    "[UNIMOD:6]": 58.005479,  # Carboxymethylation
    "[UNIMOD:64]": 100.016044,  # Succinylation
    "[UNIMOD:7]": 0.984016,  # Deamidation
    "[UNIMOD:747]": 86.000394,  # Malonylation
}

# These are only used for specific applications
AA_MOD_MASSES = {
    "K[UNIMOD:737]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:737]"],
    "M[UNIMOD:35]": AA_MASSES["M"] + MOD_MASSES["[UNIMOD:35]"],
    "C[UNIMOD:4]": AA_MASSES["C"] + MOD_MASSES["[UNIMOD:4]"],
    "K[UNIMOD:2016]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:2016]"],
    "K[UNIMOD:214]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:214]"],
    "K[UNIMOD:730]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:730]"],
    "S[UNIMOD:21]": AA_MASSES["S"] + MOD_MASSES["[UNIMOD:21]"],
    "T[UNIMOD:21]": AA_MASSES["T"] + MOD_MASSES["[UNIMOD:21]"],
    "Y[UNIMOD:21]": AA_MASSES["Y"] + MOD_MASSES["[UNIMOD:21]"],
    "S[UNIMOD:23]": AA_MASSES["S"],  # + MOD_MASSES['[UNIMOD:23]'],
    "T[UNIMOD:23]": AA_MASSES["T"],  # + MOD_MASSES['[UNIMOD:23]'],
    "Y[UNIMOD:23]": AA_MASSES["Y"],  # + MOD_MASSES['[UNIMOD:23]'],
    "K[UNIMOD:1896]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:1896]"],
    "K[UNIMOD:1881]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:1881]"],
    "K[UNIMOD:1882]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:1882]"],
    "K[UNIMOD:1884]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:1884]"],
    "K[UNIMOD:1885]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:1885]"],
    "K[UNIMOD:1886]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:1886]"],
    "K[UNIMOD:1898]": AA_MASSES["K"] + MOD_MASSES["[UNIMOD:1898]"],
    "[UNIMOD:1]-": MASSES["N_TERMINUS"] + MOD_MASSES["[UNIMOD:1]"],
    "K[UNIMOD:259]": AA_MASSES["K"],  # + MOD_MASSES['[UNIMOD:259]'],
    # To make vecMZ work
    "R[UNIMOD:267]": AA_MASSES["R"],  # + MOD_MASSES['[UNIMOD:267]']
}

AA_MOD = {**AA_MASSES, **AA_MOD_MASSES}

import re

import re
import requests
import pandas as pd
import requests
import re
import pandas as pd


class PeptideProcessor:
    def __init__(self, input_file, collision_energy, charge, model_intensity, model_irt, instrument_type="QE"):
        self.input_file = input_file
        self.collision_energy = collision_energy
        self.charge = charge
        self.instrument_type = instrument_type
        self.model_intensity = model_intensity
        self.model_irt = model_irt
        self.model_intensity_url = f"https://koina.wilhelmlab.org/v2/models/{model_intensity}/infer"
        self.model_irt_url = f"https://koina.wilhelmlab.org/v2/models/{model_irt}/infer"

    def calculate_peptide_mass(self, peptide_sequence):
        total_mass = MASSES["N_TERMINUS"]
        pattern = re.compile(r'([A-Z])(\[UNIMOD:\d+\])?')

        for match in pattern.finditer(peptide_sequence):
            aa = match.group(1)
            mod = match.group(2)
            
            if aa in AA_MASSES:
                total_mass += AA_MASSES[aa]
                if mod:
                    mod_mass = MOD_MASSES.get(mod, 0.0)
                    total_mass += mod_mass
            else:
                print(f"Unknown amino acid: {aa}")
                return None
        
        total_mass += MASSES["C_TERMINUS"]
        return total_mass

    def get_request_body(self, peptides, model_type):
        if model_type.startswith("Prosit"):
            return {
                "id": "batch_request",
                "inputs": [
                    {
                        "name": "peptide_sequences",
                        "shape": [len(peptides), 1],
                        "datatype": "BYTES",
                        "data": list(peptides)
                    },
                    {
                        "name": "collision_energies",
                        "shape": [len(peptides), 1],
                        "datatype": "FP32",
                        "data": [self.collision_energy] * len(peptides)
                    },
                    {
                        "name": "precursor_charges",
                        "shape": [len(peptides), 1],
                        "datatype": "INT32",
                        "data": [self.charge] * len(peptides)
                    }
                ]
            }
        elif model_type.startswith("ms2pip"):
            return {
                "id": "0",
                "inputs": [
                    {
                        "name": "peptide_sequences",
                        "shape": [len(peptides), 1],
                        "datatype": "BYTES",
                        "data": list(peptides)
                    },
                    {
                        "name": "precursor_charges",
                        "shape": [len(peptides), 1],
                        "datatype": "INT32",
                        "data": [self.charge] * len(peptides)
                    }
                ]
            }
        else:
            raise ValueError("Unsupported model type")

    def get_predictions(self, peptides):
        model_type = self.model_intensity.split("_")[0]  # Determine model type from the name
        request_body = self.get_request_body(peptides, self.model_intensity)

        response = requests.post(self.model_intensity_url, json=request_body)

        if response.status_code == 200:
            predictions = response.json()
            try:
                # Ensuring that intensities and mz_values are float
                intensities = [float(i) for i in predictions['outputs'][2]['data']]
                mz_values = [float(mz) for mz in predictions['outputs'][1]['data']]
            except KeyError:
                return None
            
            num_intensities_per_peptide = len(intensities) // len(peptides)

            rows = []
            for i, peptide in enumerate(peptides):
                peptide_intensities = intensities[i * num_intensities_per_peptide : (i + 1) * num_intensities_per_peptide]
                peptide_mz_values = mz_values[i * num_intensities_per_peptide : (i + 1) * num_intensities_per_peptide]
                
                row = {
                    'peptide_sequence': peptide,
                    'charge': self.charge,
                    'collision_energy': self.collision_energy,
                    'mz_values': peptide_mz_values,
                    'intensities': peptide_intensities
                }
                rows.append(row)
            
            df = pd.DataFrame(rows)
            return df
        else:
            return None

    def get_irt_predictions(self, peptides):
        if not self.model_irt_url:
            return [0.0] * len(peptides)  # Return default iRT value if no model is specified

        request_body = {
            "id": "test_id",
            "inputs": [
                {
                    "name": "peptide_sequences",
                    "shape": [len(peptides), 1],
                    "datatype": "BYTES",
                    "data": peptides
                }
            ]
        }

        response = requests.post(self.model_irt_url, json=request_body)

        if response.status_code == 200:
            predictions = response.json()
            irt_values = predictions['outputs'][0]['data']
            return irt_values
        else:
            return None

    def format_msp(self, peptide, charge, collision_energy, mz_values, intensities, irt):
        mw = self.calculate_peptide_mass(peptide)
        mz = (mw + (charge * 1.007276)) / charge

        # Convert to float to ensure no format issues
        mz = float(mz)
        collision_energy = float(collision_energy)
        irt = float(irt)

        header = f"Name: {peptide}/{charge}\n"
        pepmass = f"MW: {mz:.6f}\n"
        collision_energy_line = f"Collision_energy: {collision_energy:.2f}\n"
        irt_line = f"iRT: {irt:.6f}\n"

        sorted_peaks = sorted(
            (float(mz), float(intensity)) for mz, intensity in zip(mz_values, intensities) if mz != -1.00 and intensity != -1.000000
        )

        num_peaks = len(sorted_peaks)
        peaks_header = f"Num peaks: {num_peaks}\n"

        peaks = ""
        for mz, intensity in sorted_peaks:
            peaks += f"{mz:.2f}\t{intensity:.6f}\n"

        return f"{header}{pepmass}{collision_energy_line}{irt_line}{peaks_header}{peaks}\n"

    def save_to_msp(self, df, file, irt_values):
        for index, row in df.iterrows():
            irt = irt_values[index]
            msp_entry = self.format_msp(row['peptide_sequence'], row['charge'], row['collision_energy'], row['mz_values'], row['intensities'], irt)
            file.write(msp_entry)

    def process(self, output_filename):
        peptides = pd.read_csv(self.input_file, header=None)[0].tolist()
        batch_size = 1000
        total_batches = len(peptides) // batch_size + (1 if len(peptides) % batch_size != 0 else 0)
        progress_bar = st.progress(0)

        with open(output_filename, 'w') as file:
            for i, start in enumerate(range(0, len(peptides), batch_size)):
                batch_peptides = peptides[start:start + batch_size]
                irt_values = self.get_irt_predictions(batch_peptides)
                df = self.get_predictions(batch_peptides)

                if df is not None and irt_values is not None:
                    self.save_to_msp(df, file, irt_values)
                
                progress_bar.progress((i + 1) / total_batches)  # Update progress
                time.sleep(0.1)  # Simulate delay for user experience

        st.success("Processing complete!")
