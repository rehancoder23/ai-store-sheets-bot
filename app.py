import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. Google Sheets Connection Setup
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Streamlit Secrets se credentials uthana
creds_dict = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# Aapki Google Sheet ki ID (URL mein se d/ ke baad wali string)
# Isko aap apne mutabiq tabdeel kar sakte hain
SHEET_ID = "0232629585" 
sheet = client.open_by_key(SHEET_ID).sheet1

st.title("🤖 AI Store - Order Booking System")

# Simple User Input Form
with st.form("order_form"):
    name = st.text_input("Aapka Naam (Name)")
    address = st.text_input("Ghar ka Pata (Address)")
    phone = st.text_input("Phone Number")
    
    submit_button = st.form_submit_button(label="Book Order")

if submit_button:
    if name and address and phone:
        try:
            # Sheet mein naya row add karna: Name, Address, Phone
            sheet.append_row([name, address, phone])
            st.success(f"🎉 Shukriya {name}! Aapka order kamyabi se book ho gaya hai.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Meharbani karke saari details fill karein bahi!")
