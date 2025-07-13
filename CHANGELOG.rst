Changelog
=========


v0.0.1 - 2024-08-23
--------------------

Initial release of scorecode

- Abstract models to store data for a score and all it's checks
  Created models like PackageScore, ScorecardCheck for saving OSSF scorecard
  data.
- Django mixins to be used in SCIO and purldb
- Fetch Scorecard data for github and gitlab urls.
- Add test scripts to check for different repos scorecard data.
- Add files from Skeleton for packaging, CI and others.

v0.0.2 - 2024-08-23
--------------------

Patch Release of scorecode to fix package name.

v0.0.3 - 2025-02-24
--------------------

Patch Release of scorecode to fix checks in scorecard data.

v0.0.4 - 2025-07-12
--------------------

Added parsing score date functionality to `PackageScoreMixin`
