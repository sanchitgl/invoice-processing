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
endpoint = "https://demo-invoice-processing.cognitiveservices.azure.com/"
key = "18a2d0805de94d5bbb191932c2717365"


def analyze_bl(invoices_st):

    #path_to_sample_documents = os.listdir('Invoices_2')

    df_final = pd.DataFrame()

    #invoice_list = []
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    curr_list = ['USD','EUR','AED', '$']
    for invoice_st in invoices_st:
        
        invoice_file = invoice_st.name
        #print(invoice_file)
        # if invoice_file.endswith('.pdf',".PDF"):
        #path_to_invoice = ("Invoices_2/"+invoice_file)
        #with open(path_to_invoice, "rb") as f:
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
            df = {}
            if key_pair.key:
                # print(
                #             key_pair.key.content
                #         )
                df_keypair['key'] = key_pair.key.content
            if key_pair.value:
                # print(
                #             key_pair.value.content

                #         )
                df_keypair['value'] = key_pair.value.content

            df_keypair_dict = pd.DataFrame([df_keypair])
            DF = pd.concat([DF,df_keypair_dict], ignore_index=True)
        print(DF)
        DF = DF.dropna()
        if DF['key'].str.contains('B/L', case = False, regex = True).any():
            #data[data['subjects'].isin(list2)]
            bl = list(DF[DF['key'].str.lower().isin(['b/l no.','b\l','b/l no:'])]['value'])
            print(bl)
        
        if DF['key'].str.contains('date', case = False, regex = True).any():
            date = list(DF[DF['key'].str.lower().isin(['date','place and date of issue', 'place & date of issue', 'date of issue of b/l', 'shipped on board'])]['value'])
            print(date)

        if len(bl) >= 1:
            df['B/L_no'] = bl[0]

        if len(date) >= 1:
            df['Date'] = list(datefinder.find_dates(date[0]))[0]

        df['filename'] = invoice_file
        #print(df)
        df_dict = pd.DataFrame([df])
        #print(df_dict)
        df_final = pd.concat([df_final, df_dict])
    print(df_final)
    df_final = df_final[['filename','B/L_no','Date']]
    #df_bl = df_final[['B/L_no','Date']]
    df_final.to_csv('Tracker/BL_tracker.csv',encoding = 'utf8')