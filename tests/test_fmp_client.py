"""
Unit tests for the FMP client.
"""

from unittest.mock import Mock, patch

import pytest

from app.api.fmp_client import get_company_data_for_ticker


# NOTE: Starter test for now
def test_raises_value_error_for_invalid_ticker():
    with pytest.raises(ValueError):
        get_company_data_for_ticker(1234583.0)


# test that the function raises an error when an invalid ticker is passed. The request still goes through but the response is empty.


@patch("app.api.fmp_client.requests.get")
def test_get_company_data_for_ticker(mock_get):
    mock_fmp_response = Mock()
    mock_fmp_response.status_code = 200
    mock_fmp_response.json.return_value = []
    mock_get.return_value = mock_fmp_response

    with pytest.raises(ValueError, match="No data found for"):
        get_company_data_for_ticker("INVALIDTICKER")


# test that the function raises an error when the ticker is not found


@patch("app.api.fmp_client.requests.get")
def test_get_company_data_for_ticker_not_found(mock_get):
    mock_fmp_response = Mock()
    mock_fmp_response.status_code = 200
    mock_fmp_response.json.return_value = []
    mock_get.return_value = mock_fmp_response

    with pytest.raises(ValueError, match="No data found for"):
        get_company_data_for_ticker("TICKERNOTFOUND")


# test to see if the function has missing fields in the response
@patch("app.api.fmp_client.requests.get")
def test_missing_fields_in_response_missing_fields(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"symbol": "AAPL"}
    ]  # Missing 'companyName', 'description', etc.
    mock_get.return_value = mock_response

    result = get_company_data_for_ticker("AAPL")

    # We check the function still returns whatever is there (or handle it differently if needed)
    assert result["ticker"] == "AAPL"
    assert result["name"] is None
    assert result["description"] is None
    assert result["price"] is None


# test to see if the function is not a list
@patch("app.api.fmp_client.requests.get")
def test_response_not_list(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"error": "unexpected format"}
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Unexpected format"):
        get_company_data_for_ticker("AAPL")
