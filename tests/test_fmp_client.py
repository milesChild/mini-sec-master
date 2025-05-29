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

# . . .

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
