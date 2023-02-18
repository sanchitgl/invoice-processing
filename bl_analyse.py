import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import re
from entities.fix_product_description import postprocess_model
from utils.clean_Df import clean_df
import json
import datefinder

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
endpoint = "https://invoice-automation.cognitiveservices.azure.com/"
key = "95151a64e6b849939605098c92c04ca5"


def analyze_bl(invoices_st):

    #path_to_sample_documents = os.listdir('Invoices_2')

    df_final = pd.DataFrame()
    errors = []
    #invoice_list = []
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    curr_list = ['USD','EUR','AED', '$']
    for invoice_st in invoices_st:
        try:
            invoice_file = invoice_st.name
            bytes_data = invoice_st.read()
            poller = document_analysis_client.begin_analyze_document(
                "prebuilt-invoice", document=bytes_data, locale="en-US"
            )
            invoices = poller.result()
            digitized_text = invoices.content
            #print(digitized_text)
            DF = pd.DataFrame() 
            for idx, key_pair in enumerate(invoices.key_value_pairs):
                df_keypair = {}
                df = {
                    'filename':None,
                    'B/L_no':None,
                    'Date': None
                }
                if key_pair.key:
                    df_keypair['key'] = key_pair.key.content
                if key_pair.value:
                    df_keypair['value'] = key_pair.value.content

                df_keypair_dict = pd.DataFrame([df_keypair])
                DF = pd.concat([DF,df_keypair_dict], ignore_index=True)
            print(DF)
            DF = DF.dropna()

            # Getting all the values that may be BL number
            bl = list(DF[DF['key'].str.lower().isin(['b/l no.','b\l','b/l no:','bill of lading number'])]['value'])
            print(bl)
            
            # Getting all the values that mey be date
            dates = list(DF[DF['key'].str.lower().isin(['date','place and date of issue', 'place & date of issue', 'date of issue of b/l', 'shipped on board'])]['value'])
            extracted_dates = [next(datefinder.find_dates(string), None) for string in dates if next(datefinder.find_dates(string), None) is not None]
            print(extracted_dates)

            if bl:
                print('bl yes')
                if len(bl) >= 1:
                    df['B/L_no'] = bl[0]

            if extracted_dates:
                if len(extracted_dates) >= 1:
                    df['Date'] = extracted_dates[0]

            df['filename'] = invoice_file
            #print(df)
            df_dict = pd.DataFrame([df])
            #print(df_dict)
            df_final = pd.concat([df_final, df_dict], ignore_index=True)
        except:
            errors.append(invoice_st.name)
    print(df_final)
    df_final = df_final[['filename','B/L_no','Date']]
    #df_bl = df_final[['B/L_no','Date']]
    df_final.to_csv('Tracker/BL_tracker.csv',encoding='utf-8',date_format='%d-%m-%Y')
    print(errors)