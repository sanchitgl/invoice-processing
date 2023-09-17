# import os
# from azure.ai.formrecognizer import DocumentAnalysisClient
# from azure.core.credentials import AzureKeyCredential
import pandas as pd
import re
# from entities.fix_product_description import fix_na

# # set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal

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
import re
import dateparser
import spacy
import datefinder

# Load the SpaCy English language model
nlp = spacy.load("en_core_web_sm")

# Define regular expressions to match different date formats
date_patterns = [
    r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
    r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY
    r"\d{2}-\w{3}-\d{4}",  # DD-MMM-YYYY
    r"\d{2}\s\w{3}\s\d{4}",  # DD MMM YYYY
    r"\w{3}\s\d{1,2},\s\d{4}",  # MMM DD, YYYY
    r"\d{1,2}\s\w{3},\s\d{4}",  # DD MMM, YYYY
]

# Define a function to extract dates using regular expressions
def extract_dates_with_regex(text):
    dates = []
    for pattern in date_patterns:
        date_pattern = re.compile(pattern)
        for match in date_pattern.finditer(text):
            date_str = match.group(0)
            date = dateparser.parse(date_str)
            if date:
                dates.append(date)
    return dates

# Combine the results from both functions
def extract_dates(text):
    dates_with_regex = extract_dates_with_regex(text)
    print(dates_with_regex)
    # dates_with_spacy = extract_dates_with_spacy(text)
    # print(dates_with_spacy)
    dates = list(set(dates_with_regex))
    return sorted(dates)


text = '''
                                                  key                                              value
0                                             SHIPPER  NINGBO XINLE HOUSEHOLD APPLIANCES\nCO., LTD. 1...
1                                                TEL:                                 0086-574-87495103*
2                                       VOYAGE NUMBER                                  0FLBVW1MA/0FLBVW1
3                               BILL OF LADING NUMBER                                         NBMD995146
4                                           CONSIGNEE  VISALLY TRADE CENTRE PTY LTD C/O PILLAY R GROU...
5                                               TEL :                            +248 610699 /2501072/27
6                                               TEL :                         +248 610699 /2501072/27 **
7                                            CARRIER:  CMA CGM Société Anonyme au Capital de 234 988 ...
8                                                Tel:  (33) 4 88 91 90 00 - Fax: (33) 4 88 91 90 95 5...
9                                    PRE CARRIAGE BY*                                                NaN
10                                  PLACE OF RECEIPT*                                                NaN
11                              FREIGHT TO BE PAID AT                                             NINGBO
12                 NUMBER OF ORIGINAL BILLS OF LADING                                          THREE (3)
13                                             VESSEL                                 CMA CGM MONTMARTRE
14                                    PORT OF LOADING                                             NINGBO
15                                  PORT OF DISCHARGE                                      PORT VICTORIA
16                           FINAL PLACE OF DELIVERY*                                                NaN
17                                      MARKS AND NOS                                                NaN
18                           NO AND KIND\nOF PACKAGES                                                  1
19  DESCRIPTION OF PACKAGES AND GOODS AS STATED BY...                                                NaN
20                           GROSS WEIGHT\nCARGO\nKGS                                           6709.500
21                                          TARE\nKGS                                               3900
22                                   MEASUREMENT\nCBM                                             69.300
23                                CONTAINER AND SEALS                                        TCNU6556712
24      SHIPPER'S LOAD STOW AND COUNT SAID TO CONTAIN                                 x 40HC 198 CARTONS
25                                               SEAL                                           C4170168
26                                         ** EMAIL :                      ELECTRONICS@PILLAYRGROUP. COM
27                                       2ND NOTIFY :  SHARP MIDDLE EAST FZE P.O.BOX: 17115, JEBEL AL...
28                              DISCHARGE PORT AGENT:  SOCIETE SEYCHELLOISE DE NAVIGATION\nPO BOX 339...
29                            PLACE AND DATE OF ISSUE                                             NINGBO
30                             SIGNED FOR THE SHIPPER                                                NaN
31                                      VOYAGE NUMBER                                  0FLBVW1MA/0FLBVW1
32                              BILL OF LADING NUMBER                                         NBMD995146
33                                  PLACE OF RECEIPT*                                    PORT OF LOADING
34                              FREIGHT TO BE PAID AT           NINGBO\nPORT OF DISCHARGE\nPORT VICTORIA
35                 NUMBER OF ORIGINAL BILLS OF LADING                                              THREE
36                                             VESSEL                         CMA CGM MONTMARTRE\nNINGBO
37                           FINAL PLACE OF DELIVERY*                                                NaN
38                           NO AND KIND\nOF PACKAGES  Shipped on Board, CMA CGM MONTMARTRE 08-APR-20...
39  DESCRIPTION OF PACKAGES AND GOODS AS STATED BY...                                                CMA
40                                       GROSS WEIGHT                                                NaN
41                                  TARE\nMEASUREMENT                                           KGS\nCBM
42                LOAD STOW AND COUNT SAID TO CONTAIN                                                NaN
43                                              CARGO                                                KGS
44                                             Total:                                                  1
45                            PLACE AND DATE OF ISSUE                                             NINGBO
46                             SIGNED FOR THE SHIPPER                                                NaN
47                                            FOR THE        08 APR 2022\nCMA CGM S.A. BY CMA CGM Ningbo
'''

# print(extract_dates(text))

# matches = datefinder.find_dates(text)
# for match in matches:
#     print(match)
import pandas as pd

# create a sample DataFrame
df = pd.DataFrame({'date': ['12-2-2020']})

# save the new DataFrame to a CSV file with the desired date format
df.to_csv('my_data.csv', index=False, date_format='%m-%d-%Y')
