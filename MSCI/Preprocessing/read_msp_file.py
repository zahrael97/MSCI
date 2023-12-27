import pandas as pd
def read_msp_file(filename):
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

