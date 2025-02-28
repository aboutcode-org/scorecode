#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/scorecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import pytest

from scorecode.ossf_scorecard import fetch_scorecard

# Define a list of test cases with different platforms, organizations, and repositories
test_cases = [
    ("github.com", "nexB", "scancode-toolkit"),
    ("github.com", "tensorflow", "tensorflow"),
    ("github.com", "apache", "spark"),
    ("gitlab.com", "gitlab-org", "gitlab"),
]


@pytest.mark.parametrize("platform, org, repo", test_cases)
def test_get_scorecard(platform, org, repo):
    data = fetch_scorecard(platform, org, repo)

    # Check that the data object contains the expected fields
    assert hasattr(data, "scoring_tool")
    assert hasattr(data, "scoring_tool_version")
    assert hasattr(data, "score_date")
    assert hasattr(data, "score")
    assert hasattr(data, "scoring_tool_documentation_url")
    assert hasattr(data, "checks")

    # Validate the types of the fields
    assert isinstance(data.scoring_tool, str)
    assert isinstance(data.scoring_tool_version, str)
    assert isinstance(data.score_date, str)
    assert isinstance(data.score, str)
    assert isinstance(data.scoring_tool_documentation_url, str)
    assert isinstance(data.checks, list)

    # Check that the URL is valid and has the expected structure
    assert data.scoring_tool_documentation_url.startswith("https://github.com/")
    assert "docs/checks.md" in data.scoring_tool_documentation_url

    # Check that data.checks contains valid ScorecardCheck objects
    for check in data.checks:
        assert hasattr(check, "check_name")
        assert hasattr(check, "check_score")
        assert hasattr(check, "reason")
        assert hasattr(check, "details")

        assert isinstance(check.check_name, str)
        assert isinstance(check.check_score, str)
        assert isinstance(check.reason, (str, type(None)))  # Allow None if not provided
        assert isinstance(check.details, (list, type(None)))  # Allow None or list

        # If details exist, ensure all elements are strings
        if check.details:
            assert all(isinstance(detail, str) for detail in check.details)
