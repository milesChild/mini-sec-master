"""
Data client that provides a thin wrapper around the FMP API.
"""

import os

from dotenv import load_dotenv

load_dotenv()  # this allows us to import the FMP_API_KEY from .env

_API_KEY = os.getenv("FMP_API_KEY")# this is how we access to the FMP_API_KEY you added in .env

def get_company_data_for_ticker(ticker: str):
    """
    Fetch the company name, company description, and current stock price for `ticker`.

    Raises
    ------
    ValueError
        If the ticker is invalid / not found.
    """
    raise NotImplementedError()
