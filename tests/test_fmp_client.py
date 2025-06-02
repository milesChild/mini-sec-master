"""
Unit tests for the FMP client.
"""

import pytest

from app.api.fmp_client import get_company_data_for_ticker


# NOTE: Starter test for now
def test_raises_value_error_for_invalid_ticker():
    with pytest.raises(ValueError):
        get_company_data_for_ticker(1234583.0)

# test that the function raises an error when an invalid ticker is passed

# test that the function raises an error when the ticker is not found

# test_valid_ticker_returns_complete_data - Check if AAPL returns all expected fields

# test_different_valid_tickers - Test multiple known companies (MSFT, GOOGL, etc)

# test_ticker_case_insensitive - Test that 'aapl' and 'AAPL' give same results

# test_ticker_with_whitespace - Test that ' AAPL ' is handled correctly

# test_empty_ticker_raises_error - Test empty string input

# test_none_ticker_raises_error - Test None input

# test_invalid_ticker_format - Test ticker with invalid characters like '$AAPL'

# test_extremely_long_ticker - Test unreasonably long ticker string

# test_invalid_api_key - Verify correct error when API key is invalid

# test_missing_api_key - Verify error when API key environment variable is missing

# test_rate_limit_exceeded - Test handling of 429 rate limit response

# test_api_timeout - Test handling of API timeout

# test_api_5xx_error - Test handling of server errors

# test_network_connection_error - Test handling of network connectivity issues

# test_missing_company_name - Test handling when API response missing company name

# test_missing_description - Test handling when API response missing description

# test_missing_price - Test handling when API response missing price

# test_null_values_in_response - Test handling of null values in API response

# test_malformed_json_response - Test handling of invalid JSON in API response

# test_response_contains_required_fields - Verify all required fields are present

# test_price_is_numeric - Verify price field is a valid number

# test_currency_is_usd - Verify currency field is always 'USD'

# test_description_is_string - Verify description is a valid string

# test_name_is_string - Verify company name is a valid string        


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
