#   -------------------------------------------------------------
#   Copyright (c) Felix Kotschenreuther. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Here are all the exceptions defined that can be raised by the church_tools_api package."""

from __future__ import annotations


class ChurchToolsApiException(Exception):
    """Base class for all exceptions raised by the church_tools_api package."""


class ChurchToolsApiAuthenticationException(ChurchToolsApiException):
    """Raised when the authentication fails."""


class ChurchToolsApiConnectionException(ChurchToolsApiException):
    """Raised when the connection to the church tools instance fails."""


class ChurchToolsApiNotFoundException(ChurchToolsApiException):
    """Raised when the requested resource was not found."""


class ChurchToolsApiPermissionException(ChurchToolsApiException):
    """Raised when the user does not have the permission to access the requested resource."""


class ChurchToolsApiRateLimitException(ChurchToolsApiException):
    """Raised when the rate limit is exceeded."""


class ChurchToolsApiUnknownException(ChurchToolsApiException):
    """Raised when an unknown error occurs."""
