import os 
import subprocess
import pandas as pd
import sklearn 
from sklearn.ensemble import ExtraTreesRegressor 
from sklearn.preprocessing import StandardScaler 
import pickle 
import numpy as np 

class ExtraTreesModel():
    def __init__(self, pre_trained=True):
        if pre_trained:
            if not os.path.exists('ExtraTreesModel'):
                #set the url and output file name 
                url, output_file = "https://zenodo.org/record/8043236/files/PyBrainage_model2%20%281%29?download=1", "ExtraTreesModel"
                
                # download the model 
                subprocess.run(["wget", "-O", output_file, url])    
            
            #load the model 
            self.model = pickle.load(open('ExtraTreesModel', 'rb'))
        
    def predict(self, ROIs):
        #read in the data
        self.rois = ROIs  

        #get the subject IDs 
        IDs = self.rois.iloc[:, 0] 
        Ages = self.rois.iloc[:, 1]

        #remove the subject ID and age column 
        data = self.rois.iloc[:, 2:]   
        
        # check for missing data
        if data.isnull().values.any() == True:
            raise ValueError('There is missing data in the dataframe')

        inf =  data.isin([np.inf, -np.inf])
        if inf.values.sum() != 0: 
            raise ValueError('There is an infinite value in your dataframe') 

        # check for non-numeric data
        for index, row in enumerate(data.iterrows()):
            if any(isinstance(val, str) for val in row[1].values):
                raise ValueError('There is non-numeric data in the dataframe') 
            
        #pre_process the data 
        sc_X = StandardScaler()

        #pre_process the data 
        try:
            data = sc_X.fit_transform(data)
        except ValueError:
            raise ValueError ('Failing to normalise (StandardScaler) the data. Check the data is in the correct format')


        outputs = []

        try:
            # predict Brainage (apply model to whole array at once)
            outputs = self.model.predict(data)
            
        except:
            print(f"Applying the model to the data at once failed. Moving to apply the model row-by-row (slower).")
            # predict Brainage row-by-row
            for row in range(len(data)):
                try:
                    outputs.append(self.model.predict(data[row].reshape(1, -1))) 
                except:
                    raise ValueError(f'Failed at row {row}')
        print(f"Processed all {len(data)} rows successfully. Moving to returning the results.")


        # Stack the two arrays horizontally
        # stacked = np.column_stack((data, outputs))

        # Convert to a pandas dataframe and add column name
        df2 = pd.DataFrame(outputs) 
        df2.columns = ['BrainAge']

        # Add the subject IDs back in
        df2.insert(0, 'ID', IDs)
        df2.insert(1, 'Age', Ages)

        return df2 
