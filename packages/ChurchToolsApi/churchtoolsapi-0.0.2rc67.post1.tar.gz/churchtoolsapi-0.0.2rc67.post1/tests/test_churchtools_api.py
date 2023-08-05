#   -------------------------------------------------------------
#   Copyright (c) Felix Kotschenreuther. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Here are all the exceptions defined that can be raised by the church_tools_api package."""

from __future__ import annotations

from unittest.mock import patch

import requests
import pytest

from ChurchToolsApi.churchtools_api import ChurchToolsApi
from ChurchToolsApi.exceptions import (
    ChurchToolsApiConnectionException,
    ChurchToolsApiNotFoundException,
    ChurchToolsApiAuthenticationException,
)

import responses


def test_churchtools_api_init():
    api = ChurchToolsApi("https://demo.church.tools", "token")
    assert api.url == "https://demo.church.tools"
    assert api.token == "token"
    assert api.session is None


@responses.activate
def test_authenticate_wrong_url(api_instance, get_default_url_api):
    responses.get(get_default_url_api + "whoami", body=requests.exceptions.ConnectionError("Test"))
    with pytest.raises(ChurchToolsApiConnectionException):
        api_instance.authenticate()


@responses.activate
def test_authenticate_wrong_url_2(api_instance, get_default_url_api):
    responses.get(get_default_url_api + "/wrong_suburl", json="")
    with pytest.raises(ChurchToolsApiConnectionException):
        api_instance.authenticate()


@responses.activate
def test_authenticate_wrong_status_code(api_instance, get_default_url_api):
    responses.get(get_default_url_api + "whoami", json="", status=501)
    with pytest.raises(ChurchToolsApiConnectionException):
        api_instance.authenticate()


@responses.activate
def test_authenticate_wrong_token(api_instance, get_default_url_api):
    responses.get(get_default_url_api + "whoami", json="", status=401)
    with pytest.raises(ChurchToolsApiAuthenticationException):
        api_instance.authenticate()


@responses.activate
def test_successfull_authenticate(api_instance, get_default_url_api):
    responses.get(get_default_url_api + "whoami", json={"id": 1})
    api_instance.authenticate()
    assert api_instance.authenticated


@responses.activate
def test_requires_login_decorator(api_instance, get_default_url_api):
    responses.get(get_default_url_api + "whoami", json={"id": 1})
    responses.get(get_default_url_api + "resource/masterdata", json={"id": 1})

    assert api_instance.is_authenticated() is False
    api_instance.get_ressource_masterdata()
    assert api_instance.is_authenticated() is True
