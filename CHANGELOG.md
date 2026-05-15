---
name: "CHANGELOG.md"
description: "Version history for the Version Sync Checker skill"
created_date: "2026/05/15 18:36:37 CST"
modified_date: "2026/05/15 18:37:35 CST"
project_version: "0.1.0"
document_version: "1.0.1"
agent_sign: ["human/mimas", "codex/gpt-5"]
---

# Changelog

## [0.1.0] - 2026-05-15

### Added
- Added `CHANGELOG.md`, `SPEC.md`, and `MEMOIR.md` with aligned YAML front matter.
- Added regression and integration tests for YAML front matter parsing and end-to-end version checks.

### Changed
- Replaced regex-based front matter detection with a start-of-file parser that handles BOM, LF, and CRLF safely.
- Prevented Markdown horizontal rules in document bodies from being misidentified as YAML front matter delimiters.

### Verified
- Passed `python3 -m unittest discover -s tests -v` with 7 tests.
- Passed `python3 scripts/check_version.py .` with all mandatory documents reporting `ok` at project version `0.1.0`.
