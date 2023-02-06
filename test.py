# import os
# from azure.ai.formrecognizer import DocumentAnalysisClient
# from azure.core.credentials import AzureKeyCredential
import pandas as pd
import re
# from entities.fix_product_description import fix_na

# # set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
# endpoint = "https://invoice-automation.cognitiveservices.azure.com/"
# key = "95151a64e6b849939605098c92c04ca5"

# def format_bounding_region(bounding_regions):
#     if not bounding_regions:
#         return "N/A"
#     return ", ".join("Page #{}: {}".format(region.page_number, format_bounding_box(region.bounding_box)) for region in bounding_regions)

# def format_bounding_box(bounding_box):
#     if not bounding_box:
#         return "N/A"
#     return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])


# def analyze_invoice():

#     path_to_sample_documents = os.listdir('invoices_2')

#     df_invoices = pd.DataFrame()

#     Vendor_Name = []
#     Invoice_Id = []
#     Invoice_Date = []
#     Total = []
#     Subtotal = []
#     Tax = []
#     Product_desc = []
#     Amounts = []
#     Qty = []
#     document_analysis_client = DocumentAnalysisClient(
#         endpoint=endpoint, credential=AzureKeyCredential(key)
#     )
#     for invoice in path_to_sample_documents:
#         print(invoice)
#         # if invoice.endswith('.pdf',".PDF"):

#         path_to_invoice = ("invoices_2/"+invoice)
#         with open(path_to_invoice, "rb") as f:
#             poller = document_analysis_client.begin_analyze_document(
#                 "prebuilt-invoice", document=f, locale="en-US"
#             )
#             #print(poller.result())
#         invoices = poller.result()
    
#         DF = pd.DataFrame() 
#         for idx, invoice in enumerate(invoices.documents):       
#             for idx, item in enumerate(invoice.fields.get("Items").value):
#                 df_item = {} 
#                 count = 1
#                 low_conf = []
#                 intv = 0.7
                
#                 #print("...Item #{}".format(idx + 1))
#                 item_code = item.value.get("ProductCode")
#                 if item_code:
#                     df_item['Product_model'] = item_code.value
#                     item_code_conf = item_code.confidence
#                     if item_code_conf <= intv:
#                         low_conf.append("Product Model")
#                 else:
#                     item_description = item.value.get("Description")
#                     if item_description:
#                         df_item['Product_model'] = item_description.value
#                         item_code_conf = item_description.confidence
#                         if item_code_conf <= intv:
#                             low_conf.append("Product Model")
#                     else:
#                         df_item['Product_model'] = None
#                         item_code_conf = 0
#                         low_conf.append("Product Model")
#                     #product += str("Item #{} : ".format(idx + 1))+str(item_description.value) + '\n'

#                 item_quantity = item.value.get("Quantity")
#                 if item_quantity:
#                     df_item['Qty'] = item_quantity.value
#                     item_quantity_conf = item_quantity.confidence
#                     if item_quantity_conf <= intv:
#                         low_conf.append("Qty")
#                     #qty += str("Item #{} : ".format(idx + 1))+str(item_quantity.value) + '\n'

#                 amount = item.value.get("Amount")
#                 if amount:
#                     amt_no = re.search("\d+\.\d+",str(amount.value)).group(0)
#                     #print(amt_no)
#                     df_item['Item_total'] = amt_no

#                     amount_conf = amount.confidence
#                     if amount_conf <= intv:
#                         low_conf.append("Item Total")

#                 unit_price = item.value.get("UnitPrice")
#                 if unit_price:
#                     unit_price_val = re.search("\d+\.\d+",str(unit_price.value)).group(0)
#                     df_item['Unit_price'] = unit_price_val
#                     unit_price_conf = unit_price.confidence
#                     if unit_price_conf <= intv:
#                         low_conf.append("Unit Price")
#                 else:
#                     try:
#                         df_item['Unit_price'] =  float(df_item['Item_total'])/float(df_item['Qty'])
#                     except:
#                         df_item['Unit_price'] = None
#                         low_conf.append("Unit Price")

#                 vendor_name = invoice.fields.get("VendorName")
#                 if vendor_name:
#                     df_item['Vendor_name'] = vendor_name.value
#                     vendor_conf = vendor_name.confidence
#                     #print(vendor_conf)
#                     if vendor_conf <= intv:
#                         vendor_rec = invoice.fields.get("VendorAddressRecipient")
#                         if vendor_rec:
#                             vendor_rec_conf = vendor_rec.confidence
#                             if vendor_rec_conf >= intv:
#                                 df_item['Vendor_name'] = vendor_rec.value
#                             else:
#                                 low_conf.append("Vendor Name")
#                         else:
#                             low_conf.append("Vendor Name")
#                 else:
#                     vendor_rec = invoice.fields.get("VendorAddressRecipient")
#                     if vendor_rec:
#                         df_item['Vendor_name'] = vendor_rec.value
#                     else:
#                         df_item['Vendor_name'] = 'NA'           

#                     #Vendor_Name.append(vendor_name.value)
                    
#                 invoice_id = invoice.fields.get("InvoiceId")
#                 if invoice_id:
#                     df_item['Invoice_no'] = invoice_id.value
#                     inv_no_conf = invoice_id.confidence
#                     if inv_no_conf <= intv:
#                         low_conf.append("Invoice No.")
#                     #print(inv_no_conf)
#                     #Invoice_Id.append(invoice_id.value)

#                 invoice_date = invoice.fields.get("InvoiceDate")
#                 if invoice_date:
#                     df_item['Invoice_date'] = invoice_date.value
#                     invoice_date_conf = invoice_date.confidence
#                     if invoice_date_conf <= intv:
#                         low_conf.append("Invoice Date")
#                     #print(invoice_date_conf)
#                     #Invoice_Date.append(invoice_date.value)

#                 invoice_total = invoice.fields.get("InvoiceTotal")
#                 if invoice_total:
#                     total_no = re.search("\d+\.\d+",str(invoice_total.value)).group(0)
#                     df_item['Invoice_total'] = total_no

#                     invoice_total_conf = invoice_total.confidence    
#                     if invoice_total_conf <= intv:
#                         low_conf.append("Invoice Total")   
                    
#                 df_item['Confidence'] = (vendor_conf + inv_no_conf +invoice_date_conf + invoice_total_conf + item_code_conf + unit_price_conf + item_quantity_conf + amount_conf)/8
#                 df_item['low_conf_fields'] = ", ".join(low_conf)
#                 #print(df_item)
#                 DF = DF.append(df_item, ignore_index=True)
#                 #print(DF)


#             # #DF.to_csv('Tracker/Test.csv')
#             # #print(DF['Product_model'])
#             # if DF['Product_model'].isnull().values.any():
#             #     print("HEYYYY")
#             #     DF = fix_na(DF)

#             # else:
#             #     print("Didnt work")
#             #     print(DF['Product_model'].isnull().values.any())
#             # #print(DF)

#         df_invoices = df_invoices.append(DF, ignore_index=True)
#     df_invoices = df_invoices[['Invoice_no','Invoice_date','Vendor_name','Product_model','Qty','Unit_price','Item_total','Invoice_total','Confidence','low_conf_fields']]
#     df_invoices.to_csv('Tracker/Invoice_tracker.csv')

# if __name__ == "__main__":
#     analyze_invoice()

# stri = 'MyQ-X-E001/EN MyQ-X-E001/EN'

# print(stri.split('\n'))
df = pd.DataFrame({
    'a':['SHARP BRAND GOODS(SWD-E3TLC-BE3)','asdh45','MODEL: asdh45']
})
# re_pattern = 'MODEL\:\s([^\s]+)'
# for model_value in df[(df['a'].str.contains('MODEL'))].values:
    
# print(df[(df['a'].str.contains('MODEL'))])
# df[(df['a'].str.contains('MODEL'))] = re.findall(re_pattern,df[(df['a'].str.contains('MODEL'))])

# print(df)
# if df['a'].str.contains('\s|\n').any():
#     df['a'] = df['a'].str.split()
#     df['a'] = df['a'].str[0]
#     print(df)
    # df.loc[df['a'].str.contains('\s|\n'), 'a'] = df.loc[df['a'].str.contains('\s|\n'), 'a'].str.split()[0]
    # print(df)
# def split_model(model_text):
#     # if df['a'].str.contains('MODEL').any():
#     #     regex_pattern = 'MODEL\:\s?\n?(.*)'
#     # if df['a'].str.contains('SHARP BRAND GOODS').any():
#     regex_pattern = 'MODEL\:\s?\n?((.*))|GOODS\:?\s?\n?\(?((.*))\)'
#     if regex_pattern:
#         x= re.search(regex_pattern, model_text)
#         if x :
#             return(x.group())
#         else:
#             return model_text

def split_model(model_text):
    model_match = re.search('MODEL\:\s?\n?(.*)', model_text)
    goods_match = re.search('GOODS\:?\s?\n?\(?(.*)\)', model_text)
    if model_match:
        return model_match.group(1)
    elif goods_match:
        return goods_match.group(1)
    else:
        return model_text

# df['a'] = df['a'].apply(split_model)
# print(df)

txt = 'AADHS 998SAh17'


# if re.search('\b[A-Za-z\s]+\b|\b[0-9\s]+\b', txt):
print(re.search('(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]+', txt))