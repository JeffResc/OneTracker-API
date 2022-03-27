"""Tests for OneTracker Interface."""
import pytest
import datetime
from datetime import timedelta
from aiohttp import ClientSession
from onetracker_api import OneTracker, OneTrackerError

from onetracker_api import (
    OneTrackerError,
    OneTrackerAuthenticationError,
    OneTrackerAuthenticationSessionError,
    OneTrackerAuthenticationSessionExpiredError,
)
from onetracker_api.models import  (
    SessionObject,
    TrackingEvent,
    AuthenticationTokenResponse,
    Parcel,
    ListParcelsResponse,
    GetParcelResponse,
    DeleteParcelResponse,
    ListCarriersResponse,
)

from . import load_fixture

MATCH_HOST = "api.onetracker.app"

@pytest.mark.asyncio
async def test_loop():
    """Test loop usage is handled correctly."""
    async with OneTracker() as onetracker:
        assert isinstance(onetracker, OneTracker)

@pytest.mark.asyncio
async def test_successful_authentication_session(aresponses):
    """Test successful authentication session."""
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
        onetracker = OneTracker(session=session)
        response = await onetracker.login("", "")
        assert response
        assert type(response) == AuthenticationTokenResponse
        assert response.message == "ok"
        assert response.session
        assert type(response.session) == SessionObject
        assert response.session.user_id == 156
        assert response.session.token == "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW"
        assert response.session.expiration == datetime.datetime(2020, 8, 3, 3, 15, 54)
        assert onetracker.session_object
        assert type(onetracker.session_object) == SessionObject
        assert onetracker.session_object.user_id == 156
        assert onetracker.session_object.token == "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW"
        assert onetracker.session_object.expiration == datetime.datetime(2020, 8, 3, 3, 15, 54)

@pytest.mark.asyncio
async def test_successful_authentication_session_with_session_object():
    """Test successful authentication session with session object."""
    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": "2020-08-03T03:15:54.677770006Z"})
        onetracker = OneTracker(session=session, session_object = session_object)
        assert type(onetracker.session_object) == SessionObject
        assert onetracker.session_object.user_id == 156
        assert onetracker.session_object.token == "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW"
        assert onetracker.session_object.expiration == datetime.datetime(2020, 8, 3, 3, 15, 54)

@pytest.mark.asyncio
async def test_failed_authentication_session(aresponses):
    """Test failed authentication session."""
    aresponses.add(
        MATCH_HOST,
        "/auth/token",
        "POST",
        aresponses.Response(
            status=400,
            headers={"Content-Type": "application/json"},
            text='{"message": "Key: \'UserSignInUp.Email\' Error:Field validation for \'Email\' failed on the \'required\' tag"}',
        ),
    )

    async with ClientSession() as session:
        onetracker = OneTracker(session=session)
        with pytest.raises(OneTrackerError):
            await onetracker.login("", "")

@pytest.mark.asyncio
async def test_list_parcels(aresponses):
    """Test list parcels."""
    aresponses.add(
        MATCH_HOST,
        "/parcels",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("list_parcels.json"),
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        response = await onetracker.list_parcels()
        assert response
        assert type(response) == ListParcelsResponse
        assert response.message == "ok"
        assert response.parcels
        assert type(response.parcels) == list
        assert len(response.parcels) == 1
        assert response.parcels[0]
        assert type(response.parcels[0]) == Parcel
        assert response.parcels[0].id == 174
        assert response.parcels[0].user_id == 6
        assert response.parcels[0].email_id == 183
        assert response.parcels[0].email_sender == "example.com"
        assert response.parcels[0].retailer_name == "Example"
        assert response.parcels[0].description == "Camera"
        assert response.parcels[0].notification_level == 1
        assert response.parcels[0].is_archived == False
        assert response.parcels[0].carrier == "FedEx"
        assert response.parcels[0].carrier_name == "FedEx"
        assert response.parcels[0].carrier_redirection_available == True
        assert response.parcels[0].tracker_cached == False
        assert response.parcels[0].tracking_id == "407072905722"
        assert response.parcels[0].tracking_url == ""
        assert response.parcels[0].tracking_status == "delivered"
        assert response.parcels[0].tracking_status_description == ""
        assert response.parcels[0].tracking_status_text == ""
        assert response.parcels[0].tracking_extra_info == ""
        assert response.parcels[0].tracking_location == "Sunnyvale, CA"
        assert response.parcels[0].tracking_time_estimated == datetime.datetime(2018, 8, 8, 20, 0, 0)
        assert response.parcels[0].tracking_time_delivered == datetime.datetime(2018, 8, 8, 15, 51, 0)
        assert response.parcels[0].tracking_lock == False
        assert response.parcels[0].time_added == datetime.datetime(2018, 8, 7, 0, 50, 30)
        assert response.parcels[0].time_updated == datetime.datetime(2018, 8, 18, 20, 1, 23)
        assert type(response.parcels[0].tracking_events) == list
        assert len(response.parcels[0].tracking_events) == 0

@pytest.mark.asyncio
async def test_list_parcels_empty_json(aresponses):
    """Test list parcels empty response."""
    aresponses.add(
        MATCH_HOST,
        "/parcels",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.list_parcels()

@pytest.mark.asyncio
async def test_list_parcels_invalid_json_response(aresponses):
    """Test list parcels."""
    aresponses.add(
        MATCH_HOST,
        "/parcels",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='not json',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.list_parcels()

@pytest.mark.asyncio
async def test_list_parcels_no_session_login(aresponses):
    """Test list parcels without logging in."""
    aresponses.add(
        MATCH_HOST,
        "/parcels",
        "GET",
        aresponses.Response(
            status=401,
            headers={"Content-Type": "application/json"},
            text='{"message":"Authentication required"}',
        ),
    )

    async with ClientSession() as session:
        onetracker = OneTracker(session=session)
        with pytest.raises(OneTrackerAuthenticationSessionError):
            await onetracker.list_parcels()

@pytest.mark.asyncio
async def test_list_parcels_expired_session_login(aresponses):
    """Test list parcels with expired login session."""
    aresponses.add(
        MATCH_HOST,
        "/parcels",
        "GET",
        aresponses.Response(
            status=401,
            headers={"Content-Type": "application/json"},
            text='{"message":"Expired login session"}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerAuthenticationSessionExpiredError):
            await onetracker.list_parcels()

@pytest.mark.asyncio
async def test_list_parcels_invalid_api_token(aresponses):
    """Test list parcels with invalid API token."""
    aresponses.add(
        MATCH_HOST,
        "/parcels",
        "GET",
        aresponses.Response(
            status=401,
            headers={"Content-Type": "application/json"},
            text='{"message":"Invalid API token"}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerAuthenticationError):
            await onetracker.list_parcels()

@pytest.mark.asyncio
async def test_get_parcel(aresponses):
    """Test get parcel."""
    aresponses.add(
        MATCH_HOST,
        "/parcels/174",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("get_parcel.json"),
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        response = await onetracker.get_parcel(id=174)
        assert response
        assert type(response) == GetParcelResponse
        assert response.message == "ok"
        assert response.parcel
        assert type(response.parcel) == Parcel
        assert response.parcel.id == 938
        assert response.parcel.user_id == 6
        assert response.parcel.email_id == 0
        assert response.parcel.email_sender == ""
        assert response.parcel.retailer_name == ""
        assert response.parcel.description == ""
        assert response.parcel.notification_level == 1
        assert response.parcel.is_archived == False
        assert response.parcel.carrier == "FedEx"
        assert response.parcel.carrier_name == ""
        assert response.parcel.carrier_redirection_available == False
        assert response.parcel.tracker_cached == False
        assert response.parcel.tracking_id == "123456789012"
        assert response.parcel.tracking_url == ""
        assert response.parcel.tracking_status == "delivered"
        assert response.parcel.tracking_status_description == ""
        assert response.parcel.tracking_status_text == ""
        assert response.parcel.tracking_extra_info == ""
        assert response.parcel.tracking_location == "MEMPHIS, TN"
        assert response.parcel.tracking_time_estimated == datetime.datetime(1001, 1, 1, 0, 0, 0)
        assert response.parcel.tracking_time_delivered == datetime.datetime(2020, 1, 17, 16, 30, 0)
        assert response.parcel.tracking_lock == False
        assert response.parcel.time_added == datetime.datetime(2020, 5, 5, 4, 42, 39)
        assert response.parcel.time_updated == datetime.datetime(2020, 5, 5, 5, 47, 56)
        assert type(response.parcel.tracking_events) == list
        assert len(response.parcel.tracking_events) == 2
        assert response.parcel.tracking_events[0]
        assert type(response.parcel.tracking_events[0]) == TrackingEvent
        assert response.parcel.tracking_events[0].id == 5699
        assert response.parcel.tracking_events[0].parcel_id == 938
        assert response.parcel.tracking_events[0].carrier_id == ""
        assert response.parcel.tracking_events[0].carrier_name == ""
        assert response.parcel.tracking_events[0].status == "delivered"
        assert response.parcel.tracking_events[0].text == "Delivered. Signed for by: REF 39609023995"
        assert response.parcel.tracking_events[0].location == "MEMPHIS, TN"
        assert response.parcel.tracking_events[0].latitude == 35.149536
        assert response.parcel.tracking_events[0].longitude == -90.04898
        assert response.parcel.tracking_events[0].time == datetime.datetime(2020, 1, 17, 16, 30, 0)
        assert response.parcel.tracking_events[0].time_added == datetime.datetime(2020, 5, 5, 5, 47, 56)
        assert response.parcel.tracking_events[1]
        assert type(response.parcel.tracking_events[1]) == TrackingEvent
        assert response.parcel.tracking_events[1].id == 5697
        assert response.parcel.tracking_events[1].parcel_id == 938
        assert response.parcel.tracking_events[1].carrier_id == ""
        assert response.parcel.tracking_events[1].carrier_name == ""
        assert response.parcel.tracking_events[1].status == "pre_transit"
        assert response.parcel.tracking_events[1].text == "Shipment information sent to FedEx"
        assert response.parcel.tracking_events[1].location == ""
        assert response.parcel.tracking_events[1].latitude == 0
        assert response.parcel.tracking_events[1].longitude == 0
        assert response.parcel.tracking_events[1].time == datetime.datetime(2019, 12, 9, 7, 50, 11)
        assert response.parcel.tracking_events[1].time_added == datetime.datetime(2020, 5, 5, 5, 47, 56)

@pytest.mark.asyncio
async def test_get_parcel_empty_json(aresponses):
    """Test get parcel empty response."""
    aresponses.add(
        MATCH_HOST,
        "/parcel/174",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.get_parcel(id=174)

@pytest.mark.asyncio
async def test_get_parcel_not_found(aresponses):
    """Test get parcel with 404 parcel."""
    aresponses.add(
        MATCH_HOST,
        "/parcels/174",
        "GET",
        aresponses.Response(
            status=404,
            headers={"Content-Type": "application/json"},
            text='{"message":"Parcel not found for this user"}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.get_parcel(id=174)

@pytest.mark.asyncio
async def test_delete_parcel(aresponses):
    """Test delete parcel."""
    aresponses.add(
        MATCH_HOST,
        "/parcels/174",
        "DELETE",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"message":"ok"}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        response = await onetracker.delete_parcel(id=174)
        assert response
        assert type(response) == DeleteParcelResponse
        assert response.message == "ok"

@pytest.mark.asyncio
async def test_delete_parcel_no_id(aresponses):
    """Test delete parcel."""
    aresponses.add(
        MATCH_HOST,
        "/parcels/174",
        "DELETE",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"message":"ok"}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.delete_parcel(id=None)

@pytest.mark.asyncio
async def test_delete_parcel_non_int_id(aresponses):
    """Test delete parcel."""
    aresponses.add(
        MATCH_HOST,
        "/parcels/174",
        "DELETE",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"message":"ok"}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.delete_parcel(id="abc")

@pytest.mark.asyncio
async def test_delete_parcel_not_found(aresponses):
    """Test delete parcel not found."""
    aresponses.add(
        MATCH_HOST,
        "/parcels/174",
        "DELETE",
        aresponses.Response(
            status=404,
            headers={"Content-Type": "application/json"},
            text='{"message":"Parcel not found for this user"}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.delete_parcel(id=174)

@pytest.mark.asyncio
async def test_delete_parcel_empty_json(aresponses):
    """Test delete parcel empty response."""
    aresponses.add(
        MATCH_HOST,
        "/parcels/174",
        "DELETE",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.delete_parcel(id=174)

@pytest.mark.asyncio
async def test_list_carriers(aresponses):
    """Test list carriers."""
    aresponses.add(
        MATCH_HOST,
        "/carriers",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("carriers.json"),
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        carriers = await onetracker.list_carriers()
        
        assert carriers
        assert type(carriers) == ListCarriersResponse
        assert carriers.message == "ok"
        assert len(carriers.carriers) == 141

@pytest.mark.asyncio
async def test_list_carriers_tracking_id(aresponses):
    """Test list carriers with tracking ID."""
    aresponses.add(
        MATCH_HOST,
        "/carriers",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("carriers.json"),
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        carriers = await onetracker.list_carriers(tracking_id="abc")

        assert carriers
        assert type(carriers) == ListCarriersResponse
        assert carriers.message == "ok"
        assert len(carriers.carriers) == 141

@pytest.mark.asyncio
async def test_list_carriers_empty_json(aresponses):
    """Test list carriers with empty json response."""
    aresponses.add(
        MATCH_HOST,
        "/carriers",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.list_carriers()

@pytest.mark.asyncio
async def test_list_carriers_tracking_id_int(aresponses):
    """Test list carriers with tracking_id as an int, which is invalid."""
    aresponses.add(
        MATCH_HOST,
        "/carriers",
        "GET",
        aresponses.Response(
            status=400,
            headers={"Content-Type": "application/json"},
            text='{}',
        ),
    )

    async with ClientSession() as session:
        session_object = SessionObject.from_dict({"user_id": 156, "token": "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW", "expiration": (datetime.date.today() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')})
        onetracker = OneTracker(session=session, session_object=session_object)
        with pytest.raises(OneTrackerError):
            await onetracker.list_carriers(tracking_id=1)
