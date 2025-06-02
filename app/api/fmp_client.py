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
        If there is no data found for the ticker.
    """

    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={_API_KEY}"

    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data for {ticker}")

    data = response.json()

    if not data:
        raise ValueError(f"No data found for {ticker}")

    if not isinstance(data, list):
        raise ValueError(f"Unexpected format: Response data for {ticker} is not a list")

    company_data = data[0]

    return {
        "ticker": company_data.get("symbol"),
        "name": company_data.get("companyName"),
        "description": company_data.get("description"),
        "price": company_data.get("price")
    }

