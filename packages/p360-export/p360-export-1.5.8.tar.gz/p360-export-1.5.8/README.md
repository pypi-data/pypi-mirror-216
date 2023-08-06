# p360-export

Persona360 exporters.

### Latest Changes

* :bookmark: Bump version to 1.5.8. PR [#97](https://github.com/DataSentics/p360-export/pull/97) by [@Vinsho](https://github.com/Vinsho).
* :alien: Updated Facebok Api version to v16.0. PR [#96](https://github.com/DataSentics/p360-export/pull/96) by [@Vinsho](https://github.com/Vinsho).
* :bookmark: Bump version to 1.5.7. PR [#95](https://github.com/DataSentics/p360-export/pull/95) by [@Vinsho](https://github.com/Vinsho).
* :bug: ColumnHasher failed on None. PR [#94](https://github.com/DataSentics/p360-export/pull/94) by [@Vinsho](https://github.com/Vinsho).
* :bookmark: Bump version to 1.5.6. PR [#93](https://github.com/DataSentics/p360-export/pull/93) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Added new SFMC credential ftp_relative_path. PR [#92](https://github.com/DataSentics/p360-export/pull/92) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Added Google Analytics 4 exporter. PR [#82](https://github.com/DataSentics/p360-export/pull/82) by [@guderkar](https://github.com/guderkar).
#### 1.4.0
* :construction_worker: Fixed release workflow PR [#81](https://github.com/DataSentics/p360-export/pull/81) by [@Vinsho](https://github.com/Vinsho).
* :recycle: Typo fix. PR [#79](https://github.com/DataSentics/p360-export/pull/79) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Fixed backward compatibility. PR [#77](https://github.com/DataSentics/p360-export/pull/77) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Added logic for loading env specific config. PR [#76](https://github.com/DataSentics/p360-export/pull/76) by [@Vinsho](https://github.com/Vinsho).
* :recycle: Odap integration. PR [#75](https://github.com/DataSentics/p360-export/pull/75) by [@Vinsho](https://github.com/Vinsho).
* :art: Replaced pyfony with dependency-injector PR [#74](https://github.com/DataSentics/p360-export/pull/74) by [@Vinsho](https://github.com/Vinsho)
#### 1.3.1
* :bug: Don't fail on empty columns, don't send them to SFMC. PR [#72](https://github.com/DataSentics/p360-export/pull/72) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Added SFMC Field Name Fixer. PR [#71](https://github.com/DataSentics/p360-export/pull/71) by [@Vinsho](https://github.com/Vinsho).
* :bug: Fixed missing _ in less than and greater than. PR [#70](https://github.com/DataSentics/p360-export/pull/70) by [@Vinsho](https://github.com/Vinsho).
#### 1.3.0
* :recycle: Target user_list by export_id. PR [#68](https://github.com/DataSentics/p360-export/pull/68) by [@Vinsho](https://github.com/Vinsho).
* :recycle: Google ads export send User ID instead of email. PR [#67](https://github.com/DataSentics/p360-export/pull/67) by [@Vinsho](https://github.com/Vinsho).
* :recycle: Target audience based on its id part. PR [#66](https://github.com/DataSentics/p360-export/pull/66) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Work with SFMC Customer Keys. PR [#65](https://github.com/DataSentics/p360-export/pull/65) by [@Vinsho](https://github.com/Vinsho).
#### 1.2.1
* :technologist: Replace asserts with native unittest assertions. PR [#63](https://github.com/DataSentics/p360-export/pull/63) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Added not_equals to QueryBuilder. PR [#62](https://github.com/DataSentics/p360-export/pull/62) by [@Vinsho](https://github.com/Vinsho).
* :bug: Fixed query equals with multiple values. PR [#61](https://github.com/DataSentics/p360-export/pull/61) by [@Vinsho](https://github.com/Vinsho).
* :bug: Fixed attributes only export. PR [#60](https://github.com/DataSentics/p360-export/pull/60) by [@Vinsho](https://github.com/Vinsho).
#### 1.2.0
* :arrow_up: Feature store bundle upgrade to 2.7.1. PR [#57](https://github.com/DataSentics/p360-export/pull/57) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Enabled export without segment. PR [#56](https://github.com/DataSentics/p360-export/pull/56) by [@Vinsho](https://github.com/Vinsho).
* :recycle: Persona renamed to Segment. PR [#55](https://github.com/DataSentics/p360-export/pull/55) by [@Vinsho](https://github.com/Vinsho).
* :boom: Config is recieved as argument in runner. PR [#53](https://github.com/DataSentics/p360-export/pull/53) by [@Vinsho](https://github.com/Vinsho).
* :arrow_up: pyre-check-nightly replaced by pyre-check. PR [#54](https://github.com/DataSentics/p360-export/pull/54) by [@Vinsho](https://github.com/Vinsho).
#### 1.1.0
* :recycle: SFMC Exporter refactor. PR [#46](https://github.com/DataSentics/p360-export/pull/46) by [@Vinsho](https://github.com/Vinsho).
* :recycle: QueryBuilder and ExportManager refactor. PR [#49](https://github.com/DataSentics/p360-export/pull/49) by [@Vinsho](https://github.com/Vinsho).
* :recycle: ColumnSampleGetter turned to service. PR [#47](https://github.com/DataSentics/p360-export/pull/47) by [@Vinsho](https://github.com/Vinsho).
* :arrow_up: Unpin the fixed feature-store-bundle version. PR [#48](https://github.com/DataSentics/p360-export/pull/48) by [@Vinsho](https://github.com/Vinsho).
* :recycle: Google Ads Exporter Refactor. PR [#44](https://github.com/DataSentics/p360-export/pull/44) by [@Vinsho](https://github.com/Vinsho).
* ♻️ TypeGuesser component refactor. PR [#35](https://github.com/DataSentics/p360-export/pull/35) by [@Vinsho](https://github.com/Vinsho).
* :recycle: Facebook Exporter refactor. PR [#43](https://github.com/DataSentics/p360-export/pull/43) by [@Vinsho](https://github.com/Vinsho).
* :recycle: Data Picker components refactor. PR [#40](https://github.com/DataSentics/p360-export/pull/40) by [@Vinsho](https://github.com/Vinsho).
* :green_heart: Fixed failing pylint tests. PR [#42](https://github.com/DataSentics/p360-export/pull/42) by [@Vinsho](https://github.com/Vinsho).
* :technologist: Alter pylint to pyfony coding style. PR [#41](https://github.com/DataSentics/p360-export/pull/41) by [@Vinsho](https://github.com/Vinsho).

#### 1.0.2
* :arrow_up: Feature store bundle update to 2.5.1. PR [#36](https://github.com/DataSentics/p360-export/pull/36) by [@matejoravec](https://github.com/matejoravec).
* :construction_worker: Release pipeline customized. PR [#34](https://github.com/DataSentics/p360-export/pull/34) by [@matejoravec](https://github.com/matejoravec).

#### 1.0.1
* :memo: Missing emojis added to README. PR [#31](https://github.com/DataSentics/p360-export/pull/31) by [@matejoravec](https://github.com/matejoravec).
* :arrow_up: feature-store-bundle 2.5.0b2 -> 2.5.0b3. PR [#30](https://github.com/DataSentics/p360-export/pull/30) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Make created Data Extension sendable. PR [#29](https://github.com/DataSentics/p360-export/pull/29) by [@Vinsho](https://github.com/Vinsho).
* :bug: Fixed Type Guesser bugs. PR [#28](https://github.com/DataSentics/p360-export/pull/28) by [@Vinsho](https://github.com/Vinsho).
* :sparkles: Added Type Guesser. PR [#27](https://github.com/DataSentics/p360-export/pull/27) by [@Vinsho](https://github.com/Vinsho).
* :building_construction: Retrieval of redundant attributes removed. PR [#26](https://github.com/DataSentics/p360-export/pull/26) by [@matejoravec](https://github.com/matejoravec).
* :sparkles: SFMC Exporter: Enable field updating. PR [#23](https://github.com/DataSentics/p360-export/pull/23) by [@Vinsho](https://github.com/Vinsho).
* :construction_worker: Build & Release Pipeline outsourced. PR [#25](https://github.com/DataSentics/p360-export/pull/25) by [@matejoravec](https://github.com/matejoravec).
* :construction_worker: Latest changes action added. PR [#24](https://github.com/DataSentics/p360-export/pull/24) by [@matejoravec](https://github.com/matejoravec).
