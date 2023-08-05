#   -------------------------------------------------------------
#   Copyright (c) Felix Kotschenreuther. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""This module contains the ChurchToolsApi class."""

from __future__ import annotations

import requests
from ChurchToolsApi.exceptions import (
    ChurchToolsApiConnectionException,
    ChurchToolsApiNotFoundException,
    ChurchToolsApiAuthenticationException,
)

import logging
from urllib.parse import urlencode


class RequiresLogin:
    def __init__(self, func) -> None:
        self.func = func

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            if not instance.is_authenticated():
                instance.authenticate()
            return self.func(instance, *args, **kwargs)

        return wrapper


class ChurchToolsApi:
    """
    This class represents the ChurchToolsApi object.
    Usage:
        Instance via ChurchToolsApi(url, token)
    """

    def __init__(self, url, token):
        """
        Initialize the ChurchToolsApi object with a token.
        :param url: URL of the church tools instance
        :param token: Token for authentication
        """
        self.url = url
        self.token = token
        self.session = None
        self.authenticated = False

    def authenticate(self) -> None:
        """
        Authenticate with the given credentials.
        """
        if self.session is None:
            self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Login {self.token}"})

        # Check if the inputs are valid

        try:
            response = self.session.get(f"{self.url}/api/whoami")
            logging.warning("Response: %s", response)
            logging.warning("Response body: %s", response.json())
        except requests.exceptions.ConnectionError as exc:
            logging.warning("Connection Error: %s", exc)
            raise ChurchToolsApiConnectionException("Could not connect to the church tools instance.") from exc

        if response.url != f"{self.url}/api/whoami":
            # This happens when the prefix of the church.tools url is wrong
            raise ChurchToolsApiConnectionException("Could not connect to the church tools instance.")

        if response.status_code == 401:
            raise ChurchToolsApiAuthenticationException("Could not authenticate with the given token.")

        if response.status_code != 200:
            raise ChurchToolsApiConnectionException("Could not connect to the church tools instance.")

        self.authenticated = True

    def is_authenticated(self) -> bool:
        """
        Check if the user is authenticated.
        :return: True if authenticated, False otherwise.
        """
        return self.authenticated

    def _construct_query_string(self, *args, **kwargs) -> str:
        """
        Construct a query string from the given arguments.
        :param args: List of arguments
        :param kwargs: List of keyword arguments
        :return: Query string
        """
        query_params = {}

        for arg in args:
            if isinstance(arg, list):
                query_params[arg[0]] = arg[1:]

        query_params.update(kwargs)

        query_string = urlencode(query_params, doseq=True)
        return "?" + query_string

    def _get(self, endpoint: str, *args, **kwargs) -> dict:
        """
        Get a resource from the church tools instance.
        :param endpoint: Endpoint of the resource
        :return: JSON response
        """
        query_string = self._construct_query_string(*args, **kwargs)
        response = self.session.get(f"{self.url}/api/{endpoint}{query_string}")
        if response.status_code == 404:
            raise ChurchToolsApiNotFoundException(f"Could not find resource {endpoint}")
        return response.json()

    @RequiresLogin
    def get_ressource_masterdata(self) -> dict:
        """
        Get the masterdata for the booking module.
        :return: JSON response
        """
        return self._get("resource/masterdata")

    @RequiresLogin
    def get_booking_info(
        self, ressource_ids: list[int], start_date: str = None, end_date: str = None, status_ids: list[int] = None
    ) -> dict:
        """
        Get the booking info for a given resource.
        :param resource_ids: List of resource ids eg. [1, 2, 3]
        :param start_date: Start date of the booking in the format YYYY-MM-DD
        :param end_date: End date of the booking in the format YYYY-MM-DD
        :status_ids: List of status ids eg. [1, 2, 3, 99] where 1 = "waiting for approval", 2 = "approved", 3 = "rejected", 99 = "deleted"
        """
        return self._get(
            endpoint="bookings",
            resource_ids=ressource_ids,
            start_date=start_date,
            end_date=end_date,
            status_ids=status_ids,
        )
