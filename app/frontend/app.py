import os
import sys

import streamlit as st
from api.fmp_client import get_company_data_for_ticker

"""
Streamlit UI for our mini security master.
"""

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
st.title("📈 Mini Security Master")

# ticker = st.text_input("Enter a stock ticker", value="AAPL", max_chars=10) . . .

aapl_data = get_company_data_for_ticker("MSFT")

st.write(aapl_data)

