import tempfile
import unittest
from pathlib import Path

from scripts.check_version import VersionSyncChecker


class ExtractYamlFrontMatterTests(unittest.TestCase):
    def setUp(self):
        self.checker = VersionSyncChecker()

    def test_extracts_header_from_file_start_only(self):
        content = (
            "---\n"
            'project_version: "1.2.3"\n'
            "---\n"
            "\n"
            "# Title\n"
            "\n"
            "---\n"
            "body\n"
        )

        header = self.checker.extract_yaml_front_matter(content)

        self.assertEqual(header, 'project_version: "1.2.3"\n')

    def test_supports_crlf(self):
        content = (
            "---\r\n"
            'project_version: "1.2.3"\r\n'
            "---\r\n"
            "\r\n"
            "body\r\n"
            "---\r\n"
        )

        header = self.checker.extract_yaml_front_matter(content)

        self.assertEqual(header, 'project_version: "1.2.3"\r\n')

    def test_supports_utf8_bom(self):
        content = (
            "\ufeff---\n"
            'project_version: "1.2.3"\n'
            "---\n"
            "\n"
            "body\n"
            "---\n"
        )

        header = self.checker.extract_yaml_front_matter(content)

        self.assertEqual(header, 'project_version: "1.2.3"\n')

    def test_returns_none_without_front_matter_at_file_start(self):
        content = "# Title\n\n---\nbody\n---\n"

        header = self.checker.extract_yaml_front_matter(content)

        self.assertIsNone(header)

    def test_returns_none_when_header_is_unterminated(self):
        content = "---\nproject_version: \"1.2.3\"\nbody\n"

        header = self.checker.extract_yaml_front_matter(content)

        self.assertIsNone(header)


class CheckFileHeaderTests(unittest.TestCase):
    def test_accepts_markdown_horizontal_rule_in_body(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            file_path = root / "README.md"
            file_path.write_text(
                "---\n"
                'project_version: "1.2.3"\n'
                "---\n"
                "\n"
                "# Title\n"
                "\n"
                "---\n"
                "content\n",
                encoding="utf-8",
            )

            checker = VersionSyncChecker(str(root))
            result = checker.check_file_header("README.md", [1, 2, 3])

            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["version"], "1.2.3")


class RunCheckIntegrationTests(unittest.TestCase):
    def test_run_check_reports_aligned_mandatory_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            docs = {
                "CHANGELOG.md": (
                    "---\n"
                    'project_version: "0.1.0"\n'
                    "---\n"
                    "\n"
                    "# Changelog\n"
                    "\n"
                    "## [0.1.0] - 2026-05-15\n"
                    "- Initial release\n"
                ),
                "README.md": (
                    "---\n"
                    'project_version: "0.1.0"\n'
                    "---\n"
                    "\n"
                    "# README\n"
                    "\n"
                    "---\n"
                    "Body rule\n"
                ),
                "SPEC.md": (
                    "---\n"
                    'project_version: "0.1.0"\n'
                    "---\n"
                    "\n"
                    "# SPEC\n"
                ),
                "MEMOIR.md": (
                    "---\n"
                    'project_version: "0.1.0"\n'
                    "---\n"
                    "\n"
                    "# MEMOIR\n"
                ),
            }

            for name, content in docs.items():
                (root / name).write_text(content, encoding="utf-8")

            checker = VersionSyncChecker(str(root))
            result = checker.run_check()

            self.assertEqual(result["expected_version"], "0.1.0")
            for file_name in docs:
                self.assertEqual(result["files"][file_name]["status"], "ok")


if __name__ == "__main__":
    unittest.main()
