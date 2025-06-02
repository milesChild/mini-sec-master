import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from api.fmp_client import get_company_data_for_ticker

"""
Streamlit UI for our mini security master.
"""

st.title("📈 Mini Security Master")

ticker = st.text_input("Enter a stock ticker", value="AAPL", max_chars=10)

if not ticker.strip():
    st.error("Please enter a stock ticker")
else:
    try:
        # Convert to uppercase for consistency
        ticker = ticker.strip().upper()
        company_data = get_company_data_for_ticker(ticker)

        if not company_data:
            st.error(f"No data found for ticker '{ticker}'. Please check if the ticker is valid.")
        else:
            st.write(company_data)

    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")

