"""Tests for OneTracker-API Models."""
import json
import datetime
import pytest

from onetracker_api.exceptions import OneTrackerError

from onetracker_api.models import  (
    SessionObject,
    TrackingEvent,
    AuthenticationTokenResponse,
    Parcel,
    ListParcelsResponse,
    GetParcelResponse,
    DeleteParcelResponse,
)

from . import load_fixture

AUTHENTICATION_TOKEN_RESPONSE = json.loads(load_fixture("login.json"))
GET_PARCEL_RESPONSE = json.loads(load_fixture("get_parcel.json"))
LIST_PARCELS_RESPONSE = json.loads(load_fixture("list_parcels.json"))
DELETE_PARCEL_RESPONSE = json.loads(load_fixture("delete_parcel.json"))

def test_session_object() -> None:
    """Test the SessionObject model"""
    session_object = SessionObject.from_dict(AUTHENTICATION_TOKEN_RESPONSE["session"])

    assert session_object
    assert type(session_object) == SessionObject
    assert session_object.token == "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW"
    assert session_object.user_id == 156
    assert session_object.expiration == datetime.datetime(2020, 8, 3, 3, 15, 54)

def test_tracking_event() -> None:
    """Test the TrackingEvent model"""
    tracking_event = TrackingEvent.from_dict(GET_PARCEL_RESPONSE["parcel"]["tracking_events"][0])

    assert tracking_event
    assert type(tracking_event) == TrackingEvent
    assert tracking_event.id == 5699
    assert tracking_event.parcel_id == 938
    assert tracking_event.carrier_id == ""
    assert tracking_event.carrier_name == ""
    assert tracking_event.status == "delivered"
    assert tracking_event.text == "Delivered. Signed for by: REF 39609023995"
    assert tracking_event.location == "MEMPHIS, TN"
    assert tracking_event.latitude == 35.149536
    assert tracking_event.longitude == -90.04898
    assert tracking_event.time == datetime.datetime(2020, 1, 17, 16, 30, 0)
    assert tracking_event.time_added == datetime.datetime(2020, 5, 5, 5, 47, 56)

def test_parcel() -> None:
    """Test the Parcel model"""
    parcel = Parcel.from_dict(GET_PARCEL_RESPONSE["parcel"])

    assert parcel
    assert type(parcel) == Parcel
    assert parcel.id == 938
    assert parcel.user_id == 6
    assert parcel.email_id == 0
    assert parcel.email_sender == ""
    assert parcel.retailer_name == ""
    assert parcel.description == ""
    assert parcel.notification_level == 1
    assert parcel.is_archived == False
    assert parcel.carrier == "FedEx"
    assert parcel.carrier_name == ""
    assert parcel.carrier_redirection_available == False
    assert parcel.tracker_cached == False
    assert parcel.tracking_id == "123456789012"
    assert parcel.tracking_url == ""
    assert parcel.tracking_status == "delivered"
    assert parcel.tracking_status_description == ""
    assert parcel.tracking_status_text == ""
    assert parcel.tracking_extra_info == ""
    assert parcel.tracking_location == "MEMPHIS, TN"
    assert parcel.tracking_time_estimated == datetime.datetime(1001, 1, 1, 0, 0, 0)
    assert parcel.tracking_time_delivered == datetime.datetime(2020, 1, 17, 16, 30, 0)
    assert parcel.tracking_lock == False
    assert parcel.time_added == datetime.datetime(2020, 5, 5, 4, 42, 39)
    assert parcel.time_updated == datetime.datetime(2020, 5, 5, 5, 47, 56)
    assert type(parcel.tracking_events) == list
    assert len(parcel.tracking_events) == 2
    assert parcel.tracking_events[0]
    assert type(parcel.tracking_events[0]) == TrackingEvent
    assert parcel.tracking_events[0].id == 5699
    assert parcel.tracking_events[0].parcel_id == 938
    assert parcel.tracking_events[0].carrier_id == ""
    assert parcel.tracking_events[0].carrier_name == ""
    assert parcel.tracking_events[0].status == "delivered"
    assert parcel.tracking_events[0].text == "Delivered. Signed for by: REF 39609023995"
    assert parcel.tracking_events[0].location == "MEMPHIS, TN"
    assert parcel.tracking_events[0].latitude == 35.149536
    assert parcel.tracking_events[0].longitude == -90.04898
    assert parcel.tracking_events[0].time == datetime.datetime(2020, 1, 17, 16, 30, 0)
    assert parcel.tracking_events[0].time_added == datetime.datetime(2020, 5, 5, 5, 47, 56)
    assert parcel.tracking_events[1]
    assert type(parcel.tracking_events[1]) == TrackingEvent
    assert parcel.tracking_events[1].id == 5697
    assert parcel.tracking_events[1].parcel_id == 938
    assert parcel.tracking_events[1].carrier_id == ""
    assert parcel.tracking_events[1].carrier_name == ""
    assert parcel.tracking_events[1].status == "pre_transit"
    assert parcel.tracking_events[1].text == "Shipment information sent to FedEx"
    assert parcel.tracking_events[1].location == ""
    assert parcel.tracking_events[1].latitude == 0
    assert parcel.tracking_events[1].longitude == 0
    assert parcel.tracking_events[1].time == datetime.datetime(2019, 12, 9, 7, 50, 11)
    assert parcel.tracking_events[1].time_added == datetime.datetime(2020, 5, 5, 5, 47, 56)

def test_authentication_token_response() -> None:
    """Test the AuthenticationTokenResponse model"""
    authentication_token_response = AuthenticationTokenResponse.from_dict(AUTHENTICATION_TOKEN_RESPONSE)

    assert authentication_token_response
    assert type(authentication_token_response) == AuthenticationTokenResponse
    assert authentication_token_response.message == "ok"
    assert authentication_token_response.session
    assert type(authentication_token_response.session) == SessionObject
    assert authentication_token_response.session.token == "eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW"
    assert authentication_token_response.session.user_id == 156
    assert authentication_token_response.session.expiration == datetime.datetime(2020, 8, 3, 3, 15, 54)

def test_authentication_token_error_response() -> None:
    """Test the AuthenticationTokenResponse model with error message"""
    with pytest.raises(OneTrackerError):
        AuthenticationTokenResponse.from_dict({'message': 'error'})

def test_list_parcels_response() -> None:
    """Test the ListParcelsResponse model"""
    list_parcels_response = ListParcelsResponse.from_dict(LIST_PARCELS_RESPONSE)

    assert list_parcels_response
    assert type(list_parcels_response) == ListParcelsResponse
    assert list_parcels_response.message == "ok"
    assert list_parcels_response.parcels
    assert type(list_parcels_response.parcels) == list
    assert len(list_parcels_response.parcels) == 1
    assert list_parcels_response.parcels[0]
    assert type(list_parcels_response.parcels[0]) == Parcel
    assert list_parcels_response.parcels[0].id == 174
    assert list_parcels_response.parcels[0].user_id == 6
    assert list_parcels_response.parcels[0].email_id == 183
    assert list_parcels_response.parcels[0].email_sender == "example.com"
    assert list_parcels_response.parcels[0].retailer_name == "Example"
    assert list_parcels_response.parcels[0].description == "Camera"
    assert list_parcels_response.parcels[0].notification_level == 1
    assert list_parcels_response.parcels[0].is_archived == False
    assert list_parcels_response.parcels[0].carrier == "FedEx"
    assert list_parcels_response.parcels[0].carrier_name == "FedEx"
    assert list_parcels_response.parcels[0].carrier_redirection_available == True
    assert list_parcels_response.parcels[0].tracker_cached == False
    assert list_parcels_response.parcels[0].tracking_id == "407072905722"
    assert list_parcels_response.parcels[0].tracking_url == ""
    assert list_parcels_response.parcels[0].tracking_status == "delivered"
    assert list_parcels_response.parcels[0].tracking_status_description == ""
    assert list_parcels_response.parcels[0].tracking_status_text == ""
    assert list_parcels_response.parcels[0].tracking_extra_info == ""
    assert list_parcels_response.parcels[0].tracking_location == "Sunnyvale, CA"
    assert list_parcels_response.parcels[0].tracking_time_estimated == datetime.datetime(2018, 8, 8, 20, 0, 0)
    assert list_parcels_response.parcels[0].tracking_time_delivered == datetime.datetime(2018, 8, 8, 15, 51, 0)
    assert list_parcels_response.parcels[0].tracking_lock == False
    assert list_parcels_response.parcels[0].time_added == datetime.datetime(2018, 8, 7, 0, 50, 30)
    assert list_parcels_response.parcels[0].time_updated == datetime.datetime(2018, 8, 18, 20, 1, 23)
    assert type(list_parcels_response.parcels[0].tracking_events) == list
    assert len(list_parcels_response.parcels[0].tracking_events) == 0

def test_list_parcels_error_response() -> None:
    """Test the ListParcelsResponse model with error message"""
    with pytest.raises(OneTrackerError):
        ListParcelsResponse.from_dict({'message': 'error'})

def test_get_parcel_response() -> None:
    """Test the GetParcelResponse model"""
    get_parcel_response = GetParcelResponse.from_dict(GET_PARCEL_RESPONSE)

    assert get_parcel_response
    assert type(get_parcel_response) == GetParcelResponse
    assert get_parcel_response.message == "ok"
    assert get_parcel_response.parcel
    assert type(get_parcel_response.parcel) == Parcel
    assert get_parcel_response.parcel.id == 938
    assert get_parcel_response.parcel.user_id == 6
    assert get_parcel_response.parcel.email_id == 0
    assert get_parcel_response.parcel.email_sender == ""
    assert get_parcel_response.parcel.retailer_name == ""
    assert get_parcel_response.parcel.description == ""
    assert get_parcel_response.parcel.notification_level == 1
    assert get_parcel_response.parcel.is_archived == False
    assert get_parcel_response.parcel.carrier == "FedEx"
    assert get_parcel_response.parcel.carrier_name == ""
    assert get_parcel_response.parcel.carrier_redirection_available == False
    assert get_parcel_response.parcel.tracker_cached == False
    assert get_parcel_response.parcel.tracking_id == "123456789012"
    assert get_parcel_response.parcel.tracking_url == ""
    assert get_parcel_response.parcel.tracking_status == "delivered"
    assert get_parcel_response.parcel.tracking_status_description == ""
    assert get_parcel_response.parcel.tracking_status_text == ""
    assert get_parcel_response.parcel.tracking_extra_info == ""
    assert get_parcel_response.parcel.tracking_location == "MEMPHIS, TN"
    assert get_parcel_response.parcel.tracking_time_estimated == datetime.datetime(1001, 1, 1, 0, 0, 0)
    assert get_parcel_response.parcel.tracking_time_delivered == datetime.datetime(2020, 1, 17, 16, 30, 0)
    assert get_parcel_response.parcel.tracking_lock == False
    assert get_parcel_response.parcel.time_added == datetime.datetime(2020, 5, 5, 4, 42, 39)
    assert get_parcel_response.parcel.time_updated == datetime.datetime(2020, 5, 5, 5, 47, 56)
    assert type(get_parcel_response.parcel.tracking_events) == list
    assert len(get_parcel_response.parcel.tracking_events) == 2
    assert get_parcel_response.parcel.tracking_events[0]
    assert type(get_parcel_response.parcel.tracking_events[0]) == TrackingEvent
    assert get_parcel_response.parcel.tracking_events[0].id == 5699
    assert get_parcel_response.parcel.tracking_events[0].parcel_id == 938
    assert get_parcel_response.parcel.tracking_events[0].carrier_id == ""
    assert get_parcel_response.parcel.tracking_events[0].carrier_name == ""
    assert get_parcel_response.parcel.tracking_events[0].status == "delivered"
    assert get_parcel_response.parcel.tracking_events[0].text == "Delivered. Signed for by: REF 39609023995"
    assert get_parcel_response.parcel.tracking_events[0].location == "MEMPHIS, TN"
    assert get_parcel_response.parcel.tracking_events[0].latitude == 35.149536
    assert get_parcel_response.parcel.tracking_events[0].longitude == -90.04898
    assert get_parcel_response.parcel.tracking_events[0].time == datetime.datetime(2020, 1, 17, 16, 30, 0)
    assert get_parcel_response.parcel.tracking_events[0].time_added == datetime.datetime(2020, 5, 5, 5, 47, 56)
    assert get_parcel_response.parcel.tracking_events[1]
    assert type(get_parcel_response.parcel.tracking_events[1]) == TrackingEvent
    assert get_parcel_response.parcel.tracking_events[1].id == 5697
    assert get_parcel_response.parcel.tracking_events[1].parcel_id == 938
    assert get_parcel_response.parcel.tracking_events[1].carrier_id == ""
    assert get_parcel_response.parcel.tracking_events[1].carrier_name == ""
    assert get_parcel_response.parcel.tracking_events[1].status == "pre_transit"
    assert get_parcel_response.parcel.tracking_events[1].text == "Shipment information sent to FedEx"
    assert get_parcel_response.parcel.tracking_events[1].location == ""
    assert get_parcel_response.parcel.tracking_events[1].latitude == 0
    assert get_parcel_response.parcel.tracking_events[1].longitude == 0
    assert get_parcel_response.parcel.tracking_events[1].time == datetime.datetime(2019, 12, 9, 7, 50, 11)
    assert get_parcel_response.parcel.tracking_events[1].time_added == datetime.datetime(2020, 5, 5, 5, 47, 56)

def test_get_parcel_error_response() -> None:
    """Test the GetParcelResponse model with error message"""
    with pytest.raises(OneTrackerError):
        GetParcelResponse.from_dict({'message': 'error'})

def test_delete_parcel_response() -> None:
    """Test the DeleteParcelResponse model"""
    delete_parcel_response = DeleteParcelResponse.from_dict(DELETE_PARCEL_RESPONSE)

    assert delete_parcel_response
    assert type(delete_parcel_response) == DeleteParcelResponse
    assert delete_parcel_response.message == "ok"

def test_delete_parcel_error_response() -> None:
    """Test the DeleteParcelResponse model with error message"""
    with pytest.raises(OneTrackerError):
        DeleteParcelResponse.from_dict({'message': 'error'})