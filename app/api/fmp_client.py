"""
Data client that provides a thin wrapper around the FMP API.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()  # this allows us to import the FMP_API_KEY from .env

_API_KEY = os.getenv("FMP_API_KEY")  # this is how we access to the FMP_API_KEY you added in .env


def get_company_data_for_ticker(ticker: str):
    """
    Fetch the company name, company description, and current stock price for `ticker`.

    Raises
    ------
    ValueError
        If the ticker is invalid / not found.
    """
    if not ticker:
        raise ValueError("Ticker cannot be empty")
    if not isinstance(ticker, str):
        raise ValueError("Ticker must be a string")

    url = f"https://financialmodelingprep.com/stable/profile?symbol={ticker}&apikey={_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()  # This will raise HTTPError for status codes >= 400

    if response.json() == []:
        raise ValueError("Ticker not found")

    company_data = response.json()[0]
    if (
        "companyName" not in company_data
        or "description" not in company_data
        or "price" not in company_data
    ):
        raise ValueError("Incomplete company data")

    return company_data
