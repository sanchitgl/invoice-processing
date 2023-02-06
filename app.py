import streamlit as st
from invoice_test import analyze_invoice
from bl_analyse import analyze_bl
import os
state = st.session_state

def landing_page():
    #with title:
    # emp,title,emp = st.columns([2,2,2])
    # with title:
    
    if 'submit_ra' not in state:
        state.submit_ra= False
    if 'submit_inv' not in state:
        state.submit_inv= False
    if 'submit_bl' not in state:
        state.submit_bl= False

    st.markdown("<h2 style='text-align: center; padding:0'>Invoice Processing</h2>", unsafe_allow_html=True)
    st.write('&nbsp;')
    invoices, bl_docs, submit= file_upload_form()
    

    #try:
    if submit:
        state.submit_ra = True
        print(invoices, bl_docs)
        #print(warehouse_reports)
        #print(submit)
            #print(shipment_instructions_df)
        with st.spinner('Please wait'):
            try:
                delete_temp()
            except:
                print()
            
            if invoices:
                state.submit_inv= True
                print("Dont run invoices")
                analyze_invoice(invoices)
                emp, but, empty = st.columns([2.05,1.2,1.5])
                with but:
                    st.write("###")
                    with open('Tracker/Invoice_tracker.csv', 'rb') as my_file:
                        click = st.download_button(label = 'Download Invoice Tracker', data = my_file, file_name = 'invoice_tracker.csv', 
                        mime = 'text/csv')
            if bl_docs != []:
                state.submit_bl= True
                print("run invoices")
                analyze_bl(bl_docs)
                emp, but, empty = st.columns([2.05,1.2,1.5])
                with but:
                    st.write("###")
                    with open('Tracker/BL_tracker.csv', 'rb') as bl_file:
                        click = st.download_button(label = 'Download B\L Tracker', data = bl_file, file_name = 'bl_tracker.csv', 
                        mime = 'text/csv')
    else:
        if state.submit_ra == True:
            if state.submit_inv== True:
                emp, but, empty = st.columns([2.05,1.2,1.5])
                with but:
                    st.write("###")
                    with open('Tracker/Invoice_tracker.csv', 'rb') as my_file:
                        click = st.download_button(label = 'Download Invoice Tracker', data = my_file, file_name = 'invoice_tracker.csv', 
                        mime = 'text/csv')
            
            if state.submit_bl== True:
                emp, but, empty = st.columns([2.05,1.2,1.5])
                with but:
                    st.write("###")
                    with open('Tracker/BL_tracker.csv', 'rb') as bl_file:
                        click = st.download_button(label = 'Download B\L Tracker', data = bl_file, file_name = 'bl_tracker.csv', 
                        mime = 'text/csv')
                #print(click) 
        #st.write(workbook) 
    # except:
    #     st.error("Run failed, kindly check if the inputs are valid")

def delete_temp():
    os.remove('Tracker/Invoice_tracker.csv')


def file_upload_form():
    with st.form(key = 'invioice_uploader'):
        text, upload = st.columns([1,3]) 
        with text:
            st.write("###")
            st.write("###")
            st.write("Upload Invoices:")
        with upload:
            invoices = st.file_uploader("",key = 'invoices',accept_multiple_files = True, type=['pdf'])

        text, upload = st.columns([1,3]) 
        with text:
            st.write("###")
            st.write("###")
            st.write("Upload B\L docs:")
        with upload:
            bl_docs = st.file_uploader("",key = 'bl_docs',accept_multiple_files = True, type=['pdf'])
        
        a,button,b = st.columns([2,1.2,1.5]) 
        with button:
            st.write('###')
            submit = st.form_submit_button(label = "Start Processing")
            #submit = st.button(label="Start Reconciliation")

    return invoices, bl_docs, submit

landing_page()