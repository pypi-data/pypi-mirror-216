"""Asynchronous client for the Länderübergreifendes Hochwasserportal API."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from typing import Any

import async_timeout
from aiohttp.client import ClientError, ClientResponseError, ClientSession
from yarl import URL

from .exceptions import LHPConnectionError, LHPError
from .models import CurrentWaterLevel


@dataclass
class LHPClient:
    """Main class for the LHP API."""

    # Request timeout in seconds.
    request_timeout: float = 10.0

    # Custom client session to use for requests.
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(self, url: URL, data: dict[str, Any]) -> dict[str, Any]:
        """Handle a request to the LHP API.

        A generic method for sending/handling HTTP requests done against
        the public LHP API.

        Args:
            url: URL to call.
            data: A Python dictionary with data to post.

        Returns:
            A Python dictionary (JSON decoded) with the response from
            the API.

        Raises:
            LHPConnectionError: An error occurred while communicating with
                the LHP API.
            LHPError: Received an unexpected response from the LHP
                API.
        """
        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.post(url, data=data)
        except asyncio.TimeoutError as exception:
            raise LHPConnectionError(
                "Timeout occurred while connecting to the LHP API"
            ) from exception
        except (
            ClientError,
            ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise LHPConnectionError(
                "Error occurred while communicating with LHP API"
            ) from exception
        content_type = response.headers.get("Content-Type", "")
        if (response.status // 100) in [4, 5]:
            if "text/html; charset=UTF-8" in content_type:
                data = await response.json(content_type=None)
                response.close()
                if data.get("error") is True and (reason := data.get("reason")):
                    raise LHPError(reason)
                raise LHPError(response.status, data)
            contents = await response.read()
            response.close()
            raise LHPError(response.status, {"message": contents.decode("utf8")})

        if "text/html; charset=UTF-8" not in content_type:
            text = await response.text()
            raise LHPError(
                "Unexpected response from the LHP API",
                {"Content-Type": content_type, "response": text},
            )
        return await response.json(content_type=None)

    async def currentwaterlevel(
        self,
        *,
        pgnr: str,
    ) -> CurrentWaterLevel:
        """Get current water level.

        Args:
            pgnr: The name of the water level measurement station.

        Returns:
            A CurrentWaterLevel object.
        """
        url = URL(
            "https://hochwasserzentralen.api.proxy.bund.dev/"
            "webservices/get_infospegel.php"
        )
        data = {"pgnr": pgnr}
        result = await self._request(url=url, data=data)

        # Separate value from unit.
        result["W_float"] = float(result["W"].split()[0])

        return CurrentWaterLevel.parse_obj(result)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> LHPClient:
        """Async enter.

        Returns:
            The LHP object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
