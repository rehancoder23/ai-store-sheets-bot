import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai
import json

# 1. Page Config
st.set_page_config(
    page_title="AI Store - Intelligent Assistant",
    page_icon="🤖",
    layout="centered"
)

# 2. GitHub, Share, Star aur Deploy Buttons ko Chupane Ka Bilkul Saaf Code
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    div[data-testid="stToolbar"] {visibility: hidden !important;}
    button[title="View source code"] {visibility: hidden !important;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 3. Google Sheets Aur Gemini Config Setup
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    # Aapki Real Sheet ID bahi
    SHEET_ID = "1m4_maVguqgZjgf6lxT37drygjK6zWSeTzpTCsnRpgv0" 
    sheet = client.open_by_key(SHEET_ID).sheet1

    # Gemini Setup
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Config Error: Secrets check karein bahi! {e}")

# 4. Session State Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []
if "customer_data" not in st.session_state:
    st.session_state.customer_data = {"Name": None, "Address": None, "Phone": None}
if "sheet_saved" not in st.session_state:
    st.session_state.sheet_saved = False

# 🔥 REHAN BHAI: Yahan se maine saari confusion khatam kar di hai! Saaf HTML text hai ab.
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🤖 AI Store Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555555;'>Baatoan baatoan mein order book karne wala bot bahi</h3>", unsafe_allow_html=True)
st.write("---")

# Old Messages Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# System Instructions for AI
SYSTEM_INSTRUCTION = f"""
You are a polite customer service bot for 'AI Store'. Talk in Roman Urdu (use friendly words like 'bahi', 'shukriya').
Your job is to collect exactly THREE details from the user one by one:
1. Customer's Name
2. Delivery Address
3. Phone Number

Do NOT ask all details at once.
Once you have ALL three details, thank them and strictly append this hidden JSON block at the very end of your final response:
DATA_START {{"name": "USER_NAME", "address": "USER_ADDRESS", "phone": "USER_PHONE"}} DATA_END
Current status: {json.dumps(st.session_state.customer_data)}
"""

# 5. User Input & Chat Flow
if user_input := st.chat_input("Yahan likhein bahi..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI soch raha hai bahi..."):
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-3.1-flash-lite",
                    system_instruction=SYSTEM_INSTRUCTION
                )
                
                chat_history = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages
                ]
                
                response = model.generate_content(chat_history)
                bot_response = response.text
                
                # Sheet Saving Logic
                if "DATA_START" in bot_response and "DATA_END" in bot_response:
                    try:
                        json_str = bot_response.split("DATA_START")[1].split("DATA_END")[0].strip()
                        extracted_data = json.loads(json_str)
                        
                        if not st.session_state.sheet_saved:
                            sheet.append_row([extracted_data["name"], extracted_data["address"], extracted_data["phone"]])
                            st.session_state.sheet_saved = True
                            st.balloons()
                            bot_response = bot_response.split("DATA_START")[0] + "\n\n🎉 *Rehan Bhai! Order kamyabi se Sheet mein back-end par save ho gaya hai!*"
                    except Exception as sheet_err:
                        st.error(f"Sheet Error: {sheet_err}")
                
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
            except Exception as api_err:
                st.error(f"Gemini API Error: {api_err}")
