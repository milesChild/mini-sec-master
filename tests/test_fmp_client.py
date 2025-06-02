"""
Unit tests for the FMP client.
"""

from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError

from app.api.fmp_client import get_company_data_for_ticker


# test that the function raises a value error when passed empty string
def test_raises_value_error_for_empty_string():
    with pytest.raises(ValueError):
        get_company_data_for_ticker("")


# test that the function raises a value error when passed non-string ticker
@pytest.mark.parametrize(
    "invalid_input",
    [
        1234583.0,  # float
        42,  # integer
        True,  # boolean
        None,  # None
        ["AAPL"],  # list
        {"ticker": "AAPL"},  # dict
    ],
)
def test_raises_value_error_for_non_string_ticker(invalid_input):
    with pytest.raises(ValueError):
        get_company_data_for_ticker(invalid_input)


# test that the function raises an error when the ticker is not found
def test_raises_value_error_for_invalid_ticker():
    with pytest.raises(ValueError):
        get_company_data_for_ticker("INVALID")


# test the function raises a value error when not all company data is returned
@patch("app.api.fmp_client.requests.get")
def test_raises_value_error_when_not_all_company_data_is_returned(mock_get):
    mock_fmp_response = Mock()
    mock_fmp_response.json.return_value = [
        {"companyName": "The Cheesecake Factory", "description": "Cheesecake"}
    ]
    mock_get.return_value = mock_fmp_response
    with pytest.raises(ValueError):
        get_company_data_for_ticker("AAPL")


# test the function works when all company data is returned
@patch("app.api.fmp_client.requests.get")
def test_get_company_data_returns_correct_data_for_valid_ticker(mock_get):
    mock_fmp_response = Mock()
    mock_fmp_response.json.return_value = [
        {
            "symbol": "CCF",
            "companyName": "The Cheesecake Factory",
            "description": "Cheesecake",
            "price": 200.0,
        }
    ]
    mock_get.return_value = mock_fmp_response
    result = get_company_data_for_ticker("CCF")
    assert result["companyName"] == "The Cheesecake Factory"
    assert result["description"] == "Cheesecake"
    assert result["price"] == 200.0
    assert result["symbol"] == "CCF"


# test that the request is made to the correct URL with proper API key
@patch("app.api.fmp_client.requests.get")
def test_request_url_and_api_key(mock_get):
    mock_fmp_response = Mock()
    mock_fmp_response.json.return_value = [
        {
            "symbol": "CCF",
            "companyName": "The Cheesecake Factory",
            "description": "Cheesecake",
            "price": 200.0,
        }
    ]
    mock_get.return_value = mock_fmp_response
    get_company_data_for_ticker("CCF")

    # Get the URL that was called
    called_url = mock_get.call_args[0][0]

    # Check all URL components
    assert called_url.startswith("https://financialmodelingprep.com/stable/profile"), (
        "Incorrect base URL"
    )
    assert "symbol=CCF" in called_url, "Missing or incorrect symbol parameter"
    assert "apikey=" in called_url, "Missing API key parameter"


# test that the function handles HTTP errors appropriately
@patch("app.api.fmp_client.requests.get")
def test_raises_error_on_http_error_status(mock_get):
    mock_fmp_response = Mock()
    mock_fmp_response.status_code = 404
    mock_fmp_response.raise_for_status.side_effect = HTTPError("404 Client Error")
    mock_get.return_value = mock_fmp_response

    with pytest.raises(HTTPError):
        get_company_data_for_ticker("CCF")


# test that the function succeeds with 200 status
@patch("app.api.fmp_client.requests.get")
def test_succeeds_with_200_status(mock_get):
    mock_fmp_response = Mock()
    mock_fmp_response.status_code = 200
    mock_fmp_response.json.return_value = [
        {
            "symbol": "CCF",
            "companyName": "The Cheesecake Factory",
            "description": "Cheesecake",
            "price": 200.0,
        }
    ]
    mock_get.return_value = mock_fmp_response

    result = get_company_data_for_ticker("CCF")
    assert result is not None
