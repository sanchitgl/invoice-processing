import pandas as pd
import numpy as np

def clean_df(df):
    print(df)
    df = df.dropna(subset=['Product_model', 'Qty','Unit_price', 'Item_total'], how='all')
    if df['Product_model'].str.contains('total|amount', case = False, regex = True).any():
        print("df is not clean")
        print(df.loc[df['Product_model'].str.contains('total|amount', case = False, regex = True)])
        df = df.loc[~df['Product_model'].str.contains('total|amount', case = False, regex = True)]
        
    return df 