"""
Data client that provides a thin wrapper around the FMP API.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()  # this allows us to import the FMP_API_KEY from .env

# Reload API key after environment is loaded
_API_KEY = os.getenv("FMP_API_KEY")  # this is how we access to the FMP_API_KEY you added in .env
_BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_company_data_for_ticker(ticker: str | float | None) -> dict:
    """
    Fetch the company name, company description, and current stock price for `ticker`.

    Parameters
    ----------
    ticker : str or float or None
        The stock ticker symbol to look up

    Returns
    -------
    dict
        Dictionary containing company name, description, price and currency

    Raises
    ------
    ValueError
        If the ticker is invalid / not found or if the API key is invalid
    RuntimeError
        For API errors, rate limits, or connection issues
    """
    # Validate API key - force reload from environment
    _api_key = os.getenv("FMP_API_KEY")
    if not _api_key:
        raise ValueError("FMP_API_KEY environment variable is not set")

    # Validate and normalize ticker
    if ticker is None or not str(ticker).strip():
        raise ValueError("Ticker symbol cannot be empty or None")

    try:
        ticker = str(ticker).strip().upper()
    except (AttributeError, TypeError):
        raise ValueError(f"Invalid ticker format: {ticker}") from None

    try:
        # Fetch company profile
        profile_url = f"{_BASE_URL}/profile/{ticker}?apikey={_api_key}"
        profile_response = requests.get(profile_url)

        if profile_response.status_code == 401:
            raise ValueError("Invalid API key")
        elif profile_response.status_code == 429:
            raise RuntimeError("API rate limit exceeded")
        elif profile_response.status_code >= 400:
            raise RuntimeError(f"API request failed with status {profile_response.status_code}")

        try:
            profile_data = profile_response.json()
        except ValueError:
            raise RuntimeError("API request failed: invalid JSON response") from None

        if not profile_data:
            raise ValueError(f"Invalid ticker symbol: {ticker}")

        company_profile = profile_data[0]

        # Validate string fields
        name = company_profile.get("companyName")
        description = company_profile.get("description")

        if name is not None and not isinstance(name, str):
            name = None
        if description is not None and not isinstance(description, str):
            description = None

        # Fetch stock quote
        quote_url = f"{_BASE_URL}/quote/{ticker}?apikey={_api_key}"
        quote_response = requests.get(quote_url)

        if quote_response.status_code == 401:
            raise ValueError("Invalid API key")
        elif quote_response.status_code == 429:
            raise RuntimeError("API rate limit exceeded")
        elif quote_response.status_code >= 400:
            raise RuntimeError(f"API request failed with status {quote_response.status_code}")

        try:
            quote_data = quote_response.json()
        except ValueError:
            raise RuntimeError("API request failed: invalid JSON response") from None

        if not quote_data:
            raise ValueError(f"Could not fetch stock price for ticker: {ticker}")

        stock_data = quote_data[0]
        price = stock_data.get("price")

        # Validate price is numeric
        if price is not None and not isinstance(price, int | float):
            price = None

        return {
            "name": name,
            "description": description,
            "price": price,
            "currency": "USD"
        }

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to FMP API: {str(e)}") from None
    except ValueError as e:
        if "Invalid JSON" in str(e):
            raise RuntimeError("API request failed: invalid JSON response") from None
        raise


#dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
#dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
