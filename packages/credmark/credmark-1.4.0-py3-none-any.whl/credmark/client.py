import os
import ssl
from typing import Dict, Union

from .api.defi_api import DefiApi
from .api.portfolio_api import PortfolioApi
from .api.token_api import TokenApi
from .api.utilities import Utilities


class Credmark:
    """A class for keeping track of data related to the API

    Attributes:
        base_url: The base URL for the API, all requests are made to a relative path to this URL
        cookies: A dictionary of cookies to be sent with every request
        headers: A dictionary of headers to be sent with every request
        timeout: The maximum amount of a time in seconds a request can take. API functions will raise
            httpx.TimeoutException if this is exceeded.
        verify_ssl: Whether or not to verify the SSL certificate of the API server. This should be True in production,
            but can be set to False for testing purposes.
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document.
        follow_redirects: Whether or not to follow redirects. Default value is True.
    """

    def __init__(
        self,
        base_url: str = "https://gateway.credmark.com",
        cookies: Union[Dict[str, str], None] = None,
        headers: Union[Dict[str, str], None] = None,
        timeout: float = 1800.0,
        verify_ssl: Union[str, bool, ssl.SSLContext] = True,
        follow_redirects: bool = True,
        api_key: Union[str, None] = os.getenv("CREDMARK_API_KEY"),
        prefix: str = "Bearer",
        auth_header_name: str = "Authorization",
    ):
        cookies = cookies if cookies is not None else {}
        headers = headers if headers is not None else {}

        self.base_url = base_url
        self.cookies = cookies
        self.headers = headers
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.follow_redirects = follow_redirects
        self.api_key = api_key
        self.prefix = prefix
        self.auth_header_name = auth_header_name

        self.utilities = Utilities(client=self)
        self.defi_api = DefiApi(client=self)
        self.token_api = TokenApi(client=self)
        self.portfolio_api = PortfolioApi(client=self)

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in all endpoints"""
        if not self.api_key:
            return {**self.headers}
        auth_header_value = f"{self.prefix} {self.api_key}" if self.prefix else self.api_key
        return {self.auth_header_name: auth_header_value, **self.headers}

    def get_cookies(self) -> Dict[str, str]:
        return {**self.cookies}

    def get_timeout(self) -> float:
        return self.timeout
