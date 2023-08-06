v2.0.1 (2023-06-28)
===================

Bugfixes
--------

- Update MAXIMUM_ALLOWED_WORKFLOW_NAME_LENGTH to be consistent with database (100 characters). (`#19 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/19>`__)


Misc
----

- Update airflow dependency to 2.6.2 and use python 3.11 (`#20 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/20>`__)
- Use python 3.11 in ReadTheDocs builds

v1.4.0 (2023-05-05)
===================

Misc
----

- Update pip before use (`#17 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/17>`__)
- Move to airflow 2.6.0 (`#18 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/18>`__)


v1.3.0 (2023-02-17)
===================

Misc
----

- Update Airflow to v2.5.1


v1.2.0 (2022-11-15)
===================

Misc
----

- Update airflow dependency to include optional celery dependencies. (`#16 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/16>`__)


Documentation
-------------

- Add changelog to RTD left hand TOC to include rendered changelog in documentation build. (`#16 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/16>`__)

v1.1.2 (2022-11-02)
===================

Misc
----

- Add additional logging of container allocation information to the task startup logs to shorten investigations that may be allocation specific. (`#15 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/15>`__)


v1.1.1 (2022-10-20)
===================

Misc
----

- Make python 3.10 the minimum supported version (`#14 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/14>`__)


v1.1.0 (2022-10-10)
===================

Features
--------

- Update airflow version from 2.2.4 to 2.4.1. Details can be found here: https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html (`#13 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/13>`__)


v1.0.1 (2022-09-28)
===================

Features
--------

- Implement static method to create workflow name from constituent parts.
  This will be used by the calibration_workflow_name pre-commit hook. (`#12 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/12>`__)


v1.0.0 (2022-08-08)
===================

Removals
--------

- Updated the workflow naming API with breaking changes which do not support the old implementation. (`#11 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/11>`__)


Documentation
-------------

- Add CHANGELOG and towncrier machinery (`#10 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/10>`__)


v0.3.6 (2022-04-19)
===================

Misc
----

- Removing pinning of `markupsafe` version (related to airflow version 2.2.4)

v0.3.5 (2022-04-19)
===================

Misc
----

- Update airflow version to 2.2.4

v0.3.4 (2022-04-19)
===================

Features
--------

- Allow arbitrary tags on DAG names in Airflow (`#9 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/9>`__)


v0.3.3 (2022-03-11)
===================

Features
--------

- Update pip prior to installing pipeline into virtual env (`#8 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/8>`__)


v0.3.2 (2022-03-11)
===================

Documentation
-------------

- Update docstrings to comply with pydocstyle


v0.3.1 (2022-02-22)
===================

Bugfixes
--------

- Adding dependency fix due to Airflow pinning flask

v0.3.0 (2022-02-17)
===================

Misc
----

- Label `run()` apm spans as type "core" (`#6 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/6>`__)
- Update python and airflow to 3.9 and 2.2.3, respectively (`#7 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/7>`__)
