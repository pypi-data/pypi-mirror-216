#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""
This is a configuration file for pytest containing customizations and fixtures.

In VSCode, Code Coverage is recorded in config.xml. Delete this file to reset reporting.
"""

from __future__ import annotations

from typing import List

from ChurchToolsApi.churchtools_api import ChurchToolsApi
import logging
import pytest
import requests
import responses
from _pytest.nodes import Item


def pytest_collection_modifyitems(items: list[Item]):
    for item in items:
        if "spark" in item.nodeid:
            item.add_marker(pytest.mark.spark)
        elif "_int_" in item.nodeid:
            item.add_marker(pytest.mark.integration)


@pytest.fixture
def unit_test_mocks(monkeypatch: None):
    """Include Mocks here to execute all commands offline and fast."""
    pass


DEFAULT_URL = "https://demo.church.tools"


# Make a mock fixture that build a request response object with modifiable functions
# https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response


class MockResponse:
    def __init__(self, json_data: dict, status_code: int, url: str = "https://demo.church.tools/api/whoami"):
        self.json_data = json_data
        self.status_code = status_code
        self.url = url

    def json(self):
        return self.json_data

    def change_json(self, json_data: dict):
        self.json_data = json_data

    def change_status_code(self, status_code: int):
        self.status_code = status_code

    def change_url(self, url: str):
        self.url = url


def mock_session_get(*args, **kwargs):
    response = MockResponse({"id": 1}, 200)
    return response


@pytest.fixture
def api_instance() -> ChurchToolsApi:
    instance = ChurchToolsApi(DEFAULT_URL, "token")
    yield instance


@pytest.fixture
@responses.activate
def authenticated_api_instance(api_instance: ChurchToolsApi, get_default_url_api: str):
    responses.get(get_default_url_api + "whoami", json={"id": 1})
    api_instance.authenticate()
    yield api_instance


@pytest.fixture
def get_default_url():
    yield DEFAULT_URL


@pytest.fixture
def get_default_url_api():
    yield DEFAULT_URL + "/api/"
