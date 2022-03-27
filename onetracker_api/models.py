"""Models for OneTracker."""

from dataclasses import dataclass
import datetime
from typing import List
import datetime

from .exceptions import OneTrackerError

@dataclass(frozen=True)
class SessionObject:
    """
    Object holding session information from the OneTracker API.

    Attributes:

    user_id: User ID of the authenticated user.

    token: Authentication Token of the authenticated user.

    expiration: Expiration time and date of the authentication token.
    """

    user_id: int
    token: str
    expiration: datetime.datetime

    @staticmethod
    def from_dict(data: dict):
        return SessionObject(
            user_id=data.get("user_id"),
            token=data.get("token"),
            expiration=datetime.datetime.fromisoformat(data.get("expiration").split(".")[0])
        )

@dataclass(frozen=True)
class AuthenticationTokenResponse:
    """
    Object holding authentication token response from the OneTracker API.

    Attributes:

    message: Response message.

    session: SessionObject.
    """

    message: str
    session: SessionObject

    @staticmethod
    def from_dict(data: dict):
        if data is {} or data is None or not data.get("message") == "ok":
            if data.get("message"):
                raise OneTrackerError(data.get("message"))
            else:
                raise OneTrackerError("Unable to convert data to GetParcelResponse.")
        else:
            return AuthenticationTokenResponse(
                message=data.get("message"),
                session=SessionObject.from_dict(data.get("session"))
            )

@dataclass(frozen=True)
class TrackingEvent:
    """
    Object holding a tracking event

    Attributes:

    id: Tracking event ID.

    parcel_id: Parcel ID.

    carrier_id: Carrier ID.

    carrier_name: Carrier name.

    status: Status.

    text: Text.

    locatiom: Location.

    latitude: Latitude.

    longitude: Longitude.

    time: Time.

    time_added: Time added.
    """

    id: int
    parcel_id: int
    carrier_id: int
    carrier_name: str
    status: str
    text: str
    location: str
    latitude: float
    longitude: float
    time: datetime.datetime
    time_added: datetime.datetime

    @staticmethod
    def from_dict(data: dict):
        return TrackingEvent(
            id=data.get("id"),
            parcel_id=data.get("parcel_id"),
            carrier_id=data.get("carrier_id"),
            carrier_name=data.get("carrier_name"),
            status=data.get("status"),
            text=data.get("text"),
            location=data.get("location"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            time=datetime.datetime.fromisoformat(data.get("time").split("Z")[0]),
            time_added=datetime.datetime.fromisoformat(data.get("time_added").split("Z")[0])
        )


@dataclass(frozen=True)
class Parcel:
    """
    Object holding parcel information from the OneTracker API.

    Attributes:

    id: Parcel ID.

    user_id: User ID of the authenticated user.

    email_id: Email ID of the email associated with the parcel.

    email_sender: Email sender of the email associated with the parcel.

    retailer_name: Name of the retailer.

    description: Description of the parcel.

    notification_level: Notification level of the parcel.

    is_archived: Whether the parcel is archived or not.

    carrier: Carrier of the parcel.

    carrier_name: Carrier name of the parcel.

    carrier_redirection_available: Whether carrier redirection is available or not.

    tracker_cached: Whether the tracker is cached or not.

    tracking_id: Tracking ID of the parcel.

    tracking_url: Tracking URL of the parcel.

    tracking_status: Tracking status of the parcel.

    tracking_status_description: Tracking status description of the parcel.

    tracking_status_text: Tracking status text of the parcel.

    tracking_extra_info: Tracking extra info of the parcel.

    tracking_location: Tracking location of the parcel.

    tracking_time_estimated: Tracking time estimated of the parcel.

    tracking_time_delivered: Tracking time delivered of the parcel.

    tracking_lock: Whether the tracking is locked or not.

    tracking_events: List of TrackingEvent objects.

    time_added: Time added of the parcel.

    time_updated: Time updated of the parcel.
    """

    id: int
    user_id: int
    email_id: int
    email_sender: str
    retailer_name: str
    description: str
    notification_level: int
    is_archived: bool
    carrier: str
    carrier_name: str
    carrier_redirection_available: bool
    tracker_cached: bool
    tracking_id: str
    tracking_url: str
    tracking_status: str
    tracking_status_description: str
    tracking_status_text: str
    tracking_extra_info: str
    tracking_location: str
    tracking_time_estimated: datetime.datetime
    tracking_time_delivered: datetime.datetime
    tracking_lock: bool
    tracking_events: List[TrackingEvent]
    time_added: datetime.datetime
    time_updated: datetime.datetime

    @staticmethod
    def from_dict(data: dict):
        return Parcel(
            id=data.get("id"),
            user_id=data.get("user_id"),
            email_id=data.get("email_id"),
            email_sender=data.get("email_sender"),
            retailer_name=data.get("retailer_name"),
            description=data.get("description"),
            notification_level=data.get("notification_level"),
            is_archived=data.get("is_archived"),
            carrier=data.get("carrier"),
            carrier_name=data.get("carrier_name"),
            carrier_redirection_available=data.get("carrier_redirection_available"),
            tracker_cached=data.get("tracker_cached"),
            tracking_id=data.get("tracking_id"),
            tracking_url=data.get("tracking_url"),
            tracking_status=data.get("tracking_status"),
            tracking_status_description=data.get("tracking_status_description"),
            tracking_status_text=data.get("tracking_status_text"),
            tracking_extra_info=data.get("tracking_extra_info"),
            tracking_location=data.get("tracking_location"),
            tracking_time_estimated=datetime.datetime.fromisoformat(data.get("tracking_time_estimated").split("Z")[0]),
            tracking_time_delivered=datetime.datetime.fromisoformat(data.get("tracking_time_delivered").split("Z")[0]),
            tracking_lock=data.get("tracking_lock"),
            tracking_events=[TrackingEvent.from_dict(tracking_event) for tracking_event in data.get("tracking_events") or []],
            time_added=datetime.datetime.fromisoformat(data.get("time_added").split("Z")[0]),
            time_updated=datetime.datetime.fromisoformat(data.get("time_updated").split("Z")[0])
        )

@dataclass(frozen=True)
class ListParcelsResponse:
    """
    Object representing the response of List Parcels.

    Attributes:

    message: Response message.

    parcels: List of Parcel objects.
    """

    message: str
    parcels: List[Parcel]

    @staticmethod
    def from_dict(data: dict):
        if data is {} or data is None or not data.get("message") == "ok":
            if data.get("message"):
                raise OneTrackerError(data.get("message"))
            else:
                raise OneTrackerError("Unable to convert data to GetParcelResponse.")
        else:
            return ListParcelsResponse(
                message=data.get("message"),
                parcels=[Parcel.from_dict(parcel) for parcel in data.get("parcels") or []]
            )

@dataclass(frozen=True)
class GetParcelResponse:
    """
    Object representing the response of List Parcel.

    Attributes:

    message: Response message.

    parcel: Parcel object.
    """

    message: str
    parcel: Parcel

    @staticmethod
    def from_dict(data: dict):
        if data is {} or data is None or not data.get("message") == "ok":
            if data.get("message"):
                raise OneTrackerError(data.get("message"))
            else:
                raise OneTrackerError("Unable to convert data to GetParcelResponse.")
        else:
            return GetParcelResponse(
                message=data.get("message"),
                parcel=Parcel.from_dict(data.get("parcel"))
            )

@dataclass(frozen=True)
class DeleteParcelResponse:
    """
    Object representing the response of Delete Parcel.

    Attributes:

    message: Response message.
    """

    message: str

    @staticmethod
    def from_dict(data: dict):
        if data is {} or data is None or not data.get("message") == "ok":
            if data.get("message"):
                raise OneTrackerError(data.get("message"))
            else:
                raise OneTrackerError("Unable to convert data to GetParcelResponse.")
        else:
            return DeleteParcelResponse(
                message=data.get("message")
            )

@dataclass(frozen=True)
class Carrier:
    """
    Object representing a carrier.

    Attributes:

    id: ID of the carrier.

    name: Name of the carrier.

    frequently_used: If the carrier is frequently used or not.
    """

    id: str
    name: str
    frequently_used: bool

    @staticmethod
    def from_dict(data: dict):
        return Carrier(
            id=data.get("id"),
            name=data.get("name"),
            frequently_used=data.get("frequently_used"),
        )

@dataclass(frozen=True)
class ListCarriersResponse:
    """
    Object representing the response of List Carriers.

    Attributes:

    message: Response message.

    carriers: List of Carrier objects.
    """

    message: str
    carriers: List[Carrier]

    @staticmethod
    def from_dict(data: dict):
        if data is {} or data is None or not data.get("message") == "ok":
            if data.get("message"):
                raise OneTrackerError(data.get("message"))
            else:
                raise OneTrackerError("Unable to convert data to GetParcelResponse.")
        else:
            return ListCarriersResponse(
                message=data.get("message"),
                carriers=[Carrier.from_dict(carrier) for carrier in data.get("carriers") or []]
            )
