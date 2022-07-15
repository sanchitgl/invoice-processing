#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:36:42 2022

@author: sanchit
"""

import pandas as pd
import re
import itertools
#from entities.fix_product_description import fix_na

df = pd.read_csv('Tracker/Test.csv')

def fix_df(df):
    qty = list(df[df['Qty'].notnull()]['Qty'])
    unit_p = list(df[df['Unit_price'].notnull()]['Unit_price'])
    item_tot = list(df[df['Item_total'].notnull()]['Item_total'])
    conf = list(df[df['Item_total'].notnull()]['Confidence'])
    low_conf = list(df[df['Item_total'].notnull()]['low_conf_fields'])
    prod_model = list(df[df['Product_model'].notnull()]['Product_model'])
    
    nest = [prod_model,qty,unit_p,item_tot,conf,low_conf]
    df_fix = pd.DataFrame((_ for _ in itertools.zip_longest(*nest)), columns=['Product_model','Qty','Unit_price','Item_total','Confidence','low_conf_fields'])
    df_fix[['Vendor_name','Invoice_no','Invoice_date','Item_total']] = df[['Vendor_name','Invoice_no','Invoice_date','Item_total']]
    return df_fix

if df['Product_model'].isnull().values.any():
    if df['Item_total'].isnull().values.any():
        df_fix = fix_df(df)
    else:
        df_fix = df
    df_pd = df_fix[df_fix['Product_model'].notnull()]
    descriptions = df_pd['Product_model']
    desc_str = ""
    for description in descriptions:
        desc_str +=  description
        # print(desc_str)
        # print("*****************")
    re_pattern = 'MODEL\:\s(.*)'
    models = re.findall(re_pattern,desc_str)

    if len(models) == len(df_fix['Product_model']):
        df_fix['Product_model'] = models

    
    print(df_fix)

def patterns (vname):
    if vname.contains("VESTEL HOLLAND"):
        re_pattern = 'MODEL(.)'

    return vname