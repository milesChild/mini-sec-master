"""
Streamlit UI for our mini security master.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
from api.fmp_client import get_company_data_for_ticker

st.title("📈 Mini Security Master")

ticker = st.text_input("Enter a stock ticker", value="AAPL", max_chars=10)

if ticker:
    try:
        company_data = get_company_data_for_ticker(ticker)
        st.write(company_data)
    except ValueError as e:
        st.error(f"Error: {str(e)}")
else:
    st.warning("Please enter a ticker symbol")

