"""Internal client for connecting to an OneTracker installation."""
import asyncio
import json
import aiohttp
import async_timeout
from socket import gaierror as SocketGIAError
from yarl import URL
from typing import Any, Dict, Optional

from .__version__ import __version__
from .exceptions import (
    OneTrackerClientError,
    OneTrackerConnectionError,
    OneTrackerError,
    OneTrackerInternalServerError,
    OneTrackerAuthenticationError,
)
from .models import SessionObject

class Client:
    def __init__(
        self,
        request_timeout: int = 8,
        session: aiohttp.client.ClientSession = None,
        user_agent: str = None,
        session_object: SessionObject = None,
    ) -> None:
        """Initialize connection to OneTracker."""
        self._session = session
        self._close_session = False

        self.request_timeout = request_timeout
        self.user_agent = user_agent

        if user_agent is None:
            self.user_agent = f"OneTracker-API/{__version__}"

        self.session_object = session_object

        self.scheme = "https"
        self.host = "api.onetracker.app"

    async def _request(
        self,
        uri: str = '',
        method: str = 'GET',
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """
        Handles a request to the API.

        Args:

        uri: The URI to request.

        method: The HTTP method to use.

        data: The data to send.

        headers: The headers to send.

        Returns:
            The response.
        """

        url = URL.build(
            scheme=self.scheme, host=self.host
        ).join(URL(uri))

        api_headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
        }

        if headers is not None:
            headers.update(api_headers)
        else:
            headers = api_headers

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    method,
                    url,
                    data=data,
                    headers=headers,
                    ssl=(self.scheme == "https"),
                )
        except asyncio.TimeoutError as exception:
            raise OneTrackerConnectionError(
                "Timeout occurred while connecting to API"
            ) from exception
        except (aiohttp.ClientError, SocketGIAError) as exception: # pragma: no cover
            raise OneTrackerConnectionError(
                "Error occurred while communicating with API"
            ) from exception

        if (response.status // 100) in [4, 5]:
            data = await response.json()
            error_message = data.get("message", "")
            if response.status == 401 and error_message == "Invalid API token":
                raise OneTrackerAuthenticationError(error_message)
            elif response.status >= 400 and response.status <= 499:
                raise OneTrackerClientError(f"{response.status}: {error_message}")
            elif response.status >= 500 and response.status <= 599:
                raise OneTrackerInternalServerError(f"{response.status}: {error_message}")

        content_type = response.headers.get("Content-Type", "")


        try:
            data = await response.json()
            return data
        except json.JSONDecodeError as e:
            raise OneTrackerError(
                "Error decoding JSON response",
                {
                    "content-type": content_type,
                    "message": e.msg,
                    "status-code": response.status,
                },
            )

    async def close_session(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "Client":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close_session()
