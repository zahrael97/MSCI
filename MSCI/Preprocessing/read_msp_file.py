import pandas as pd
def read_msp_file(filename):
    """
This function is designed to parse and extract specific spectral data from an MSP formatted file. 
This function processes the file line-by-line, capturing the name of the spectrum, molecular weight (MW), 
and a comment that contains the iRT value. The function initializes an empty list called spectra to store individual 
spectrum dictionaries. As the function reads through the file, it identifies lines starting with 'Name:', 'MW:', 
and 'Comment:' to extract the relevant data. Once all data for a spectrum is collected, it's appended to the spectra list. 
This process continues until the end of the file. The function then converts the list of dictionaries into pandas DataFrame 
with columns 'Name', 'MW', and 'iRT', which is returned as the final output.

Usage:
df = read_msp_file(filename)

Arguments:
filename: A string representing the path to the MSP file to be read.

Value:
The function returns a pandas DataFrame with columns:
Name: The name of the spectrum.
MW: The molecular weight of the spectrum.
iRT: The iRT value is extracted from the comment section of the spectrum.
This data frame provides a structured representation of the spectra data, making further analysis and processing easier.
"""
    spectra = []
    current_spectrum = {}
    
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith('Name: '):
                if current_spectrum:
                    spectra.append(current_spectrum)
                current_spectrum = {'Name': line.split('Name: ')[1]}
            elif line.startswith('MW: '):
                current_spectrum['MW'] = float(line.split('MW: ')[1])
            elif line.startswith('Comment: '):
                comment = line.split('Comment: ')[1]
                current_spectrum['iRT'] = float(comment.split(' iRT=')[1].split(' ')[0])

    if current_spectrum:
        spectra.append(current_spectrum)

    index_df = pd.DataFrame(spectra, columns=['Name', 'MW', 'iRT'])
    return index_df

