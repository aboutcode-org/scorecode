#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/scorecode for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#


from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class PackageScoreMixin(models.Model):
    """
    Abstract Model for saving OSSF scorecard data.
    """

    class ScoringTool(models.TextChoices):
        OSSF = "ossf-scorecard"
        OTHERS = "others"

    scoring_tool = models.CharField(
        max_length=100,
        choices=ScoringTool.choices,
        blank=True,
        help_text=_(
            "Defines the source of a score or any other scoring metrics"
            "For example: ossf-scorecard for scorecard data"
        ),
    )

    scoring_tool_version = models.CharField(
        max_length=50,
        blank=True,
        help_text=_(
            "Defines the version of the scoring tool used for scanning the"
            "package"
            "For Eg : 4.6 current version of OSSF - scorecard"
        ),
    )

    score = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Score of the package which is scanned"),
    )

    scoring_tool_documentation_url = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Documentation URL of the scoring tool used"),
    )

    score_date = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        help_text=_("Date when the scoring was calculated on the package"),
    )

    @classmethod
    def parse_score_date(cls, date_str, formats=None):
        """
        Parse a date string into a timezone-aware datetime object,
        or return None if parsing fails.
        """

        if not formats:
            formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"]

        if date_str:
            for fmt in formats:
                try:
                    naive_datetime = datetime.strptime(date_str, fmt)
                    return timezone.make_aware(naive_datetime, timezone.get_current_timezone())
                except ValueError:
                    continue

        return None

    class Meta:
        abstract = True


class ScorecardChecksMixin(models.Model):

    check_name = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "Defines the name of check corresponding to the OSSF score"
            "For example: Code-Review or CII-Best-Practices"
            "These are the some of the checks which are performed on a scanned package"
        ),
    )

    check_score = models.CharField(
        max_length=50,
        blank=True,
        help_text=_(
            "Defines the score of the check for the package scanned"
            "For Eg : 9 is a score given for Code-Review"
        ),
    )

    reason = models.CharField(
        max_length=300,
        blank=True,
        help_text=_(
            "Gives a reason why a score was given for a specific check"
            "For eg, : Found 9/10 approved changesets -- score normalized to 9"
        ),
    )

    details = models.JSONField(
        default=list,
        blank=True,
        help_text=_("A list of details/errors regarding the score"),
    )

    class Meta:
        abstract = True
