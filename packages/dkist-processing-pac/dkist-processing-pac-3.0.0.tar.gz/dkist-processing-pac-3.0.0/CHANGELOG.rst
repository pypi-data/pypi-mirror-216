v3.0.0 (2023-06-29)
===================

Misc
----

- Update to python 3.11 and update library package versions. (`#23 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/23>`__)


v2.1.1 (2023-05-05)
===================

Misc
----

- Remove version constraint on required package `asdf`. This is needed to allow airflow to be updated.


v2.1.0 (2023-04-12)
===================

Features
--------

- Add fitting parameter (``inherit_global_vary_in_local_fit``) that allows the "local" fits to vary in the same way as "global" fits.
  Useful when you want to vary, e.g., the CU retardance over a large FOV. (`#22 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/22>`__)


v2.0.0 (2023-04-12)
===================

Features
--------

- Add flag to fit modes ("I_sys_per_CS_step") that allows I_sys to be freely for for every CS step in the polcal input. (`#17 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/17>`__)
- Optional argument ("suppress_local_starting_values") to `PolcalFitter` that drastically reduces the logging output on
  data with a large number of points to be fit. (`#20 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/20>`__)


Bugfixes
--------

- Remove all constraints on the dimensionality of input data (previously input data were required to be 3D). (`#18 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/18>`__)
- Don't require a minimum flux value in the input data. This allows instruments to normalize (or not) their polcal data however they want. (`#19 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/19>`__)
- Correct how coordinate transformations are applied in the inverse telescope model. The default Mueller Matrix will now
  place data into the same coordinate frame used by SDO and HINODE (-Q and +Q will be aligned parallel and perpendicular to the
  central meridian of the Sun, respectively). It will also apply a sign flip to U and V. All of these options can still be turned off if desired. (`#21 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/21>`__)


Misc
----

- Replace default `logging.info` with `logger.info` and default logger from `logger = logging.getLogger(__name__)`. (`#16 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/16>`__)


v1.0.1 (2022-12-15)
===================

Bugfixes
--------

- Fixed crash of fit caused by incorrectly set value of I_clear/I_sys if `remove_I_trend` option was set to `False`. (`#15 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/15>`__)


Documentation
-------------

- Add changelog to RTD left hand TOC to include rendered changelog in documentation build. (`#14 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/14>`__)


v1.0.0 (2022-11-02)
===================

Misc
----

- Major version change for production release.



v0.9.0 (2022-11-01)
===================

Bugfixes
--------

- Add correction angles to R23 and R45 in telescope model to account for true telescope mount configuration. (`#13 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/13>`__)


Misc
----

- Change import of QhullError due to upcoming scipy deprecation. (`#11 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/11>`__)


v0.8.1 (2022-09-30)
===================

Misc
----

- Refactor to expose `dkist_processing_pac.fitter.fitter_parameters.TELESCOPE_PARAMS` for other libraries (namely `dkist-processing-common`). (`#12 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/12>`__)


v0.8.0 (2022-06-13)
===================

Features
--------

- Implement two-stage fitting method where Calibration Unit parameters are fit from a single globally-average bin and then fixed for the fits of each local bin's modulation matrix (`#10 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/10>`__)


v0.7.0 (2022-06-03)
===================

Misc
----

- Complete rewrite to convert SV code to Data Center context (`#9 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/9>`__)


v0.6.2 (2022-04-28)
===================

Features
--------

- Relaxed version to FITS specification to move to SPEC0122 Rev F.

v0.6.1 (2022-04-27)
===================

Bugfixes
--------

- Don't modify dresser polarizer and retarder values when using it to initialize a `CalibrationSequence` object

v0.6.0 (2022-04-19)
===================

Features
--------

- Include `lmfit` `MinimizerResult` objects in return from `FittingFramework.run_core` (`#7 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/7>`__)
- Refactor to create `FittingFramework.prepare_model_objects` function (`#7 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/7>`__)


Documentation
-------------

- Add changelog and towncrier machinery (`#5 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/5>`__)


v0.5.1 (2022-03-31)
===================

Misc
----

- Don't throw annoying telescope db warnings if there is only 1 time listed in db (`#4 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/4>`__)


v0.5.0 (2022-03-24)
===================

Bugfixes
--------

- "Q_in" now *always* fixed to 0 if `use_M12` flag is set in fit mode (`#3 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/3>`__)


v0.4.1 (2022-03-10)
===================

Features
--------

- Added more fit_modes (`M12_fitUV`, `fit_QUV`, `no_T`, `use_M12`, and `use_M12_globalRet_globalTrans`)

v0.4.0 (2022-03-10)
===================

Features
--------

- Single Calibration Sequence steps now expected to come from separate IPs (`#2 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/2>`__)


Bugfixes
--------

- Use "none" instead of 0 for angle in headers when GOS optic not in the beam (`#2 <https://bitbucket.org/dkistdc/dkist-processing-pac/pull-requests/2>`__)


v0.3.5 (2022-02-22)
===================

First version to touch DKIST summit data
