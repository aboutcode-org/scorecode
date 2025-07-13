#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/scorecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

from collections import namedtuple
from urllib.parse import urlparse

import requests

from scorecode import OSSF_SCORECARD_API_URL
from scorecode.models import PackageScore


def fetch_scorecard(platform, org, repo):
    """
    Return a `PackageScore` object with OSSF scorecard data for a specific repo
    For example : for this repository : github.com/aboutcode-org/scorecode
        github.com is platform
        aboutcode-org is org
        scorecode is repo
    """

    url = f"{OSSF_SCORECARD_API_URL}/projects/{platform}/{org}/{repo}"
    response = requests.get(url)

    if response.ok:
        score_data = response.json()
        return PackageScore.from_data(score_data)
    else:
        response.raise_for_status()


def is_available():
    """Return True if the configured Scorecard server is available."""

    try:
        session = requests.Session()
        response = session.get(OSSF_SCORECARD_API_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as request_exception:
        return False

    return response.ok


def fetch_scorecard_info(package, logger=None):
    """
    Return scorecard info for a list of discovered packages.
    """
    url = package.vcs_url
    if url:
        repo_data = extract_repo_info(url, check_url_existence=True)
        if repo_data:
            scorecard_data = fetch_scorecard(
                platform=repo_data.platform, org=repo_data.org, repo=repo_data.repo
            )
            return scorecard_data


def extract_repo_info(url, check_url_existence=False):
    """
    Extract platform, org, and repo from a given GitHub or GitLab URL.
    """
    RepoData = namedtuple("RepoData", ["platform", "org", "repo"])

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if not hostname:
        return None

    if "github.com" in hostname:
        platform = "github.com"
    elif "gitlab.com" in hostname:
        platform = "gitlab.com"
    else:
        return None

    path_parts = parsed_url.path.strip("/").split("/")

    if len(path_parts) < 2:
        return None

    org, repo = path_parts

    repo_url = f"https://{hostname}/{org}/{repo}"

    if check_url_existence:
        try:
            response = requests.head(repo_url)
            if not response.ok:
                return None
        except requests.RequestException:
            return None

    return RepoData(platform=platform, org=org, repo=repo)
