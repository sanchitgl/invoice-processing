#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:13:52 2022

@author: sanchit
"""

# import libraries
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import re
from entities.fix_product_description import postprocess_model
from utils.clean_Df import clean_df
import json

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
endpoint = "https://demo-invoice-processing.cognitiveservices.azure.com/"
key = "18a2d0805de94d5bbb191932c2717365"

def format_bounding_region(bounding_regions):
    if not bounding_regions:
        return "N/A"
    return ", ".join("Page #{}: {}".format(region.page_number, format_bounding_box(region.bounding_box)) for region in bounding_regions)

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])


def analyze_invoice(invoices_st):

    #path_to_sample_documents = os.listdir('Invoices_2')
    with open('utils/vendor_name_dict.json') as json_file:
        vn_master = json.load(json_file)

    df_invoices = pd.DataFrame()

    # Vendor_Name = []
    # Invoice_Id = []
    # Invoice_Date = []
    # Total = []
    # Subtotal = []
    # Tax = []
    # Product_desc = []
    # Amounts = []
    # Qty = []
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
            #print(poller.result())
        invoices = poller.result()
        digitized_text = invoices.content
        #print(digitized_text)
        DF = pd.DataFrame() 
        #count = 0
        for idx, invoice in enumerate(invoices.documents):   
            print("_______________") 
            for idx, item in enumerate(invoice.fields.get("Items").value):
                #print("item")
                df_item = {} 
                count = 1
                low_conf = []
                intv = 0.5
                vendor_conf, inv_no_conf, invoice_date_conf, invoice_total_conf, item_code_conf, unit_price_conf, item_quantity_conf, amount_conf = 0,0,0,0,0,0,0,0
                df_item['filename'] = invoice_file
                print(df_item['filename'])
                print(invoice_file)
                curr = [currency for currency in curr_list if currency in digitized_text]
                if curr:
                    df_item['Currency'] = " ".join(curr)
                else:
                    df_item['Currency'] = None

                #print("...Item #{}".format(idx + 1))
                item_code = item.value.get("ProductCode")
                item_description = item.value.get("Description")

                if item_code:
                    df_item['Product_model'] = item_code.value
                    item_code_conf = item_code.confidence
                    if item_code_conf <= intv:
                        if item_description:
                            df_item['Product_model'] = item_description.value
                            low_conf.append("Product Model")
                else:
                    if item_description:
                        df_item['Product_model'] = item_description.value
                        item_code_conf = item_description.confidence
                        if item_code_conf <= intv:
                            low_conf.append("Product Model")
                    else:
                        df_item['Product_model'] = None
                        item_code_conf = 0
                        low_conf.append("Product Model")
                    #product += str("Item #{} : ".format(idx + 1))+str(item_description.value) + '\n'

                    #qty += str("Item #{} : ".format(idx + 1))+str(item_quantity.value) + '\n'

                amount = item.value.get("Amount")
                unit_price = item.value.get("UnitPrice")
                item_quantity = item.value.get("Quantity")

                if amount:
                    amt_no = re.search("\d+\.\d+",str(amount.value)).group(0)
                    #print(amt_no)
                    df_item['Item_total'] = amt_no

                    amount_conf = amount.confidence
                    if amount_conf <= intv:
                        low_conf.append("Item Total")

                if item_quantity:
                    print(item_quantity)
                    if item_quantity.value:
                        df_item['Qty'] = item_quantity.value
                    elif item_quantity.content:
                        print(item_quantity.content)
                        try:
                            item_quant_temp = re.match(r'\d+',str(item_quantity.content)).group()
                            df_item['Qty'] = item_quant_temp
                        except:
                            df_item['Qty'] = item_quantity.content
                    item_quantity_conf = item_quantity.confidence
                    if item_quantity_conf <= intv:
                        low_conf.append("Qty")

                if unit_price:
                    unit_price_val = re.search("\d+\.\d+",str(unit_price.value)).group(0)
                    df_item['Unit_price'] = unit_price_val
                    unit_price_conf = unit_price.confidence
                    if unit_price_conf <= intv:
                        low_conf.append("Unit Price")
                else:
                    try:
                        df_item['Unit_price'] =  float(df_item['Item_total'])/float(df_item['Qty'])
                    except:
                        df_item['Unit_price'] = None
                        low_conf.append("Unit Price")                   

                vendor_name = invoice.fields.get("VendorName")
                if vendor_name:
                    df_item['Vendor_name'] = vendor_name.value
                    vendor_conf = vendor_name.confidence
                    #print(vendor_conf)
                    if vendor_conf <= intv:
                        vendor_rec = invoice.fields.get("VendorAddressRecipient")
                        if vendor_rec:
                            df_item['Vendor_name'] = vendor_rec.value
                        else:
                            low_conf.append("Vendor Name")
                else:
                    vendor_rec = invoice.fields.get("VendorAddressRecipient")
                    if vendor_rec:
                        df_item['Vendor_name'] = vendor_rec.value
                    else:
                        df_item['Vendor_name'] = 'NA' 
                #print(df_item['Vendor_name'])          
                df_item['Vendor_name']= df_item['Vendor_name'].split('\n')[0]
                    #Vendor_Name.append(vendor_name.value)
                #print(df_item['Vendor_name'])  


                invoice_id = invoice.fields.get("InvoiceId")
                if invoice_id:
                    df_item['Invoice_no'] = max(invoice_id.value.split())
                    inv_no_conf = invoice_id.confidence
                    if inv_no_conf <= intv:
                        low_conf.append("Invoice No.")
                    #print(inv_no_conf)
                    #Invoice_Id.append(invoice_id.value)

                invoice_date = invoice.fields.get("InvoiceDate")
                if invoice_date:
                    df_item['Invoice_date'] = invoice_date.value
                    invoice_date_conf = invoice_date.confidence
                    if invoice_date_conf <= intv:
                        low_conf.append("Invoice Date")
                    #print(invoice_date_conf)
                    #Invoice_Date.append(invoice_date.value)

                invoice_total = invoice.fields.get("InvoiceTotal")
                if invoice_total:
                    total_no = re.search("\d+\.\d+",str(invoice_total.value)).group(0)
                    df_item['Invoice_total'] = total_no

                    invoice_total_conf = invoice_total.confidence    
                    if invoice_total_conf <= intv:
                        low_conf.append("Invoice Total")   
                    
                
                if not item_quantity:
                    #print('no_qty')
                    if amount and unit_price:
                        df_item['Qty'] = round(float(df_item['Item_total'])/float(df_item['Unit_price']))



                df_item['Confidence'] = (vendor_conf + inv_no_conf +invoice_date_conf + invoice_total_conf + item_code_conf + unit_price_conf + item_quantity_conf + amount_conf)/8
                df_item['low_conf_fields'] = ", ".join(low_conf)
                #print(df_item)

            
                df_item_dict = pd.DataFrame([df_item])
                DF = pd.concat([DF,df_item_dict], ignore_index=True)
                #print(DF)
            df_table = pd.DataFrame()
            for table_idx, table in enumerate(invoices.tables):
                # print(
                #     "Table # {} has {} rows and {} columns".format(
                #         table_idx, table.row_count, table.column_count
                #     )
                # )
                for cell in table.cells:
                    # print(
                    #     "...Cell[{}][{}] has content '{}'".format(
                    #         cell.row_index,
                    #         cell.column_index,
                    #         cell.content,
                    #     )
                    # )
                    df_table.loc[cell.row_index,cell.column_index] = cell.content
                #print(df_table)
                #df_table.to_csv('Tracker/item_df.csv')
                        
                    #DF.to_csv('Tracker/Test.csv')
                    #print(DF['Product_model'])

            DF = postprocess_model(DF,df_table)
            DF = clean_df(DF)
            vn_name = DF['Vendor_name'][0]
            vname_final = [k for k, v in vn_master.items() if vn_name in v]
            #print(vname_final)
            if vname_final:
                DF['Vendor_name'] = pd.Series([vname_final[0] for x in range(len(DF.index))])
            df_invoices = pd.concat([df_invoices,DF], ignore_index=True)
    df_invoices = df_invoices[['filename','Invoice_no','Invoice_date','Vendor_name','Product_model','Qty','Unit_price','Item_total','Invoice_total','Currency','Confidence','low_conf_fields']]
    df_invoices.to_csv('Tracker/Invoice_tracker.csv',encoding = 'utf8')

if __name__ == "__main__":
    analyze_invoice()


