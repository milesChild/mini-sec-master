"""
Unit tests for the FMP client.
"""

import pytest
from unittest.mock import patch, Mock
import requests

from app.api.fmp_client import get_company_data_for_ticker

# Tests that numeric input for ticker raises ValueError
def test_raises_value_error_for_invalid_ticker():
    with pytest.raises(ValueError):
        get_company_data_for_ticker(1234583.0)

# Tests that invalid ticker symbols return an error
@patch("app.api.fmp_client.requests.get")
def test_invalid_ticker_raises_error(mock_get):
    """Test that the function raises an error when an invalid ticker is passed"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []  # FMP returns empty list for invalid tickers
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Invalid ticker symbol"):
        get_company_data_for_ticker("INVALID")

# Tests that non-existent tickers return a 404 error
@patch("app.api.fmp_client.requests.get")
def test_ticker_not_found(mock_get):
    """Test that the function raises an error when the ticker is not found"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = Exception("Not Found")
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="API request failed"):
        get_company_data_for_ticker("NOTFOUND")

# Tests that valid ticker (AAPL) returns all required data fields
@patch("app.api.fmp_client.requests.get")
def test_valid_ticker_returns_complete_data(mock_get):
    """Check if AAPL returns all expected fields"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": "Apple Inc.",
        "description": "Apple designs smartphones and computers",
        "symbol": "AAPL"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{
        "symbol": "AAPL",
        "price": 150.0
    }]

    mock_get.side_effect = [profile_response, quote_response]

    result = get_company_data_for_ticker("AAPL")
    
    assert result["name"] == "Apple Inc."
    assert result["description"] == "Apple designs smartphones and computers"
    assert result["price"] == 150.0
    assert result["currency"] == "USD"

# Tests that multiple different company tickers return correct data
@patch("app.api.fmp_client.requests.get")
def test_different_valid_tickers(mock_get):
    """Test multiple known companies (MSFT, GOOGL, etc)"""
    test_cases = {
        "MSFT": {
            "name": "Microsoft Corporation",
            "description": "Microsoft develops software",
            "price": 300.0
        },
        "GOOGL": {
            "name": "Alphabet Inc.",
            "description": "Google's parent company",
            "price": 2500.0
        }
    }

    for ticker, data in test_cases.items():
        profile_response = Mock()
        profile_response.status_code = 200
        profile_response.json.return_value = [{
            "companyName": data["name"],
            "description": data["description"],
            "symbol": ticker
        }]

        quote_response = Mock()
        quote_response.status_code = 200
        quote_response.json.return_value = [{
            "symbol": ticker,
            "price": data["price"]
        }]

        mock_get.side_effect = [profile_response, quote_response]
        
        result = get_company_data_for_ticker(ticker)
        assert result["name"] == data["name"]
        assert result["description"] == data["description"]
        assert result["price"] == data["price"]
        assert result["currency"] == "USD"

# Tests that ticker symbols are case-insensitive
@patch("app.api.fmp_client.requests.get")
def test_ticker_case_insensitive(mock_get):
    """Test that 'aapl' and 'AAPL' give same results"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": "Apple Inc.",
        "description": "Test description",
        "symbol": "AAPL"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{
        "symbol": "AAPL",
        "price": 150.0
    }]

    mock_get.side_effect = [profile_response, quote_response]
    lower_result = get_company_data_for_ticker("aapl")

    mock_get.side_effect = [profile_response, quote_response]
    upper_result = get_company_data_for_ticker("AAPL")

    assert lower_result == upper_result

# Tests that whitespace in ticker symbols is properly handled
@patch("app.api.fmp_client.requests.get")
def test_ticker_with_whitespace(mock_get):
    """Test that ' AAPL ' is handled correctly"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": "Apple Inc.",
        "description": "Test description",
        "symbol": "AAPL"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{
        "symbol": "AAPL",
        "price": 150.0
    }]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker(" AAPL ")
    
    assert result["name"] == "Apple Inc."
    assert result["price"] == 150.0

# Tests that empty string ticker raises ValueError
def test_empty_ticker_raises_error():
    """Test empty string input"""
    with pytest.raises(ValueError):
        get_company_data_for_ticker("")

# Tests that None ticker raises ValueError
def test_none_ticker_raises_error():
    """Test None input"""
    with pytest.raises(ValueError):
        get_company_data_for_ticker(None)

# Tests that tickers with special characters raise ValueError
@patch("app.api.fmp_client.requests.get")
def test_invalid_ticker_format(mock_get):
    """Test ticker with invalid characters like '$AAPL'"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Invalid ticker symbol"):
        get_company_data_for_ticker("$AAPL")

# Tests that extremely long ticker strings are rejected
@patch("app.api.fmp_client.requests.get")
def test_extremely_long_ticker(mock_get):
    """Test unreasonably long ticker string"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Invalid ticker symbol"):
        get_company_data_for_ticker("A" * 100)

# Tests that invalid API key returns appropriate error
@patch("app.api.fmp_client.requests.get")
def test_invalid_api_key(mock_get):
    """Verify correct error when API key is invalid"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized")
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Invalid API key"):
        get_company_data_for_ticker("AAPL")

# Tests that missing API key environment variable raises error
@patch.dict("os.environ", {}, clear=True)
def test_missing_api_key():
    """Verify error when API key environment variable is missing"""
    with pytest.raises(ValueError, match="FMP_API_KEY environment variable is not set"):
        get_company_data_for_ticker("AAPL")

# Tests that rate limit exceeded response is handled correctly
@patch("app.api.fmp_client.requests.get")
def test_rate_limit_exceeded(mock_get):
    """Test handling of 429 rate limit response"""
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("429 Client Error: Too Many Requests")
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="API rate limit exceeded"):
        get_company_data_for_ticker("AAPL")

# Tests that API timeout is handled gracefully
@patch("app.api.fmp_client.requests.get")
def test_api_timeout(mock_get):
    """Test handling of API timeout"""
    mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

    with pytest.raises(RuntimeError, match="Failed to connect to FMP API"):
        get_company_data_for_ticker("AAPL")

# Tests that 5xx server errors are handled properly
@patch("app.api.fmp_client.requests.get")
def test_api_5xx_error(mock_get):
    """Test handling of server errors"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="API request failed"):
        get_company_data_for_ticker("AAPL")

# Tests that network connection errors are handled appropriately
@patch("app.api.fmp_client.requests.get")
def test_network_connection_error(mock_get):
    """Test handling of network connectivity issues"""
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

    with pytest.raises(RuntimeError, match="Failed to connect to FMP API"):
        get_company_data_for_ticker("AAPL")

# Tests that missing company name in response is handled correctly
@patch("app.api.fmp_client.requests.get")
def test_missing_company_name(mock_get):
    """Test handling when API response missing company name"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "description": "Test description",
        "symbol": "TEST"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{"price": 100.0}]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker("TEST")
    assert result["name"] is None

# Tests that missing description in response is handled correctly
@patch("app.api.fmp_client.requests.get")
def test_missing_description(mock_get):
    """Test handling when API response missing description"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": "Test Company",
        "symbol": "TEST"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{"price": 100.0}]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker("TEST")
    assert result["description"] is None

# Tests that missing price in response is handled correctly
@patch("app.api.fmp_client.requests.get")
def test_missing_price(mock_get):
    """Test handling when API response missing price"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": "Test Company",
        "description": "Test description",
        "symbol": "TEST"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{"symbol": "TEST"}]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker("TEST")
    assert result["price"] is None

# Tests that null values in API response are handled correctly
@patch("app.api.fmp_client.requests.get")
def test_null_values_in_response(mock_get):
    """Test handling of null values in API response"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": None,
        "description": None,
        "symbol": "TEST"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{"price": None}]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker("TEST")
    assert result["name"] is None
    assert result["description"] is None
    assert result["price"] is None

# Tests that malformed JSON response is handled properly
@patch("app.api.fmp_client.requests.get")
def test_malformed_json_response(mock_get):
    """Test handling of invalid JSON in API response"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="API request failed"):
        get_company_data_for_ticker("AAPL")

# Tests that response contains all required data fields
@patch("app.api.fmp_client.requests.get")
def test_response_contains_required_fields(mock_get):
    """Verify all required fields are present"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": "Test Company",
        "description": "Test description",
        "symbol": "TEST"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{"price": 100.0}]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker("TEST")
    
    required_fields = {"name", "description", "price", "currency"}
    assert all(field in result for field in required_fields)

# Tests that price field is a valid number
@patch("app.api.fmp_client.requests.get")
def test_price_is_numeric(mock_get):
    """Verify price field is a valid number"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": "Test Company",
        "description": "Test description",
        "symbol": "TEST"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{"price": "not a number"}]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker("TEST")
    assert result["price"] is None

# Tests that currency field is always USD
@patch("app.api.fmp_client.requests.get")
def test_currency_is_usd(mock_get):
    """Verify currency field is always USD"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": "Test Company",
        "description": "Test description",
        "symbol": "TEST"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{"price": 100.0}]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker("TEST")
    assert result["currency"] == "USD"

# Tests that description field is a valid string
@patch("app.api.fmp_client.requests.get")
def test_description_is_string(mock_get):
    """Verify description is a valid string"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": "Test Company",
        "description": 12345,  # Non-string description
        "symbol": "TEST"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{"price": 100.0}]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker("TEST")
    assert result["description"] is None

# Tests that company name field is a valid string
@patch("app.api.fmp_client.requests.get")
def test_name_is_string(mock_get):
    """Verify company name is a valid string"""
    profile_response = Mock()
    profile_response.status_code = 200
    profile_response.json.return_value = [{
        "companyName": 12345,  # Non-string name
        "description": "Test description",
        "symbol": "TEST"
    }]

    quote_response = Mock()
    quote_response.status_code = 200
    quote_response.json.return_value = [{"price": 100.0}]

    mock_get.side_effect = [profile_response, quote_response]
    result = get_company_data_for_ticker("TEST")
    assert result["name"] is None


##############################################################################################

# NOTE: here is an example test with a mock
# this decorator tells us precisely which module and method we are patching
# @patch("app.api.fmp_client.requests.get")
# def test_get_company_data_for_ticker(mock_get):  # you have to pass in mock_get as an argument
#     # Mock the first API call to FMP /profile/AAPL
#     mock_fmp_response = Mock()
#     mock_fmp_response.json.return_value = [{
#         "companyName": "The Cheesecake Factory",
#         "description": "Cheesecake",
#         . . .
#     }]

#     # Set the mock to return this response
#     mock_get.return_value = mock_fmp_response

#     result = get_company_data_for_ticker("AAPL")

#     assert result["companyName"] == "The Cheesecake Factory"
#     assert result["description"] == "Cheesecake"
#     assert result["price"] == 200.0
#     assert result["symbol"] == "AAPL"
