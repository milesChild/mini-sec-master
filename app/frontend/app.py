"""
Streamlit UI for our mini security master.
"""

import streamlit as st

from app.api.fmp_client import get_company_data_for_ticker

st.title("📈 Mini Security Master")

# ticker = st.text_input("Enter a stock ticker", value="AAPL", max_chars=10) . . .

aapl_data = get_company_data_for_ticker("AAPL")

st.write(aapl_data)
