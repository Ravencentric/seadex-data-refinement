from typing import override

import httpx
import stamina


def backoff(error: Exception) -> bool | float:
    """
    Stamina accepts a callable that decides whether something
    should be retried or not:

    True -> Retry with stamina's defaults
    False -> Don't retry
    float -> Retry after this many seconds.
    """
    if isinstance(error, httpx.HTTPStatusError):
        if error.response.status_code == 429:
            return float(error.response.headers["Retry-After"])
        return error.response.is_server_error

    return isinstance(error, httpx.TransportError)


class RetryingTransport(httpx.HTTPTransport):
    """
    A transport wrapper to both retry and keep a track of the number
    of requests made.

    See: <https://www.python-httpx.org/advanced/transports/#custom-transports>
    """

    requests: int = 0
    """Number of requests made."""

    @override
    @stamina.retry(on=backoff, attempts=4, timeout=None)
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.requests += 1
        response = super().handle_request(request)
        # HTTPX normally attaches this later, but our status check needs it now.
        response.request = request
        try:
            response.read()
        finally:
            response.close()
        response.raise_for_status()
        return response


class Client(httpx.Client):
    """Preconfigured client."""

    transport: RetryingTransport

    def __init__(self) -> None:
        self.transport = RetryingTransport()
        super().__init__(transport=self.transport, timeout=60)

    @property
    def requests(self) -> int:
        return self.transport.requests
