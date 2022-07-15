import pandas as pd 
import re
import itertools

def fix_na(df):

    if df['Item_total'].isnull().values.any():
        df_fix = fix_df(df)
        print("DF id fixed")
        print(df_fix)
    else:
        df_fix = df

    df_pd = df_fix[df_fix['Product_model'].notnull()]
    descriptions = df_pd['Product_model']
    desc_str = ""
    for description in descriptions:
        desc_str +=  description
        # print(desc_str)
        # print("*****************")
    re_pattern = patterns(df['Vendor_name'])
    if re_pattern != 'NA':
        models = re.findall(re_pattern,desc_str)
        print(models)
        print(len(df_fix))
        if len(models) == len(df_fix):
            df_fix['Product_model'] = models
            print("Code is working")
            print(df_fix)
        
    return df_fix

def fix_df(df):
    qty = list(df[df['Qty'].notnull()]['Qty'])
    unit_p = list(df[df['Unit_price'].notnull()]['Unit_price'])
    item_tot = list(df[df['Item_total'].notnull()]['Item_total'])
    conf = list(df[df['Item_total'].notnull()]['Confidence'])
    low_conf = list(df[df['Item_total'].notnull()]['low_conf_fields'])
    prod_model = list(df[df['Product_model'].notnull()]['Product_model'])

    print(qty)
    print(unit_p)
    print(item_tot)
    print(prod_model)
    
    nest = [prod_model,qty,unit_p,item_tot,conf,low_conf]
    df_fix = pd.DataFrame((_ for _ in itertools.zip_longest(*nest)), columns=['Product_model','Qty','Unit_price','Item_total','Confidence','low_conf_fields'])
    df_fix[['Vendor_name','Invoice_no','Invoice_date','Invoice_total']] = df[['Vendor_name','Invoice_no','Invoice_date','Invoice_total']]
    print("--------------------")
    print(df_fix)
    return df_fix

def patterns(vname):
    if "VESTEL" in vname[0]:
        re_pattern = 'MODEL\:\s(.*)'

    else:
        re_pattern = 'NA'

    return re_pattern