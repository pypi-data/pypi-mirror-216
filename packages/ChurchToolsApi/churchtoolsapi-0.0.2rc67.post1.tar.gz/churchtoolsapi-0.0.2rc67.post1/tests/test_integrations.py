#   -------------------------------------------------------------
#   Copyright (c) Felix Kotschenreuther. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Here are all the integration tests defined that can be run by the church_tools_api package."""

from __future__ import annotations
import pytest
from ChurchToolsApi.churchtools_api import ChurchToolsApi
from ChurchToolsApi.exceptions import (
    ChurchToolsApiConnectionException,
    ChurchToolsApiNotFoundException,
    ChurchToolsApiAuthenticationException,
)


@pytest.mark.integration
def test_integration_stud():
    # This is a stud integration test
    pass
