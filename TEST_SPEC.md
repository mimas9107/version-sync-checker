---
name: "TEST_SPEC.md"
description: "Comparison test specification and observed results for old and new YAML front matter parsing behavior"
created_date: "2026/05/15 18:48:32 CST"
modified_date: "2026/05/15 18:48:32 CST"
project_version: "0.1.0"
document_version: "1.0.0"
agent_sign: ["human/mimas", "codex/gpt-5"]
---

# Test Specification

## Purpose

This document records the comparison test set used to evaluate the previous regex-based parser against the current start-of-file front matter parser.

The goal of the comparison is to verify whether Markdown body-level horizontal rules (`---`) can interfere with YAML front matter detection and to identify the exact failure conditions in the previous implementation.

## Compared Implementations

- Old version: commit `c6e9bd0`
- New version: current implementation after `Fix YAML front matter parsing`

## Test Method

- Both implementations were executed without modifying either version's source code.
- A temporary test workspace was created for each case.
- Each case was evaluated with the same input content.
- Single-file cases called `check_file_header("README.md", [1, 2, 3])`.
- The integration case called `run_check()` against a full document set containing `CHANGELOG.md`, `README.md`, `SPEC.md`, and `MEMOIR.md`.

## Test Set

### A. LF Header With Body Rule

- YAML front matter starts at the first line of the file.
- Line endings use `LF`.
- The document body contains a Markdown horizontal rule `---`.

Expected verification target:
- Body-level horizontal rules must not affect a valid front matter at the start of the file.

### B. BOM Header Without Body Rule

- YAML front matter starts at the first logical line but is preceded by `UTF-8 BOM`.
- The document body does not contain a Markdown horizontal rule.

Expected verification target:
- BOM-prefixed files must still be recognized as having valid front matter.

### C. BOM Header With Body Rule

- YAML front matter starts at the first logical line but is preceded by `UTF-8 BOM`.
- The document body contains one Markdown horizontal rule `---`.

Expected verification target:
- BOM-prefixed valid front matter must be parsed correctly.
- A body-level horizontal rule must not become a fallback delimiter candidate.

### D. BOM Header With Two Body Rules

- YAML front matter starts at the first logical line but is preceded by `UTF-8 BOM`.
- The document body contains two Markdown horizontal rules `---`.

Expected verification target:
- Multiple body-level horizontal rules must not influence header parsing.

### E. Integration Case

- `CHANGELOG.md`, `README.md`, `SPEC.md`, and `MEMOIR.md` all contain:
- A valid YAML front matter
- A leading `UTF-8 BOM`
- A Markdown horizontal rule in the document body

Expected verification target:
- `run_check()` must derive `expected_version` from `CHANGELOG.md`.
- All mandatory files must report `ok`.

## Observed Results

### Single-File Cases

| Case | Old version | New version |
| --- | --- | --- |
| A. LF header with body rule | `ok` | `ok` |
| B. BOM header without body rule | `missing_header` | `ok` |
| C. BOM header with body rule | `error: 'NoneType' object has no attribute 'get'` | `ok` |
| D. BOM header with two body rules | `error: 'NoneType' object has no attribute 'get'` | `ok` |

### Integration Case

| Implementation | Result |
| --- | --- |
| Old version | `expected_version` was resolved as `0.1.0`, but all mandatory files returned `error: 'NoneType' object has no attribute 'get'` |
| New version | `expected_version` was resolved as `0.1.0`, and all mandatory files returned `ok` |

## Interpretation

- The old implementation was not broken by body-level horizontal rules alone.
- The old implementation failed when the real YAML front matter was not matched first, especially in BOM-prefixed files.
- Under that condition, body-level `---` lines could participate in an incorrect regex match and produce false negatives or parse errors.
- The new implementation avoids this class of failure by only accepting front matter that begins at the start of the file and ends at the next standalone delimiter line.

## Conclusion

The current implementation is verified to be robust against Markdown body horizontal rules in the tested scenarios.

The comparison also confirms that the previous implementation could be misled by the combination of `UTF-8 BOM` and body-level `---`, which explains the earlier false detection behavior.
