---
name: "SPEC.md"
description: "Functional specification for the Version Sync Checker skill"
created_date: "2026/05/15 18:36:37 CST"
modified_date: "2026/05/15 18:36:37 CST"
project_version: "0.1.0"
document_version: "1.0.0"
agent_sign: ["human/mimas", "codex/gpt-5"]
---

# Specification

## Purpose

This skill checks whether project version metadata stays aligned across Markdown documents, changelogs, and optional package metadata.

## Source Of Truth

`CHANGELOG.md` is the primary source of the project version.

## Requirements

- YAML front matter must be read only from the start of a file.
- A valid front matter block starts with a standalone `---` line and ends at the next standalone `---` line.
- Markdown horizontal rules in the body must not be treated as front matter.
- The parser must support UTF-8 BOM, LF, and CRLF inputs.
