"""
Data client that provides a thin wrapper around the FMP API.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # this allows us to import the FMP_API_KEY from .env

_API_KEY = os.getenv("FMP_API_KEY")# this is how we access to the FMP_API_KEY you added in .env
_BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_company_data_for_ticker(ticker: str):
    """
    Fetch the company name, company description, and current stock price for `ticker`.

    Raises
    ------
    ValueError
        If the ticker is invalid / not found or if the API key is invalid
    """
    if not _API_KEY:
        raise ValueError("FMP_API_KEY environment variable is not set")
    
    ticker = ticker.strip().upper()
    try:
        profile_url = f"{_BASE_URL}/profile/{ticker}?apikey={_API_KEY}"
        profile_response = requests.get(profile_url)
        profile_response.raise_for_status() 
        
        profile_data = profile_response.json()
        if not profile_data:
            raise ValueError(f"Invalid ticker symbol: {ticker}")
        
        company_profile = profile_data[0]
        quote_url = f"{_BASE_URL}/quote/{ticker}?apikey={_API_KEY}"
        quote_response = requests.get(quote_url)
        quote_response.raise_for_status()
        quote_data = quote_response.json()
        if not quote_data:
            raise ValueError(f"Could not fetch stock price for ticker: {ticker}")
        stock_data = quote_data[0]
        return {
            "name": company_profile.get("companyName"),
            "description": company_profile.get("description"),
            "price": stock_data.get("price"),
            "currency": "USD"
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid API key") from e
        elif e.response.status_code == 429:
            raise RuntimeError("API rate limit exceeded") from e
        else:
            raise RuntimeError(f"API request failed: {str(e)}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to FMP API: {str(e)}") from e
