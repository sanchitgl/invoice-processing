import pandas as pd 
import re
import itertools

def postprocess_model(df,item_table):
    print("********************")
    if df['Product_model'].isnull().values.any():
        print("HEYYYYYYY")
        DF = fix_na(df,item_table)
    elif df['Product_model'].str.contains('SHARP BRAND MODEL').any():
        DF = fix_na(df,item_table)
        print(DF)
        print("yes too much")
    else:
        DF = df
        print('all good')
    return DF

def fix_na(df,item_table):
    vname = df['Vendor_name'][0]
    # if multiple product description in one row 
    if df['Item_total'].isnull().values.any():
        df_fix = fix_df(df)
        print("DF id fixed")
        print(df_fix)
    else:
        df_fix = df

    if "VESTEL" in vname:
        print('*********************')
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
            #print(len(df_fix))
            if len(models) == len(df_fix):
                df_fix['Product_model'] = models
                print("Code is working")
                #print(df_fix)
            else:
                df_fix['Product_model'] = pd.Series(models)

    # if no product description not picked by the model
    elif "JIANGSU" in vname:
        print('found Jiangsu')
        if df_fix['Product_model'].isnull().all(): 
            print('no product descriptions found')
            item_column = item_table.columns[item_table.eq('SHARP MODEL').any()].values[0]
            item_row = item_table[item_table.eq('SHARP MODEL').any(1)].index.values[0]
            print(item_row)
            print(item_table[item_column])
            print(item_table[item_column][1:])
            descriptions = item_table[item_column][(item_row+1):]
            descriptions = descriptions[descriptions.notnull()]
            #print(df[(ans_column.values[0])][ans_row.index.values[0]:])
            print(descriptions)
            if len(descriptions) == len(df_fix):
                print("df matched")
                df_fix['Product_model'] = descriptions
            else:
                desc_list = ' '.join(descriptions.tolist()).split()
                print(desc_list)
                if len(desc_list) == len(df_fix):
                    df_fix['Product_model'] = desc_list



    return df_fix

def fix_df(df):
    qty = list(df[df['Qty'].notnull()]['Qty'])
    unit_p = list(df[df['Unit_price'].notnull()]['Unit_price'])
    item_tot = list(df[df['Item_total'].notnull()]['Item_total'])
    conf = list(df[df['Item_total'].notnull()]['Confidence'])
    low_conf = list(df[df['Item_total'].notnull()]['low_conf_fields'])
    prod_model = list(df[df['Product_model'].notnull()]['Product_model'])

    #print(qty)
    #print(unit_p)
    #print(item_tot)
    #print(prod_model)
    
    nest = [prod_model,qty,unit_p,item_tot,conf,low_conf]
    df_fix = pd.DataFrame((_ for _ in itertools.zip_longest(*nest)), columns=['Product_model','Qty','Unit_price','Item_total','Confidence','low_conf_fields'])
    df_fix[['filename','Vendor_name','Invoice_no','Invoice_date','Invoice_total','Currency']] = df[['filename','Vendor_name','Invoice_no','Invoice_date','Invoice_total','Currency']]
    #print("--------------------")
    #print(df_fix)
    return df_fix

def patterns(vname):
    if "VESTEL" in vname[0]:
        re_pattern = 'MODEL\:\s([^\s]+)'
    else:
        re_pattern = 'NA'

    return re_pattern