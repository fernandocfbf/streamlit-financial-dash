import pandas as pd
import numpy as np

from src.constants.scheme import COLUMNS

class DataLoader():

    def __init__(self, path):
        self.path = path
        self.dataframe = None
    
    def load_data(self, generate_category=False):
        dataframe = pd.read_csv(f"{self.path}transaction-history.csv")
        categories = pd.read_csv(f"{self.path}categories.csv")
        dataframe = dataframe.rename(columns=COLUMNS)
        dataframe['is_transfer'] = dataframe['transfer_number'].str.startswith('TRANSFER')
        dataframe['balance_conversion'] = dataframe['transfer_number'].str.startswith('BALANCE_TRANSACTION')
        dataframe['start_date'] = pd.to_datetime(dataframe['start_date'])
        dataframe['end_date'] = pd.to_datetime(dataframe['end_date'])
        dataframe['year'] = dataframe['start_date'].dt.year
        dataframe['month'] = dataframe['start_date'].dt.month_name()
        dataframe['day'] = dataframe['start_date'].dt.day
        dataframe = dataframe.merge(categories, how='left', left_on='beneficiary_name', right_on='beneficiary')
        dataframe['category'] = dataframe['category'].fillna('unknown')
        if generate_category:
            size = len(dataframe)
            dataframe["category"] = np.random.choice(['A', 'B', 'C'], size=size)
        dataframe.to_csv(f"{self.path}transaction-history-clean.csv", index=False)
        self.dataframe = dataframe

    def get_card_transactions_dataframe(self):
        card_transactions_dataframe = self.dataframe.query("origin_currency == 'EUR' and is_transfer == False")
        return card_transactions_dataframe
    
    def get_money_in(self):
        money_in_dataframe = self.dataframe.query("(is_transfer == True and direction == 'IN' and destiny_currency == 'EUR') or balance_conversion == True")
        money_in_transactions = money_in_dataframe.query("is_transfer == True")['origin_amount'].sum()
        money_in_balance_conversion = money_in_dataframe.query("balance_conversion == True")['destiny_amount'].sum()
        total_money_in = money_in_transactions + money_in_balance_conversion
        return round(total_money_in, 2)
    
    def get_money_out(self):
        transfer_out_dataframe = self.dataframe.query("is_transfer == True and direction == 'OUT' and destiny_currency == 'EUR'")
        card_out_dataframe = self.dataframe.query("direction == 'OUT' and is_transfer == False")
        money_out = transfer_out_dataframe["destiny_amount"].sum() + card_out_dataframe["origin_amount"].sum()
        return round(money_out, 2)

    