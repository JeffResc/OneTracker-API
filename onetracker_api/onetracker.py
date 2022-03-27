"""Asynchronous Python client for OneTracker."""
from typing import Dict, List, Optional, Type
from aiohttp.client import ClientSession
import json
import datetime

from .client import Client
from .exceptions import (
    OneTrackerError,
    OneTrackerAuthenticationSessionError,
    OneTrackerAuthenticationSessionExpiredError
)
from .models import (
    AuthenticationTokenResponse,
    ListParcelsResponse,
    GetParcelResponse,
    SessionObject,
    DeleteParcelResponse,
    ListCarriersResponse,
)

class OneTracker(Client):
    """
    Main class for Python API.

    Args:

    email: The email address of the user.

    password: The password of the user.

    request_timeout: The request timeout in seconds.

    session: The aiohttp.ClientSession to use.

    user_agent: The user agent to use.
    """

    def __init__(
        self,
        request_timeout: int = 8,
        session: ClientSession = None,
        user_agent: str = None,
        session_object: SessionObject = None,
    ) -> None:
        """Initilize connection with OneTracker"""
        super().__init__(
            request_timeout=request_timeout,
            session=session,
            user_agent=user_agent,
            session_object=session_object,
        )

    def __check_session_object__(self) -> None:
        """
        Check internally saved session object.
        
        Raises:
        
        OneTrackerAuthenticationSessionError: If session object is None.
        """
        if self.session_object is None:
            raise OneTrackerAuthenticationSessionError("Unable to authenticate to the API, no session object. Please call the onetracker.login() method first.")
        if self.session_object.expiration < datetime.datetime.now():
            raise OneTrackerAuthenticationSessionExpiredError("Unable to authenticate to the API, the authentication session has expired. Please call the onetracker.login() method again.")

    def __check_parcel_id__(self, id) -> None:
        """
        Check if parcel_id is not None and is a string. For internal use.
        
        Args:
        
        parcel_id: The parcel_id to check.
        
        Raises:
        
        OneTrackerError: If parcel_id is not a string.
        """
        if id is None:
            raise OneTrackerError("Unable to perform that method, no id specified.")
        if type(id) is not int:
            raise OneTrackerError("Unable to perform that method, id must be an int.")

    def __check_tracking_id__(self, tracking_id) -> None:
        """
        Check if tracking_id is a string. For internal use.
        
        Args:
        
        tracking_id: The tracking_id to check.
        
        Raises:
        
        OneTrackerError: If tracking_id is not a string.
        """
        if type(tracking_id) is not str:
            raise OneTrackerError("Unable to perform that method, tracking_id must be a string.")

    async def login(self, email, password) -> AuthenticationTokenResponse:
        """
        Create authentication token.

        Args:

        email: The email address of the user.

        password: The password of the user.

        Returns:
            AuthenticationTokenResponse: Authentication Token Response Object.
        """
        try:
            results = await self._request("/auth/token", method='POST', data=json.dumps({"email": email, "password": password}))
            authentication_token_response = AuthenticationTokenResponse.from_dict(results)
            self.session_object = authentication_token_response.session
            return authentication_token_response
        except OneTrackerError as e:
            raise OneTrackerError(f"Unable to authenticate with OneTracker API: {e}")

    async def list_parcels(self, archived = False) -> ListParcelsResponse:
        """
        List parcels.

        Args:

        archived: If True, archived parcels will be returned.

        Returns:
            ListParcelsResponse: List Parcels Response Object.
        """
        self.__check_session_object__()
        archived_str = "true" if archived else "false"
        results = await self._request("/parcels?archived={}".format(archived_str), method='GET', headers={"x-api-token": self.session_object.token})
        try:
            return ListParcelsResponse.from_dict(results)
        except OneTrackerError as e:
            raise OneTrackerError(f"Unable to list parcels: {e}")

    async def get_parcel(self, id) -> GetParcelResponse:
        """
        Get one parcel.

        Args:

        id: The id of the parcel.

        Returns:
            GetParcelResponse: Parcel Response Object.
        """
        self.__check_session_object__()
        self.__check_parcel_id__(id)
        results = await self._request("/parcels/{}".format(id), method='GET', headers={"x-api-token": self.session_object.token})
        try:
            return GetParcelResponse.from_dict(results)
        except OneTrackerError as e:
            raise OneTrackerError(f"Unable to get parcel: {e}")

    async def delete_parcel(self, id) -> DeleteParcelResponse:
        """
        Delete one parcel.

        Args:

        id: The id of the parcel.

        Returns:
            DeleteParcelResponse: Delete Parcel Response Object.
        """
        self.__check_session_object__()
        self.__check_parcel_id__(id)
        results = await self._request("/parcels/{}".format(id), method='DELETE', headers={"x-api-token": self.session_object.token})
        try:
            return DeleteParcelResponse.from_dict(results)
        except OneTrackerError as e:
            raise OneTrackerError(f"Unable to delete parcel: {e}")

    async def list_carriers(self, tracking_id=None) -> ListCarriersResponse:
        """
        List carriers with tracking_id.

        Args:

        tracking_id: If given, the OneTracker API will return carriers that the given tracking ID is most likely to be carried by. Optional argument, will return all carriers if unspecified.

        Returns:
            ListCarrierResponse: List Carrier Response Object.
        """
        self.__check_session_object__()
        if tracking_id is not None:
            self.__check_tracking_id__(tracking_id)
            results = await self._request("/carriers?trackingID={}".format(tracking_id), method='GET', headers={"x-api-token": self.session_object.token})
        else:
            results = await self._request("/carriers", method='GET', headers={"x-api-token": self.session_object.token})
        try:
            return ListCarriersResponse.from_dict(results)
        except OneTrackerError as e:
            raise OneTrackerError(f"Unable to list carriers: {e}")

    async def __aenter__(self) -> "OneTracker":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close_session()
