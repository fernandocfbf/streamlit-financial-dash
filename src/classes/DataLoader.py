import pandas as pd
import numpy as np

from src.constants.scheme import COLUMNS

class DataLoader():

    def __init__(self, path):
        self.path = path
    
    def load_data(self, generate_category=False):
        dataframe = pd.read_csv(f"{self.path}transaction-history.csv")
        categories = pd.read_csv(f"{self.path}categories.csv")

        #rename columns
        dataframe = dataframe.rename(columns=COLUMNS)

        #drop rows
        dataframe = dataframe[~dataframe['transfer_number'].str.startswith('TRANSFER')]
        dataframe = dataframe.query("origin_currency == 'EUR'")

        #apply transformations
        dataframe['start_date'] = pd.to_datetime(dataframe['start_date'])
        dataframe['end_date'] = pd.to_datetime(dataframe['end_date'])
        dataframe['origin_amount'] = np.where(dataframe['direction'] == 'IN', dataframe['origin_amount'] * -1, dataframe['origin_amount'])
        dataframe['destiny_amount'] = np.where(dataframe['direction'] == 'IN', dataframe['origin_amount'] * -1, dataframe['origin_amount'])

        #merge dataframes
        dataframe = dataframe.merge(categories, how='left', left_on='beneficiary_name', right_on='beneficiary')
        
        #fill missing values
        dataframe['category'] = dataframe['category'].fillna('unknown')
        if generate_category:
            size = len(dataframe)
            dataframe["category"] = np.random.choice(['A', 'B', 'C'], size=size)
        
        return dataframe

    