import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets scopes
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_gsheet_client():
    # Load service account credentials from Streamlit secrets
    service_account_info = st.secrets["gcp_service_account"]

    credentials = Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPE
    )

    return gspread.authorize(credentials)

def get_sheet(sheet_name):
    client = get_gsheet_client()
    return client.open(sheet_name).sheet1
