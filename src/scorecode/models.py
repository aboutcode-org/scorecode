#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/scorecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import attr
from commoncode.datautils import Date
from commoncode.datautils import List
from commoncode.datautils import String

from scorecode.utils import remove_fragment


class ModelMixin:

    def to_dict(self, **kwargs):
        """
        Return a mapping of primitive Python types.
        """
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, mapping):
        """
        Return an object built from ``kwargs`` mapping. Always ignore unknown
        attributes provided in ``kwargs`` that do not exist as declared attributes
        in the ``cls`` class.
        """
        known_attr = attr.fields_dict(cls)
        kwargs = {k: v for k, v in mapping.items() if k in known_attr}
        return cls(**kwargs)


@attr.attributes(slots=True)
class ScorecardCheck(ModelMixin):

    check_name = String(
        repr=True,
        label="check name",
        help="Defines the name of check corresponding to the OSSF score"
        "For example: Code-Review or CII-Best-Practices"
        "These are the some of the checks which are performed on a scanned "
        "package",
    )

    check_score = String(
        repr=True,
        label="check score",
        help="Defines the score of the check for the package scanned"
        "For Eg : 9 is a score given for Code-Review",
    )

    reason = String(
        repr=True,
        label="reason",
        help="Gives a reason why a score was given for a specific check"
        "For eg, : Found 9/10 approved changesets -- score normalized to 9",
    )

    details = List(
        repr=True, label="score details", help="A list of details/errors regarding the score"
    )

    @classmethod
    def from_data(cls, check_data):
        """
        Return a list of check objects for a package.
        """
        checks = []

        for check in check_data:
            data = {
                "check_name": check.get("name"),
                "check_score": str(check.get("score")),
                "reason": check.get("reason", None),
                "details": check.get("details", None),
            }
            checks.append(cls(**data))

        return checks


@attr.attributes(slots=True)
class PackageScore(ModelMixin):
    """
    Class for storing scorecard data related to packages.
    """

    scoring_tool = String(
        repr=True,
        label="scoring tool",
        help="Defines the source of a score or any other scoring metrics"
        "For example: ossf-scorecard for scorecard data",
    )

    scoring_tool_version = String(
        repr=True,
        label="scoring tool version",
        help="Defines the version of the scoring tool used for scanning the package",
    )

    score = String(repr=True, label="score", help="Score of the package which is scanned")

    scoring_tool_documentation_url = String(
        repr=True, label="scoring documentation url", help="Version of the package as a string."
    )

    score_date = Date(repr=True, label="score date", help="score date")

    checks = List(item_type=ScorecardCheck, label="checks", help="List of all checks used")

    @classmethod
    def from_data(cls, scorecard_data):
        """
        Return PackageScore object created from a `scorecard_data` mapping.
        """
        data = {
            "score": str(scorecard_data.get("score")),
            "scoring_tool_version": scorecard_data.get("scorecard").get("version"),
            "scoring_tool_documentation_url": remove_fragment(
                scorecard_data.get("checks")[0].get("documentation").get("url")
            ),
            # This needs to be a constant variable
            "scoring_tool": "ossf_scorecard",
            "score_date": scorecard_data.get("date", None),
            "checks": ScorecardCheck.from_data(scorecard_data.get("checks", [])),
        }

        return cls(**data)
