import pandas as pd
import numpy as np
import re

def clean_df(df):
    print(df)
    df = df.dropna(subset=['Product_model', 'Qty','Unit_price', 'Item_total'], how='all')
    if df['Product_model'].str.contains('total|amount', case = False, regex = True).any():
        print("df is not clean")
        print(df.loc[df['Product_model'].str.contains('total|amount', case = False, regex = True)])
        df = df.loc[~df['Product_model'].str.contains('total|amount', case = False, regex = True)]
    try:
        vname = df['Vendor_name'][0]
        if "JIANGSU" in vname:
            df = df.dropna(subset=['Qty','Unit_price', 'Item_total'], how='all')
    except:
        print()

    print(df)
    # try:
    # df['Invoice_date'] = pd.to_datetime(df['Invoice_date'], format='%d/%m/%Y')
    # except:
    #     print()
    print(df)
    # df = df.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True) 
    return df 