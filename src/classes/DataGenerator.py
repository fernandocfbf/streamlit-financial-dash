import pandas as pd
import numpy as np

class DataGenerator():
    def __init__(self, data_size):
        self.data_size = data_size
    
    def generate_dataframe(self):
        df = pd.DataFrame()
        df['date'] = pd.date_range(start='1/1/2018', periods=self.data_size, freq='D')
        df['category'] = np.random.choice(['A', 'B', 'C'], size=self.data_size)
        df['value'] = np.random.randint(0, 100, size=self.data_size)
        df['refunded'] = np.random.choice([True, False], size=self.data_size)
        return df


