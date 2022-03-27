"""Tests for OneTracker-API Client."""
import asyncio
import pytest

from aiohttp import ClientSession, ClientError

from onetracker_api import (
    Client,
    OneTrackerError,
    OneTrackerConnectionError,
    OneTrackerInternalServerError,
    OneTrackerClientError,
    OneTrackerAuthenticationError,
)

MATCH_HOST = "api.onetracker.app"

@pytest.mark.asyncio
async def test_json_request(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/auth/token",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"message": "ok", "session": {"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": "2020-08-03T03:15:54.677770006Z"}}',
        ),
    )

    async with ClientSession() as session:
        client = Client(session=session)
        response = await client._request("/auth/token", "POST", {"email": "", "password": ""})
        assert response
        assert type(response) == dict
        assert response.get("message") == "ok"
        assert response.get("session")
        assert type(response.get("session")) == dict
        assert response.get("session").get("user_id") == 156
        assert response.get("session").get("token") == "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW"
        assert response.get("session").get("expiration") == "2020-08-03T03:15:54.677770006Z"

@pytest.mark.asyncio
async def test_internal_session(aresponses):
    """Test JSON response is handled correctly with internal session."""
    aresponses.add(
        MATCH_HOST,
        "/auth/token",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"message": "ok", "session": {"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": "2020-08-03T03:15:54.677770006Z"}}',
        ),
    )

    async with Client() as client:
        response = await client._request("/auth/token", "POST", {"email": "", "password": ""})
        assert response
        assert type(response) == dict
        assert response.get("message") == "ok"
        assert response.get("session")
        assert type(response.get("session")) == dict
        assert response.get("session").get("user_id") == 156
        assert response.get("session").get("token") == "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW"
        assert response.get("session").get("expiration") == "2020-08-03T03:15:54.677770006Z"

@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout from the API."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        await asyncio.sleep(2)
        return aresponses.Response(body="Timeout!")

    aresponses.add(MATCH_HOST, "/auth/token", "POST", response_handler)

    async with ClientSession() as session:
        client = Client(session=session, request_timeout=1)
        with pytest.raises(OneTrackerConnectionError):
            assert await client._request("/auth/token", "POST", {"email": "", "password": ""})

@pytest.mark.asyncio
async def test_http_error404(aresponses):
    """Test HTTP 404 response handling."""
    aresponses.add(
        MATCH_HOST,
        "/auth/token",
        "POST",
        aresponses.Response(
            status=404,
            headers={"Content-Type": "application/json"},
            text='{"message":"Resource not found. Please update client to the latest version."}',
        ),
    )

    async with ClientSession() as session:
        client = Client(session=session)
        with pytest.raises(OneTrackerClientError):
            assert await client._request("/auth/token", "POST", {"email": "", "password": ""})

@pytest.mark.asyncio
async def test_http_error401(aresponses):
    aresponses.add(
        MATCH_HOST,
        "/auth/token",
        "POST",
        aresponses.Response(
            status=401,
            headers={"Content-Type": "application/json"},
            text='{"message":"Invalid API token"}',
        ),
    )

    async with ClientSession() as session:
        client = Client(session=session)
        with pytest.raises(OneTrackerAuthenticationError):
            assert await client._request("/auth/token", "POST", {"email": "", "password": ""})

@pytest.mark.asyncio
async def test_http_error500(aresponses):
    """Test HTTP 500 response handling."""
    aresponses.add(
        MATCH_HOST,
        "/auth/token",
        "POST",
        aresponses.Response(
            status=500,
            headers={"Content-Type": "application/json"},
            text='{"message":"Internal server error."}',
        ),
    )

    async with ClientSession() as session:
        client = Client(session=session)
        with pytest.raises(OneTrackerInternalServerError):
            assert await client._request("/auth/token", "POST", {"email": "", "password": ""})

@pytest.mark.asyncio
async def test_http_error400(aresponses):
    """Test HTTP 400 response handling."""
    aresponses.add(
        MATCH_HOST,
        "/auth/token",
        "POST",
        aresponses.Response(
            status=400,
            headers={"Content-Type": "application/json"},
            text='{"message":"Bad request."}',
        ),
    )

    async with ClientSession() as session:
        client = Client(session=session)
        with pytest.raises(OneTrackerClientError):
            assert await client._request("/auth/token", "POST", {"email": "", "password": ""})

@pytest.mark.asyncio
async def test_malformed_json(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        MATCH_HOST,
        "/auth/token",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='not_json',
        ),
    )

    async with ClientSession() as session:
        client = Client(session=session)
        with pytest.raises(OneTrackerError):
            assert await client._request("/auth/token", "POST", {"email": "", "password": ""})