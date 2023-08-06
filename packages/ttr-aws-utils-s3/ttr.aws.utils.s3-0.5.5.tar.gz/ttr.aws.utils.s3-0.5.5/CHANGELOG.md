# Changelog

## ttr.aws.utils.s3 0.5.5 (2023-06-30)

- Bugfixes
  - Remove support for python 2.7, 3.6 and 3.7
    ([#14](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/14))
  - Remove dependency on configparser backport
    ([#15](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/15))
  - tox tests are again passing (fixed setup.cfg attribute names)
    ([#16](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/16))
  - Support python versions 3.7 .. 3.11
    ([#17](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/17))
- Features
  - No significant changes
- Docs
  - No significant changes
- Internals
  - No significant changes

## ttr.aws.utils.s3 0.5.4 (2020-12-19)

- Bugfixes
  - No significant changes
- Features
  - No significant changes
- Docs
  - Help for s3lsvers shortened and fixed.
    ([#12](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/12))
  - Help for s3getvers shortened and fixed.
    ([#13](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/13))
- Internals
  - No significant changes

## ttr.aws.utils.s3 0.5.3 (2020-12-19)

- Bugfixes
  - `s3lsvers --version-id` finally works and starts fetching from version
    following given version-id
    ([#8](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/8))
- Features
  - removed testing for python 3.4 and 3.5. Tool may still work there.
    ([#5](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/5))
  - Add tests for python 3.8
    ([#6](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/6))
  - Add tests for python 3.9
    ([#7](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/7))
- Docs
  - ChangeLog/NEWS.txt refactored into CHANGELOG.md. Content using categories. Removed
    redundant entries.
    ([#9](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/9))
- Internals
  - Generate CHANGELOG.md using `proclamation` tool.
    ([#9](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/issues/9))

## ttr.aws.utils.s3 0.5.2 (2019-02-27)

- Bugfixes
  - Fixed line termination on Windows and UTF-8
- Features
- Docs
  - Updated NEWS.txt
- Internals
  - Fixed test failing due to new pytest features

## ttr.aws.utils.s3 0.5.1 (2018-08-21)

- Bugfixes
  - Fix plac version to 0.9.6 to fix parsing error
- Features
  - removed support for python 2.6, 3.3
  - added support for python 3.7
- Docs
  - Fixed sample .s3lsversrc
- Internals
  - cleanup .gitignore, add pylintrc

## ttr.aws.utils.s3 0.5.0 (2017-06-02)

- Bugfixes
  - fixed lsvers (invalid import)
  - Fixed broken getvers (invalid import)
- Features
  - Added support for python 3.3..3.6. Now supports python 2.6, 2.7, 3.3..3.6.
- Docs
  - Updated NEWS.txt
- Internals
  - Updated tox.ini
  - Added tests for FnameFactory
  - ttr.aws.utils.s3.saver module properly commented
  - CLI commands moved to ttr.aws.utils.s3.cli package

## ttr.aws.utils.s3 v0.4.5 (2017-05-10)

- Features
  - s3tmpgen got -http flag to generate http urls (instead of https)
- Internals
  - Rewritten to boto3
  - Rewritten to pbr.

## ttr.aws.utils.s3 v0.4.3 (2014-09-10)

- Bugfix
  - Resolves bug #2 - s3tmpgen generating shifted expiration time in url
    ([#2](https://gitlab.com/tamtamresearch-public/pypi/ttr.aws.utils.s3/-/issues/2))
- Docs
  - Updated repo url

## ttr.aws.utils.s3 v0.4.2.1 (2014-09-08)

- Bugfix
  - fix broken formatting of README.rst and NEWS.txt

## ttr.aws.utils.s3 v0.4.2 (2014-09-08)

- Bugfix
  - s3tmpgen generated url now points to the latest version, not to a specific version id
- Internals
  - Removed obsolete references from MANIFEST.in

## ttr.aws.utils.s3 v0.4.0 (2014-02-18)

- Bugfix
  - s3tmpget now really works
- Features
  - Added options to specify AWS credentials via boto profile_name
	(boto>=2.25.0) or explicit id and secret key
  - allow using aliases for bucket/key_name values in .s3lsvers
- Internals
  - Stop using buildout
  - Optimized creation of html chart - calculating datetime from epoch in milis
  - chart.html template added into packaging

## ttr.aws.utils.s3 v0.3.0 (2012-06-15)

- Features
  - added command s3tmpgen - generating temporary urls for selected keys in buckets

## ttr.aws.utils.s3 v0.2.3 (2012-05-28)

- Features
  - added command s3lsvers - to list key versions
  - added command s3getvers - to fetch versions listed in csv file
- Docs
  - corrected doc

## ttr.aws.utils.s3 v0.2.1

- Internals
  - refactor CLI from argparse to plac
- Features
  - removed option -period
  - added command s3getvers, fetching versions according to csv file
