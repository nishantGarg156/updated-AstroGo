def check(response, expected_status_code, expected_text=None, api_name=None):
    """
    Validate response status code and optional expected text.
    On failure, print API name and request URL for debugging.

    :param response: Response object
    :param expected_status_code: int
    :param expected_text: str (optional)
    :param api_name: str (optional) - friendly API name
    :return: bool
    """
    if response.status_code != expected_status_code:
        print(f"[FAIL] Status code mismatch in API '{api_name or 'Unknown API'}': expected {expected_status_code}, got {response.status_code}")
        print(f"Request URL: {response.request.url}")
        return False

    if expected_text and expected_text.lower() not in response.text.lower():
        print(f"[FAIL] Expected text '{expected_text}' not found in API '{api_name or 'Unknown API'}' response body.")
        print(f"Request URL: {response.request.url}")
        return False

    print(f"[PASS] Response validated successfully for API ")
    return True
