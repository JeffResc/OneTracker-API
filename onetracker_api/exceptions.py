"""Exceptions for OneTracker."""

class OneTrackerError(Exception):
    """Generic OneTracker Exception."""

    pass


class OneTrackerConnectionError(OneTrackerError):
    """OneTracker connection exception."""

    pass


class OneTrackerInternalServerError(OneTrackerError):
    """OneTracker internal server error exception."""

    pass

class OneTrackerClientError(OneTrackerError):
    """OneTracker client error exception."""

    pass

class OneTrackerAuthenticationError(OneTrackerError):
    """OneTracker authentication session error exception."""

    pass

class OneTrackerAuthenticationSessionError(OneTrackerError):
    """OneTracker authentication session error exception."""

    pass

class OneTrackerAuthenticationSessionExpiredError(OneTrackerError):
    """OneTracker authentication session expired error exception."""

    pass