import numpy as np
import pandas as pd 


def ndotproduct(x, y, m=0, n=0.5, na_rm=True):
    wx = _weightxy(x.iloc[:,0], x.iloc[:,1], m, n)
    wy = _weightxy(y.iloc[:,0], y.iloc[:,1], m, n)
    wx2 = wx**2
    wy2 = wy**2
    return (np.sum(wx * wy)**2) / (np.sum(wx2, axis=0) * np.sum(wy2, axis=0))



def nspectraangle(x, y, m=0, n=0.5, na_rm=True):
    return 1 - 2 * np.arccos(ndotproduct(x, y, m, n, na_rm)) / np.pi

def _weightxy(x, y, m=0, n=0.5):
    return x**m * y**n


class joinPeaks:
    def __init__(self, tolerance=0, ppm=10):
        self.tolerance = tolerance
        self.ppm = ppm
        self.mz_index = {}

    def match(self, x, y):
        # Merge dataframes
        self.mz_index = {}
        merged = pd.merge(x, y, on='mz', how='outer', suffixes=('_x', '_y'))
        merged = merged.sort_values('mz')

        # Separate into x and y dataframes
        x = merged[['mz', 'intensities_x']].rename(columns={'intensities_x': 'intensities'})
        y = merged[['mz', 'intensities_y']].rename(columns={'intensities_y': 'intensities'})

        # Replace missing values with NaN
        x.where(pd.notnull(x), None, inplace=True)
        y.where(pd.notnull(y), None, inplace=True)

        # Iterate over each row in the merged dataframe
        indices = []
        for index, row in merged.iterrows():
            # Check if the "m/z" value is within the tolerance of an existing index
            matched = False
            for mz, idx in self.mz_index.items():
                mass_tolerance = (mz * self.ppm * 1e-6) 
                if abs(row['mz'] - mz) <= mass_tolerance:
                    # Assign the same index to both peaks
                    indices.append(idx)
                    matched = True
                    break
            if not matched:
                # Assign a new index to the peak
                new_index = len(self.mz_index)
                self.mz_index[row['mz']] = new_index
                indices.append(new_index)
        self.mz_index.clear()
        # Assign indices to 'index' column in one go
        x['index'] = indices
        y['index'] = indices

        # Remove rows where the index is duplicated and intensity is NaN
        x = x[~(x.duplicated(subset='index', keep=False) & x['intensities'].isna())]
        y = y[~(y.duplicated(subset='index', keep=False) & y['intensities'].isna())]

        # Update m/z values to None where intensity is None
        x['mz'] = np.where(x['intensities'].isna(), None, x['mz'])
        y['mz'] = np.where(y['intensities'].isna(), None, y['mz'])

        # Set index
        x.set_index('index', inplace=True)
        y.set_index('index', inplace=True)
        
        return x, y


def process_combin(pair, spectra, tolerance, ppm):
    matcher = joinPeaks(tolerance=tolerance, ppm=ppm)
    
    # Unpack the pair into individual indices
    x_idx, y_idx = pair
    
    # Extract the data for the two spectra
    x_data = {"mz": spectra[x_idx].peaks.mz, "intensities": spectra[x_idx].peaks.intensities}
    y_data = {"mz": spectra[y_idx].peaks.mz, "intensities": spectra[y_idx].peaks.intensities}
    
    # Convert the data to DataFrames
    x = pd.DataFrame(x_data)
    y = pd.DataFrame(y_data)
    
    # Match the peaks in the two spectra
    x, y = matcher.match(x, y)
    
    # Compute the angle between the two spectra
    angle = nspectraangle(x, y, m=0, n=0.5, na_rm=True)
    print(angle)
    # Create a result dictionary
    # Assuming you have already defined and computed the 'angle' variable

    
    return angle




from functools import partial
def process_combin_wrapper(combin, spectra, tolerance, ppm):
    return process_combin(combin, spectra, tolerance ,ppm)
def saveList(myList,filename):
    # the filename should mention the extension 'npy'
    np.save(filename,myList)
    print("Saved successfully!")
    

def loadList(filename):
    # the filename should mention the extension 'npy'
    tempNumpyArray=np.load(filename, allow_pickle=True)
    return tempNumpyArray.tolist()
