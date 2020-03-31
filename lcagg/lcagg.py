import glob
import os
import re

import numpy as np 
import pandas as pd

print('new loaded')

class LcCsv(object):
    def __init__(self, h5file, ):
        self.store = pd.HDFStore(h5file)

    def folder_proc(self, folder, sample_str='\d+-\d+-(\w+\d+_\d+\w?)_'):
        # Pull the appropriate sample name from the full file name. This will
        # be specific to different users/data sets
        # The default finds sample names that are like `abcd####_###` 
        srch = re.compile(sample_str)
        # Search string to find wavelengths
        srch2 = re.compile('Sig=(\d+),')

        # Glob searches for patterns. We want it to be recursive (go through
        # all folders) the '**' means that it will go through all folders. The
        # '*.csv' is going to look for files that end in '.csv'
        for fpath in glob.glob(folder + r'\**\*.csv', recursive=True):
            fname = os.path.basename(fpath)
            
            # If the filename matches either of these types, they will be
            # processed, but the "base" for saving in the HDF file will be
            # different
            if 'blank' in fname or 'DAD' in fname:
                continue
            elif 'Integration' in fname:
                base = '/int'
            elif 'Signal' in fname:
                base = '/sig'
            else:
                # Ignore all other CSV files
                continue 
            
            # Get the sample name from the larger file name
            match = srch.search(fname)
            try:
                smpl_name = match.group(1)
            except:
                mssg = "There is a problem with filename: "
                raise ValueError(mssg + fname)

            # Find the wavelength value from the first line of the file
            with open(fpath, encoding='UTF16') as f:
                firstline = f.readline() 
            match2 = srch2.search(firstline)
            wl = match2.group(1)
           
            # Hopefully unique path for the data
            path = smpl_name + base + wl
            # Ignore data that is already there. This could be a problem if
            # there are two files with the same expt name
            if path not in self.store:
#                print('Adding:', path)
                # Put the chromatogram into storage
                df = pd.read_csv(fpath, header=1, encoding='UTF16')
                # Remove start/end whitespace from column names
                df.rename(columns=lambda x: x.strip(), inplace=True)
                self.store[path] = df
#            else:
#                print('Skipping:', path)

    def select(self, specs, data_type='signal', wl=315):
        if isinstance(specs, str):
            specs = [specs]

        if data_type == 'signal':
            sep = '/sig'
        elif data_type == 'ints':
            sep = '/int'
        else:
            raise ValueError("Data type isn't recognized.")

        try:
            wl = str(wl)
        except:
            raise ValueError("Something is wrong with your wavelength"\
                    " selection.")

        suffix = sep + wl
        dfs = {spec+suffix:self.store[spec+suffix] for spec in specs}
        dfs = pd.concat(dfs, axis=0)
        dfs.index.set_names(['Spec', 'idx'], inplace=True)
        return dfs

    def update_table(self, specs, utype='area%'):
        # Get DFs if specs 
        if utype == 'area%':
            gb = specs.groupby('Spec')
            for spec, df in gb:
                ap = self._area_per(df)
                specs.loc[ap.index, 'Area %'] = ap
            
    def _area_per(self, df):
        tot_area = df['Area'].sum()
        area_per = df[['Area']]*100/tot_area
        return area_per.rename({'Area': 'Area %'}, axis=1)

    def close(self,):
        self.store.close()
        
    def __contains__(self, item):
        return item in self.store

