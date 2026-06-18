import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. Page Configuration (Website ko khoobsurat aur professional banane ke liye)
st.set_page_config(
    page_title="AI Store - Order Booking",
    page_icon="📦",
    layout="centered"
)

# 2. GitHub ka nishan, Streamlit ka footer aur Share menu chupanay ka Khufia Code
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div.block-container {padding-top: 2rem;}
    /* Input fields ko thoda stylish banane ke liye */
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_code=True)

# 3. Google Sheets Connection Setup
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)

    # 🔥 REHAN BHAI: Aapki Sheet ID maine khud fit kar di hai yahan!
    SHEET_ID = "1m4_maVguqgZjgf6lxT37drygjK6zWSeTzpTCsnRpgv0" 
    sheet = client.open_by_key(SHEET_ID).sheet1
except Exception as e:
    st.error("⚠️ System Setup Mein Masla Hai. Meharbani karke cloud settings check karein bahi!")

# 4. Professional Header UI
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📦 AI Store</h1>", unsafe_allow_code=True)
st.markdown("<p style='text-align: center; color: #555555; font-size: 1.1rem;'>Customer Order Booking System</p>", unsafe_allow_code=True)
st.write("---")

st.subheader("📝 Naya Order Book Karein bahi")

# Professional Form Layout
with st.form("order_form", clear_on_submit=True):
    name = st.text_input("👤 Customer Name (Naam)")
    address = st.text_input("🏠 Delivery Address (Ghar ka Pata)")
    phone = st.text_input("📞 Phone Number")
    
    # Form ka submit button
    st.markdown("<br>", unsafe_allow_code=True)
    submit_button = st.form_submit_button(label="Confirm & Save Order 🚀", use_container_width=True)

# 5. Order Logic
if submit_button:
    if name and address and phone:
        with st.spinner("Order sheet mein save ho raha hai, thoda intezar karein bahi..."):
            try:
                # Sheet mein naya row add karna
                sheet.append_row([name, address, phone])
                st.balloons() # Screen par balloons udane ke liye decoration
                st.success(f"🎉 Shabaash Rehan Bhai! {name} ka order kamyabi se aapki Google Sheet mein save ho gaya hai!")
            except Exception as e:
                st.error(f"❌ Error: Sheet mein data nahi ja saka bahi! Check karein ke aapne Sheet share ki hui hai na? ({e})")
    else:
        st.warning("⚠️ Yaar meharbani karke teeno cheezain (Name, Address, Phone) lazmi likhein bahi!")
