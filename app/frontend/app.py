"""
Streamlit UI for our mini security master.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from api.fmp_client import get_company_data_for_ticker
from requests.exceptions import HTTPError

# Set page config and styling
st.set_page_config(page_title="Mini Security Master", page_icon="📈")

# Custom CSS
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .company-info {
        padding: 20px;
        border-radius: 5px;
        background-color: #f8f9fa;
        margin: 10px 0;
    }
    .description {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        line-height: 1.6;
        margin-top: 10px;
    }
    .error-message {
        background-color: #ffebee;
        color: #c62828;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .price {
        color: #4CAF50;
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📈 Mini Security Master")

col1, col2 = st.columns([2, 1])
with col1:
    ticker = st.text_input("Enter a stock ticker", value="AAPL", max_chars=10)
with col2:
    st.write("")  # Add some spacing
    st.write("")  # Add some spacing
    search_button = st.button("🔍 Get Company Data")

if search_button:
    if ticker:
        try:
            company_data = get_company_data_for_ticker(ticker.upper())
            if company_data:
                st.markdown(
                    f"""
                <div class='company-info'>
                    <h2>{company_data.get("companyName", "N/A")} ({ticker.upper()})</h2>
                    <div class='price'>💲 {company_data.get("price", "N/A"):,.2f} USD</div>
                    <div class='description'>
                        {company_data.get("description", "No description available.")}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        except ValueError as e:
            st.markdown(
                f"""
            <div class='error-message'>
                ❌ {str(e) or "Invalid ticker symbol. Please check and try again."}
            </div>
            """,
                unsafe_allow_html=True,
            )
        except HTTPError:
            st.markdown(
                """
            <div class='error-message'>
                ❌ API Error: Unable to fetch data at this time. Please try again later.
            </div>
            """,
                unsafe_allow_html=True,
            )
        except Exception:
            st.markdown(
                """
            <div class='error-message'>
                ❌ An unexpected error occurred. Please try again later.
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
        <div class='error-message'>
            ⚠️ Please enter a ticker symbol
        </div>
        """,
            unsafe_allow_html=True,
        )
